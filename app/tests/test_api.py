import pytest
from app.social_network.models import Post, Like
from django.contrib.auth import get_user_model
from django.urls import reverse
from urllib.parse import urlencode

User = get_user_model()


@pytest.mark.celery
@pytest.mark.django_db
def test_signup(client, mocker):
    mocker.patch(
        "app.social_network.tasks.clearbit_client.get_enrichment",
        return_value=dict(person=dict(name=dict(fullName="Kirill Bakanov"))),
    )

    mocker.patch(
        "app.social_network.serializers.pyhunter_client.verify_email",
        return_value=dict(result="risky", score=50),
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


@pytest.mark.django_db
def test_create_post(admin_client, admin_user):
    response = admin_client.post(
        reverse("create_post"), data={"title": "New post", "text": "New text"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "New post"

    assert Post.objects.count() == 1
    assert Post.objects.first().author == admin_user


@pytest.mark.django_db
def test_post_like(admin_client, admin_user):
    post = Post.objects.create(title="text", text="text", author=admin_user)

    response = admin_client.post(reverse("like_post", kwargs={"post_id": post.id}), data={})
    assert response.status_code == 201
    assert Like.objects.filter(post=post).count() == 1

    response = admin_client.post(reverse("like_post", kwargs={"post_id": post.id}), data={})
    assert response.status_code == 400
    assert Like.objects.filter(post=post).count() == 1


@pytest.mark.django_db
def test_post_dislike(admin_client, admin_user):
    like = Like.objects.create(
        author=admin_user,
        post=Post.objects.create(title="text", text="text", author=admin_user),
    )
    assert Like.objects.count() == 1

    response = admin_client.delete(reverse("dislike_post", kwargs={"post_id": like.post.id}), data={})
    assert response.status_code == 204
    assert Like.objects.count() == 0

    response = admin_client.delete(reverse("dislike_post", kwargs={"post_id": like.post.id}), data={})
    assert response.status_code == 404


@pytest.mark.django_db
def test_analytics(client, admin_user):
    likes = []
    for i in range(0, 5):
        likes.append(
            Like.objects.create(
                author=admin_user,
                post=Post.objects.create(title=i, text=i, author=admin_user),
            )
        )
    query = {"created_at_before": likes[2].created_at.isoformat()}
    response = client.get(f"{reverse('analytics')}?{urlencode(query)}", )
    assert response.status_code == 200
    assert response.json()["likes"] == 3

    query = {"created_at_after": likes[3].created_at.isoformat()}
    response = client.get(f"{reverse('analytics')}?{urlencode(query)}", )
    assert response.status_code == 200
    assert response.json()["likes"] == 2

    query = {
        "created_at_after": likes[1].created_at.isoformat(),
        "created_at_before": likes[3].created_at.isoformat(),
    }
    response = client.get(f"{reverse('analytics')}?{urlencode(query)}", )
    assert response.status_code == 200
    assert response.json()["likes"] == 3
