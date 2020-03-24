from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from app.social_network.filters import LikeFilter
from app.social_network.models import Like, Post
from app.social_network.serializers import (
    AnalyticsSerializer,
    LikeSerializer,
    PostSerializer,
    SignupSerializer,
)
from app.social_network.utils import get_tokens_for_user


class SignupView(GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = serializer.data
        response_data["token"] = get_tokens_for_user(user)
        return Response(response_data, status=status.HTTP_201_CREATED)


class PostViewset(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.select_related("author").prefetch_related("likes").all()


class PostLikeView(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer
    lookup_field = "post"
    lookup_url_kwarg = "post_id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["post"] = Post.objects.filter(id=self.kwargs["post_id"]).first()
        return context

    def get_queryset(self):
        return Like.objects.select_related("author", "post").filter(
            author=self.request.user
        )


class AnalyticsView(GenericAPIView):
    http_method_names = ["get"]
    queryset = Like.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LikeFilter
    serializer_class = AnalyticsSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).aggregate(
            likes=Count("id")
        )
        serializer = self.get_serializer(
            {"likes": queryset["likes"], "date_from": None, "date_to": None}
        )
        return Response(serializer.data)
