from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}: {self.created_at}"


class Like(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.email} on post: {self.post.title} at {self.created_at}"

    class Meta:
        unique_together = ["author", "post"]


class Bot(BaseModel):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
