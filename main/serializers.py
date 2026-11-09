from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Achievement, Experience


def clean_text(value, required=False, label="Field"):
    """Strip HTML tags; optionally reject values that become empty."""
    value = strip_tags(value).strip()
    if required and not value:
        raise serializers.ValidationError(f"{label} cannot be empty.")
    return value


class StarFieldsSerializer(serializers.ModelSerializer):
    """Read-only computed star fields shared by all starrable models."""
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class AchievementSerializer(StarFieldsSerializer):
    level_display = serializers.CharField(source="get_level_display", read_only=True)

    class Meta:
        model = Achievement
        fields = [
            "id", "title", "issuer", "description", "level", "level_display",
            "date_achieved", "certificate_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        return clean_text(value, True, "Title")

    def validate_issuer(self, value):
        return clean_text(value, True, "Issuer")

    def validate_description(self, value):
        return clean_text(value)


class ExperienceSerializer(StarFieldsSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category", "category_display",
            "thumbnail", "started_at", "ended_at", "is_ongoing",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        return clean_text(value, True, "Title")

    def validate_description(self, value):
        return clean_text(value)

    def validate(self, attrs):
        started = attrs.get("started_at", getattr(self.instance, "started_at", None))
        ended = attrs.get("ended_at", getattr(self.instance, "ended_at", None))
        if started and ended and ended < started:
            raise serializers.ValidationError(
                {"ended_at": "End date cannot be before start date."}
            )
        return attrs