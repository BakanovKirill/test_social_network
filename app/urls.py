from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views

from app.social_network.views import (
    AnalyticsView,
    PostLikeView,
    PostViewset,
    SignupView,
)

API_VERSION = "v1"

schema_view = get_schema_view(
    openapi.Info(
        title="Social Network API",
        default_version="v1",
        description="Social network with bot",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kirill.bakanov@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_urlpatterns = [
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", SignupView.as_view(), name="api_signup"),
    path("posts/", PostViewset.as_view({"post": "create"}), name="create_post"),
    path(
        "posts/<int:post_id>/like",
        PostLikeView.as_view({"post": "create"}),
        name="like_post",
    ),
    path(
        "posts/<int:post_id>/dislike",
        PostLikeView.as_view({"delete": "destroy"}),
        name="dislike_post",
    ),
    path("analytics/", AnalyticsView.as_view(), name="analytics"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path(f"api/{API_VERSION}/", include(api_urlpatterns)),
]
