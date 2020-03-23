import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.celery
@pytest.mark.django_db
def test_signup(client, mocker):
    mocker.patch(
        "app.social_network.tasks.clearbit_client.get_enrichment",
        return_value=dict(person=dict(name=dict(fullName="Kirill Bakanov"))),
    )

    email = "abc@i.ua"
    response = client.post(
        reverse("api_signup"),
        data={"email": email, "password1": "Test12345", "password2": "Test12345"},
    )

    assert response.status_code == 201
    assert sorted(response.json().keys()) == sorted(["username", "email", "token"])
    user = User.objects.filter(email=email).first()
    assert user
    assert user.first_name == "Kirill"
    assert user.last_name == "Bakanov"
