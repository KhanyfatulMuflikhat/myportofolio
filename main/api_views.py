"""Function-based DRF views under /api/v1/. Authorization lives in main.permissions."""
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Achievement, Experience
from main.permissions import AchievementPermission, ExperiencePermission
from main.serializers import AchievementSerializer, ExperienceSerializer


def _filtered_achievements(params):
    """Apply the level, q and sort query params to the Achievement queryset."""
    queryset = Achievement.objects.prefetch_related("starred_by")
    level = params.get("level", "").strip()
    q = params.get("q", "").strip()
    if level:
        queryset = queryset.filter(level=level)
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q) | Q(issuer__icontains=q) | Q(description__icontains=q)
        )
    if params.get("sort") == "stars":
        return queryset.annotate(star_total=Count("starred_by")).order_by(
            "-star_total", "-date_achieved", "id"
        )
    return queryset.order_by("-date_achieved", "id")


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([AchievementPermission])
def achievement_list(request):
    """GET: list with ?level, ?q, ?sort=stars. POST: create (owner only)."""
    if request.method in ("GET", "HEAD"):
        serializer = AchievementSerializer(
            _filtered_achievements(request.query_params),
            many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = AchievementSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([AchievementPermission])
def achievement_detail(request, achievement_id):
    """GET: read. PUT/PATCH: owner or Editor. DELETE: owner only."""
    achievement = get_object_or_404(
        Achievement.objects.prefetch_related("starred_by"), pk=achievement_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = AchievementSerializer(achievement, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        achievement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = AchievementSerializer(
        achievement, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


def _toggle_star(request, model, serializer_class, pk):
    """Toggle request.user's star on the object and return its fresh representation."""
    obj = get_object_or_404(model, pk=pk)
    if obj.starred_by.filter(pk=request.user.pk).exists():
        obj.starred_by.remove(request.user)
    else:
        obj.starred_by.add(request.user)
    return Response(serializer_class(obj, context={"request": request}).data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def achievement_star(request, achievement_id):
    """POST: toggle the logged-in user's star."""
    return _toggle_star(request, Achievement, AchievementSerializer, achievement_id)


def _filtered_experiences(params):
    """Apply the category, q and sort query params to the Experience queryset."""
    queryset = Experience.objects.prefetch_related("starred_by")
    category = params.get("category", "").strip()
    q = params.get("q", "").strip()
    if category:
        queryset = queryset.filter(category=category)
    if q:
        queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if params.get("sort") == "stars":
        return queryset.annotate(star_total=Count("starred_by")).order_by(
            "-star_total", "-started_at", "id"
        )
    return queryset.order_by("-started_at", "id")


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([ExperiencePermission])
def experience_list(request):
    """GET: list with ?category, ?q, ?sort=stars. POST: create (owner only)."""
    if request.method in ("GET", "HEAD"):
        serializer = ExperienceSerializer(
            _filtered_experiences(request.query_params),
            many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ExperienceSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([ExperiencePermission])
def experience_detail(request, experience_id):
    """GET: read. PUT/PATCH: owner or Editor. DELETE: owner only."""
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"), pk=experience_id,
    )
    if request.method in ("GET", "HEAD"):
        return Response(ExperienceSerializer(experience, context={"request": request}).data)

    if request.method == "DELETE":
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ExperienceSerializer(
        experience, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    """POST: toggle the logged-in user's star."""
    return _toggle_star(request, Experience, ExperienceSerializer, experience_id)