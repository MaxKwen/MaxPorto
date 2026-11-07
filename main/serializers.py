from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Achievement, Experience, Project


def clean_text(value, *, required=False, label="This field"):
    """Buang tag HTML (setara clean_<field> di form); tolak teks wajib yang jadi kosong."""
    value = strip_tags(value or "").strip()
    if required and not value:
        raise serializers.ValidationError(f"{label} cannot be empty.")
    return value


class StarInfoMixin(serializers.Serializer):
    """Informasi star dari sebagai field hasil perhitungan."""

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
        # Hanya username; email dan password hash tidak pernah dikirim
        return ", ".join(user.username for user in obj.starred_by.all())


class ProjectSerializer(StarInfoMixin, serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "title_id", "description_id",
            "category", "project_url", "thumbnail", "is_featured",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    # Validasi setara ProjectForm, karena API tidak melewati form
    def validate_title(self, value):
        return clean_text(value, required=True, label="Title")

    def validate_title_id(self, value):
        return clean_text(value)

    def validate_description(self, value):
        return clean_text(value)

    def validate_description_id(self, value):
        return clean_text(value)

    def validate_category(self, value):
        return clean_text(value, required=True, label="Category")


YEAR_LIMITS = {"min_value": 1900, "max_value": 2100}


class ExperienceSerializer(StarInfoMixin, serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            "id", "title", "title_id", "organization", "organization_id",
            "description", "description_id", "category", "start_year", "end_year",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]
        # Batas tahun sama dengan ExperienceForm
        extra_kwargs = {"start_year": YEAR_LIMITS, "end_year": YEAR_LIMITS}

    def validate_title(self, value):
        return clean_text(value, required=True, label="Title")

    def validate_title_id(self, value):
        return clean_text(value)

    def validate_organization(self, value):
        return clean_text(value, required=True, label="Organization")

    def validate_organization_id(self, value):
        return clean_text(value)

    def validate_description(self, value):
        return clean_text(value, required=True, label="Description")

    def validate_description_id(self, value):
        return clean_text(value)

    def validate_category(self, value):
        return clean_text(value, required=True, label="Category")

    def validate(self, attrs):
        # Saat PATCH, bandingkan dengan nilai lama untuk field yang tidak dikirim
        start_year = attrs.get("start_year", getattr(self.instance, "start_year", None))
        end_year = attrs.get("end_year", getattr(self.instance, "end_year", None))
        if start_year is not None and end_year is not None and end_year < start_year:
            raise serializers.ValidationError(
                {"end_year": ["End year cannot be earlier than start year."]}
            )
        return attrs


class AchievementSerializer(StarInfoMixin, serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = [
            "id", "title", "title_id", "result", "result_id", "category",
            "year", "display_order",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]
        # Batas tahun sama dengan AchievementForm; tahun boleh kosong
        extra_kwargs = {"year": YEAR_LIMITS}

    def validate_title(self, value):
        return clean_text(value, required=True, label="Title")

    def validate_title_id(self, value):
        return clean_text(value)

    def validate_result(self, value):
        return clean_text(value, required=True, label="Result")

    def validate_result_id(self, value):
        return clean_text(value)

    def validate_category(self, value):
        return clean_text(value, required=True, label="Category")
