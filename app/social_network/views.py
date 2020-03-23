from app.social_network.serializers import SignupSerializer
from app.social_network.utils import get_tokens_for_user
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class SignupView(GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = serializer.data
        response_data["token"] = get_tokens_for_user(user)
        return Response(response_data, status=status.HTTP_201_CREATED)
