from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers
from .tasks import enrich_user

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=8, required=True, write_only=True)
    password2 = serializers.CharField(min_length=8, required=True, write_only=True)
    email = serializers.EmailField(required=True, allow_blank=False)
    username = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def validate(self, data):
        validated_data = super().validate(data)
        email = validated_data.get("email")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "User with such email already exists"}
            )

        validated_data["username"] = email

        user_creation_form = UserCreationForm(data=validated_data)
        if not user_creation_form.is_valid():
            raise serializers.ValidationError(user_creation_form.errors)

        validated_data.pop("password2")
        validated_data["password"] = make_password(validated_data.pop("password1"))

        return validated_data

    def create(self, validated_data):
        with transaction.atomic():
            user = super().create(validated_data)
            user.save()

        enrich_user.delay(user.id)
        return user
