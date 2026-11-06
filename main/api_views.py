from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Experience, Project
from main.permissions import (
    IsPortfolioOwnerOrEditorOrReadOnly, IsPortfolioOwnerOrReadOnly,
)
from main.serializers import ExperienceSerializer, ProjectSerializer


# ---------- Helper bersama; izin sudah diperiksa permission class ----------

def create_response(request, serializer_class):
    serializer = serializer_class(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def detail_response(request, obj, serializer_class):
    """GET, PUT/PATCH, dan DELETE untuk satu objek."""
    if request.method in ("GET", "HEAD"):
        return Response(serializer_class(obj, context={"request": request}).data)

    if request.method == "DELETE":
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = serializer_class(
        obj, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


def toggle_star(request, obj, serializer_class):
    """Beri/batalkan star atas nama request.user, lalu kembalikan data terbaru."""
    if obj.starred_by.filter(pk=request.user.pk).exists():
        obj.starred_by.remove(request.user)
    else:
        obj.starred_by.add(request.user)
    return Response(serializer_class(obj, context={"request": request}).data)


# ---------- Projects (Tutorial 07): hanya pemilik yang boleh menulis ----------

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    if request.method in ("GET", "HEAD"):
        projects = Project.objects.prefetch_related("starred_by").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            projects = projects.filter(title__icontains=title)
        serializer = ProjectSerializer(
            projects, many=True, context={"request": request},
        )
        return Response(serializer.data)
    return create_response(request, ProjectSerializer)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related("starred_by"), pk=project_id,
    )
    return detail_response(request, project, ProjectSerializer)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return toggle_star(request, project, ProjectSerializer)


# ---------- Experience (Tugas 6): Editor juga boleh PUT/PATCH ----------

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    if request.method in ("GET", "HEAD"):
        experiences = Experience.objects.prefetch_related("starred_by").order_by(
            "-start_year", "id"
        )
        # Pencarian Tugas 5 (?q=) dipindah ke parameter query endpoint ini
        query = request.query_params.get("q", "").strip()
        if query:
            experiences = experiences.filter(
                Q(title__icontains=query)
                | Q(title_id__icontains=query)
                | Q(organization__icontains=query)
                | Q(organization_id__icontains=query)
            )
        serializer = ExperienceSerializer(
            experiences, many=True, context={"request": request},
        )
        return Response(serializer.data)
    return create_response(request, ExperienceSerializer)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"), pk=experience_id,
    )
    return detail_response(request, experience, ExperienceSerializer)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    return toggle_star(request, experience, ExperienceSerializer)
