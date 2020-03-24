from django_filters import rest_framework as filters

from app.social_network.models import Like


class LikeFilter(filters.FilterSet):
    created_at = filters.IsoDateTimeFromToRangeFilter()

    class Meta:
        model = Like
        fields = ["created_at"]
