"""Halaman, API JSON, CRUD, dan star proyek."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from main.copy import PROJECT_COPY
from main.forms import ProjectForm
from main.models import Project
from main.permissions import is_editor


# Halaman HTML
def show_projects(request, language="en"):
    title_query = request.GET.get("title", "").strip()
    context = {
        "copy": PROJECT_COPY[language],
        "title_query": title_query,
        "is_editor": is_editor(request.user),
        "form": ProjectForm(),
    }
    return render(request, "projects/list.html", context)


# API JSON untuk daftar dan pencarian AJAX
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related("starred_by").all()
    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []
    for project in projects:
        starred_users = list(project.starred_by.all())
        data.append(
            {
                "model": "main.project",
                "pk": project.pk,
                "fields": {
                    "title": project.title,
                    "title_id": project.title_id,
                    "description": project.description,
                    "description_id": project.description_id,
                    "category": project.category,
                    "project_url": project.project_url,
                    "thumbnail": project.thumbnail,
                    "is_featured": project.is_featured,
                    "starred_by": [
                        [user.username] for user in starred_users
                    ],
                    "star_count": len(starred_users),
                    "is_starred": request.user.is_authenticated
                    and any(user.pk == request.user.pk for user in starred_users),
                    "starred_by_names": ", ".join(
                        user.username for user in starred_users
                    ),
                    "can_update": request.user.is_superuser
                    or is_editor(request.user),
                    "can_delete": request.user.is_superuser,
                    "update_url": reverse(
                        "main:update_project", args=[project.pk]
                    ),
                    "delete_url": reverse(
                        "main:delete_project", args=[project.pk]
                    ),
                    "star_url": reverse("main:toggle_star", args=[project.pk]),
                },
            }
        )

    return JsonResponse(data, safe=False)


# Tambah melalui form halaman
@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "copy": PROJECT_COPY["en"],
        "form": form,
        "form_title": "Add Project",
        "form_eyebrow": "Portfolio / Projects",
        "form_heading": "Add New Project",
        "form_intro": "Add a project to your portfolio.",
        "submit_label": "Tambah Proyek",
    }
    return render(request, "projects/form.html", context)


# Tambah melalui modal AJAX
@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


# Edit melalui form halaman
@login_required(login_url="/login/")
def update_project(request, project_id):
    if not request.user.is_superuser and not is_editor(request.user):
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "copy": PROJECT_COPY["en"],
        "form": form,
        "form_title": "Update Project",
        "form_eyebrow": "Portfolio / Projects",
        "form_heading": "Update Project",
        "form_intro": "Update this project in your portfolio.",
        "submit_label": "Simpan Perubahan",
    }
    return render(request, "projects/form.html", context)


# Hapus melalui POST
@login_required(login_url="/login/")
@require_POST
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    messages.success(request, "Proyek berhasil dihapus!")
    return redirect("main:show_projects")


# Toggle star untuk pengguna login
@login_required(login_url="/login/")
@require_POST
def toggle_project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.user in project.starred_by.all():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)

    return redirect("main:show_projects")
