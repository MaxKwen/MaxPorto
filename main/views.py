from django.contrib import messages
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied 
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from main.forms import AchievementForm, ExperienceForm, ProjectForm
from main.models import Achievement, Experience, Project, Skill

import datetime


PROJECT_COPY = {
    "en": {
        "language": "en",
        "page_title": "Projects",
        "meta_description": "Projects by Maximus Quinn Hertada.",
        "experience": "Experience",
        "skills": "Skills",
        "projects": "Projects",
        "achievements": "Achievements",
        "switch_label": "ID",
        "eyebrow": "Portfolio / Projects",
        "intro": "Selected work across software, connected devices, and applied research.",
        "featured": "Featured project",
        "view_project": "View project",
        "add_project": "Add Project",
        "edit_project": "Edit Project",
        "search": "Search",
        "search_placeholder": "Search by project title",
        "no_results": "No projects match that title.",
        "delete_project": "Delete Project",
        "delete_title": "Delete project?",
        "delete_prompt": "Are you sure you want to delete",
        "cancel": "Cancel",
        "confirm_delete": "Yes, delete",
        "empty_state": "No projects have been added yet.",
    },
    "id": {
        "language": "id",
        "page_title": "Proyek",
        "meta_description": "Proyek karya Maximus Quinn Hertada.",
        "experience": "Pengalaman",
        "skills": "Keahlian",
        "projects": "Proyek",
        "achievements": "Prestasi",
        "switch_label": "EN",
        "eyebrow": "Portofolio / Proyek",
        "intro": "Karya pilihan dalam perangkat lunak, perangkat terhubung, dan riset terapan.",
        "featured": "Proyek unggulan",
        "view_project": "Lihat proyek",
        "add_project": "Tambah Proyek",
        "edit_project": "Edit Proyek",
        "search": "Cari",
        "search_placeholder": "Cari berdasarkan judul proyek",
        "no_results": "Tidak ada proyek dengan judul tersebut.",
        "delete_project": "Hapus Proyek",
        "delete_title": "Hapus proyek?",
        "delete_prompt": "Apakah kamu yakin ingin menghapus",
        "cancel": "Batal",
        "confirm_delete": "Ya, hapus",
        "empty_state": "Belum ada proyek yang ditambahkan.",
    },
}

EXPERIENCE_COPY = {
    "en": {
        "language": "en",
        "page_title": "Experience",
        "meta_description": "Experience of Maximus Quinn Hertada.",
        "experience": "Experience",
        "skills": "Skills",
        "projects": "Projects",
        "achievements": "Achievements",
        "switch_label": "ID",
        "eyebrow": "Portfolio / Experience",
        "intro": "Roles and communities that have shaped my professional growth.",
        "add_experience": "Add Experience",
        "add_heading": "Add New Experience",
        "adding": "Adding...",
        "close_form": "Close add experience form",
        "add_success_title": "Success",
        "add_success": "Experience added successfully.",
        "add_error_title": "Could not add experience",
        "add_error": "The request failed. Please try again.",
        "connection_error": "Could not reach the server. Please try again.",
        "permission_denied": "Only the portfolio owner can add experience.",
        "request_rejected": "Request rejected. Refresh the page and check your access.",
        "form_labels": {
            "title": "Role (English)",
            "title_id": "Role (Indonesian)",
            "organization": "Organization (English)",
            "organization_id": "Organization (Indonesian)",
            "description": "Description (English)",
            "description_id": "Description (Indonesian)",
            "category": "Category",
            "start_year": "Start year",
            "end_year": "End year",
        },
        "edit_experience": "Edit Experience",
        "delete_experience": "Delete Experience",
        "delete_title": "Delete experience?",
        "delete_prompt": "Are you sure you want to delete",
        "cancel": "Cancel",
        "confirm_delete": "Yes, delete",
        "star": "Star",
        "unstar": "Unstar",
        "starred_by": "Starred by",
        "first_star": "Be the first to star this experience",
        "present": "present",
        "search": "Search",
        "search_placeholder": "Search by role or organization",
        "no_results": "No experience matches your search.",
        "loading": "Loading experience...",
        "load_error": "Failed to load experience. Please try again.",
        "retry": "Try again",
        "empty_state": "No experience has been added yet.",
    },
    "id": {
        "language": "id",
        "page_title": "Pengalaman",
        "meta_description": "Pengalaman Maximus Quinn Hertada.",
        "experience": "Pengalaman",
        "skills": "Keahlian",
        "projects": "Proyek",
        "achievements": "Prestasi",
        "switch_label": "EN",
        "eyebrow": "Portofolio / Pengalaman",
        "intro": "Peran dan komunitas yang membentuk perkembangan profesional saya.",
        "add_experience": "Tambah Pengalaman",
        "add_heading": "Tambah Pengalaman Baru",
        "adding": "Menambahkan...",
        "close_form": "Tutup form tambah pengalaman",
        "add_success_title": "Berhasil",
        "add_success": "Pengalaman berhasil ditambahkan.",
        "add_error_title": "Gagal menambahkan pengalaman",
        "add_error": "Permintaan gagal. Silakan coba lagi.",
        "connection_error": "Tidak dapat terhubung ke server. Silakan coba lagi.",
        "permission_denied": "Hanya pemilik portofolio yang dapat menambah pengalaman.",
        "request_rejected": "Permintaan ditolak. Muat ulang halaman dan periksa hak aksesmu.",
        "edit_experience": "Edit Pengalaman",
        "delete_experience": "Hapus Pengalaman",
        "delete_title": "Hapus pengalaman?",
        "delete_prompt": "Apakah kamu yakin ingin menghapus",
        "cancel": "Batal",
        "confirm_delete": "Ya, hapus",
        "star": "Beri Star",
        "unstar": "Batalkan Star",
        "starred_by": "Diberi star oleh",
        "first_star": "Jadilah yang pertama memberi star pada pengalaman ini",
        "present": "sekarang",
        "search": "Cari",
        "search_placeholder": "Cari berdasarkan posisi atau organisasi",
        "no_results": "Tidak ada pengalaman yang sesuai dengan pencarianmu.",
        "loading": "Memuat pengalaman...",
        "load_error": "Gagal memuat pengalaman. Silakan coba lagi.",
        "retry": "Coba lagi",
        "empty_state": "Belum ada pengalaman yang ditambahkan.",
    },
}

SKILL_COPY = {
    "en": {
        "language": "en",
        "page_title": "Skills",
        "meta_description": "Technical skills of Maximus Quinn Hertada.",
        "experience": "Experience",
        "skills": "Skills",
        "projects": "Projects",
        "achievements": "Achievements",
        "switch_label": "ID",
        "eyebrow": "Portfolio / Skills",
        "intro": "Languages and tools I use to turn ideas into working software.",
        "filter_all": "All",
        "filter_language": "Languages",
        "filter_tool": "Tools",
        "filter_backend": "Backend",
        "filter_frontend": "Frontend",
        "empty_state": "No skills have been added yet.",
    },
    "id": {
        "language": "id",
        "page_title": "Keahlian",
        "meta_description": "Keahlian teknis Maximus Quinn Hertada.",
        "experience": "Pengalaman",
        "skills": "Keahlian",
        "projects": "Proyek",
        "achievements": "Prestasi",
        "switch_label": "EN",
        "eyebrow": "Portofolio / Keahlian",
        "intro": "Bahasa dan alat yang saya gunakan untuk mewujudkan ide menjadi perangkat lunak.",
        "filter_all": "Semua",
        "filter_language": "Bahasa Pemrograman",
        "filter_tool": "Alat",
        "filter_backend": "Backend",
        "filter_frontend": "Frontend",
        "empty_state": "Belum ada keahlian yang ditambahkan.",
    },
}

ACHIEVEMENT_COPY = {
    "en": {
        "language": "en",
        "page_title": "Achievements",
        "meta_description": "Achievements of Maximus Quinn Hertada.",
        "experience": "Experience",
        "skills": "Skills",
        "projects": "Projects",
        "achievements": "Achievements",
        "switch_label": "ID",
        "eyebrow": "Portfolio / Achievements",
        "intro": "Milestones from academic competitions and continuous learning.",
        "add_achievement": "Add Achievement",
        "add_heading": "Add New Achievement",
        "adding": "Adding...",
        "close_form": "Close add achievement form",
        "add_success_title": "Success",
        "add_success": "Achievement added successfully.",
        "add_error_title": "Could not add achievement",
        "add_error": "The request failed. Please try again.",
        "connection_error": "Could not reach the server. Please try again.",
        "permission_denied": "Only the portfolio owner can add achievements.",
        "request_rejected": "Request rejected. Refresh the page and check your access.",
        "form_labels": {
            "title": "Achievement (English)",
            "title_id": "Achievement (Indonesian)",
            "result": "Result (English)",
            "result_id": "Result (Indonesian)",
            "category": "Category",
            "year": "Year",
            "display_order": "Display order",
        },
        "edit_achievement": "Edit Achievement",
        "delete_achievement": "Delete Achievement",
        "delete_title": "Delete achievement?",
        "delete_prompt": "Are you sure you want to delete",
        "cancel": "Cancel",
        "confirm_delete": "Yes, delete",
        "star": "Star",
        "unstar": "Unstar",
        "starred_by": "Starred by",
        "first_star": "Be the first to star this achievement",
        "search_placeholder": "Search achievement titles or results...",
        "search": "Search",
        "no_results": "No achievements match your search.",
        "loading": "Loading achievements...",
        "load_error": "Failed to load achievements. Please try again.",
        "retry": "Try again",
        "empty_state": "No achievements have been added yet.",
    },
    "id": {
        "language": "id",
        "page_title": "Prestasi",
        "meta_description": "Prestasi Maximus Quinn Hertada.",
        "experience": "Pengalaman",
        "skills": "Keahlian",
        "projects": "Proyek",
        "achievements": "Prestasi",
        "switch_label": "EN",
        "eyebrow": "Portofolio / Prestasi",
        "intro": "Pencapaian dari kompetisi akademik dan proses belajar berkelanjutan.",
        "add_achievement": "Tambah Prestasi",
        "add_heading": "Tambah Prestasi Baru",
        "adding": "Menambahkan...",
        "close_form": "Tutup form tambah prestasi",
        "add_success_title": "Berhasil",
        "add_success": "Prestasi berhasil ditambahkan.",
        "add_error_title": "Gagal menambahkan prestasi",
        "add_error": "Permintaan gagal. Silakan coba lagi.",
        "connection_error": "Tidak dapat terhubung ke server. Silakan coba lagi.",
        "permission_denied": "Hanya pemilik portofolio yang dapat menambah prestasi.",
        "request_rejected": "Permintaan ditolak. Muat ulang halaman dan periksa hak aksesmu.",
        "edit_achievement": "Edit Prestasi",
        "delete_achievement": "Hapus Prestasi",
        "delete_title": "Hapus prestasi?",
        "delete_prompt": "Apakah kamu yakin ingin menghapus",
        "cancel": "Batal",
        "confirm_delete": "Ya, hapus",
        "star": "Beri Star",
        "unstar": "Batalkan Star",
        "starred_by": "Diberi star oleh",
        "first_star": "Jadilah yang pertama memberi star pada prestasi ini",
        "search_placeholder": "Cari judul atau hasil prestasi...",
        "search": "Cari",
        "no_results": "Tidak ada prestasi yang cocok dengan pencarianmu.",
        "loading": "Memuat prestasi...",
        "load_error": "Gagal memuat prestasi. Silakan coba lagi.",
        "retry": "Coba lagi",
        "empty_state": "Belum ada prestasi yang ditambahkan.",
    },
}

def is_editor(user):
    return user.is_authenticated and user.groups.filter(name="Editor").exists()

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "MaxKwen",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        response = redirect("landing_page")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "MaxKwen",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("landing_page")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
@require_POST
def toggle_project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.user in project.starred_by.all():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)

    return redirect("main:show_projects")

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


def show_projects(request, language="en"):
    title_query = request.GET.get("title", "").strip()
    context = {
        "copy": PROJECT_COPY[language],
        "title_query": title_query,
        "is_editor": is_editor(request.user),
        "form": ProjectForm(),
    }
    return render(request, "projects.html", context)

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
    return render(request, "projects_form.html", context)


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
    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")
@require_POST
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    messages.success(request, "Proyek berhasil dihapus!")
    return redirect("main:show_projects")


def get_experiences_json(request):
    search_query = request.GET.get("q", "").strip()
    experiences = Experience.objects.prefetch_related("starred_by").order_by(
        "-start_year", "id"
    )
    if search_query:
        experiences = experiences.filter(
            Q(title__icontains=search_query)
            | Q(title_id__icontains=search_query)
            | Q(organization__icontains=search_query)
            | Q(organization_id__icontains=search_query)
        )

    can_update = request.user.is_superuser or is_editor(request.user)
    data = []
    for experience in experiences:
        starred_users = list(experience.starred_by.all())
        data.append(
            {
                "model": "main.experience",
                "pk": experience.pk,
                "fields": {
                    "title": experience.title,
                    "title_id": experience.title_id,
                    "organization": experience.organization,
                    "organization_id": experience.organization_id,
                    "description": experience.description,
                    "description_id": experience.description_id,
                    "category": experience.category,
                    "start_year": experience.start_year,
                    "end_year": experience.end_year,
                    "starred_by": [[user.username] for user in starred_users],
                    "star_count": len(starred_users),
                    "is_starred": request.user.is_authenticated
                    and any(user.pk == request.user.pk for user in starred_users),
                    "starred_by_names": ", ".join(
                        user.username for user in starred_users
                    ),
                    "can_update": can_update,
                    "can_delete": request.user.is_superuser,
                    "update_url": reverse(
                        "main:update_experience", args=[experience.pk]
                    ),
                    "delete_url": reverse(
                        "main:delete_experience", args=[experience.pk]
                    ),
                    "star_url": reverse(
                        "main:toggle_experience_star", args=[experience.pk]
                    ),
                },
            }
        )

    return JsonResponse(data, safe=False)


def show_experiences(request, language="en"):
    context = {
        "copy": EXPERIENCE_COPY[language],
        "search_query": request.GET.get("q", "").strip(),
        "is_editor": is_editor(request.user),
    }
    if request.user.is_superuser:
        form = ExperienceForm()
        for name, label in EXPERIENCE_COPY[language].get("form_labels", {}).items():
            form.fields[name].label = label
        for name, field in form.fields.items():
            field.widget.attrs["aria-describedby"] = f"experience-error-{name}"
        form.fields["title"].widget.attrs["autofocus"] = True
        context["form"] = form
    return render(request, "experiences.html", context)


@login_required(login_url="/login/")
@require_POST
def toggle_experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.user in experience.starred_by.all():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)

    return redirect("main:show_experiences")


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experiences")

    context = {
        "copy": EXPERIENCE_COPY["en"],
        "form": form,
        "form_title": "Add Experience",
        "form_eyebrow": "Portfolio / Experience",
        "form_heading": "Add Experience",
        "form_intro": "Add a role or organization to your portfolio.",
        "submit_label": "Tambah Pengalaman",
    }
    return render(request, "experiences_form.html", context)


@require_POST
def create_experience_ajax(request):
    language = request.POST.get("language", "en")
    copy = EXPERIENCE_COPY.get(language, EXPERIENCE_COPY["en"])
    if not request.user.is_superuser:
        return JsonResponse({"message": copy["permission_denied"]}, status=403)

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": copy["add_success"], "pk": experience.pk}, status=201
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not request.user.is_superuser and not is_editor(request.user):
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experiences")

    context = {
        "copy": EXPERIENCE_COPY["en"],
        "form": form,
        "form_title": "Update Experience",
        "form_eyebrow": "Portfolio / Experience",
        "form_heading": "Update Experience",
        "form_intro": "Update this experience in your portfolio.",
        "submit_label": "Simpan Perubahan",
    }
    return render(request, "experiences_form.html", context)


@login_required(login_url="/login/")
@require_POST
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)
    experience.delete()
    messages.success(request, "Pengalaman berhasil dihapus!")
    return redirect("main:show_experiences")


def show_skills(request, language="en"):
    context = {"copy": SKILL_COPY[language], "skill_list": Skill.objects.all()}
    return render(request, "skills.html", context)


def get_achievements_json(request):
    search_query = request.GET.get("q", "").strip()
    achievements = Achievement.objects.prefetch_related("starred_by")
    if search_query:
        achievements = achievements.filter(
            Q(title__icontains=search_query)
            | Q(title_id__icontains=search_query)
            | Q(result__icontains=search_query)
            | Q(result_id__icontains=search_query)
        )

    can_update = request.user.is_superuser or is_editor(request.user)
    data = []
    for achievement in achievements:
        starred_users = list(achievement.starred_by.all())
        data.append(
            {
                "model": "main.achievement",
                "pk": achievement.pk,
                "fields": {
                    "title": achievement.title,
                    "title_id": achievement.title_id,
                    "result": achievement.result,
                    "result_id": achievement.result_id,
                    "category": achievement.category,
                    "year": achievement.year,
                    "display_order": achievement.display_order,
                    "starred_by": [[user.username] for user in starred_users],
                    "star_count": len(starred_users),
                    "is_starred": request.user.is_authenticated
                    and any(user.pk == request.user.pk for user in starred_users),
                    "starred_by_names": ", ".join(
                        user.username for user in starred_users
                    ),
                    "can_update": can_update,
                    "can_delete": request.user.is_superuser,
                    "update_url": reverse(
                        "main:update_achievement", args=[achievement.pk]
                    ),
                    "delete_url": reverse(
                        "main:delete_achievement", args=[achievement.pk]
                    ),
                    "star_url": reverse(
                        "main:toggle_achievement_star", args=[achievement.pk]
                    ),
                },
            }
        )

    return JsonResponse(data, safe=False)


def show_achievements(request, language="en"):
    context = {
        "copy": ACHIEVEMENT_COPY[language],
        "search_query": request.GET.get("q", "").strip(),
        "is_editor": is_editor(request.user),
    }
    if request.user.is_superuser:
        form = AchievementForm()
        for name, label in ACHIEVEMENT_COPY[language].get("form_labels", {}).items():
            form.fields[name].label = label
        for name, field in form.fields.items():
            field.widget.attrs["aria-describedby"] = f"achievement-error-{name}"
        form.fields["title"].widget.attrs["autofocus"] = True
        context["form"] = form
    return render(request, "achievements.html", context)


@require_POST
def create_achievement_ajax(request):
    language = request.POST.get("language", "en")
    copy = ACHIEVEMENT_COPY.get(language, ACHIEVEMENT_COPY["en"])
    if not request.user.is_superuser:
        return JsonResponse({"message": copy["permission_denied"]}, status=403)

    form = AchievementForm(request.POST)
    if form.is_valid():
        achievement = form.save()
        return JsonResponse(
            {"message": copy["add_success"], "pk": achievement.pk}, status=201
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
@require_POST
def toggle_achievement_star(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)

    if request.user in achievement.starred_by.all():
        achievement.starred_by.remove(request.user)
    else:
        achievement.starred_by.add(request.user)

    return redirect("main:show_achievements")


@login_required(login_url="/login/")
def create_achievement(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = AchievementForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Prestasi baru berhasil ditambahkan!")
        return redirect("main:show_achievements")

    context = {
        "copy": ACHIEVEMENT_COPY["en"],
        "form": form,
        "form_title": "Add Achievement",
        "form_eyebrow": "Portfolio / Achievements",
        "form_heading": "Add Achievement",
        "form_intro": "Add an achievement to your portfolio.",
        "submit_label": "Tambah Prestasi",
    }
    return render(request, "achievements_form.html", context)


@login_required(login_url="/login/")
def update_achievement(request, achievement_id):
    if not request.user.is_superuser and not is_editor(request.user):
        raise PermissionDenied
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    form = AchievementForm(request.POST or None, instance=achievement)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Prestasi berhasil diperbarui!")
        return redirect("main:show_achievements")

    context = {
        "copy": ACHIEVEMENT_COPY["en"],
        "form": form,
        "form_title": "Update Achievement",
        "form_eyebrow": "Portfolio / Achievements",
        "form_heading": "Update Achievement",
        "form_intro": "Update this achievement in your portfolio.",
        "submit_label": "Simpan Perubahan",
    }
    return render(request, "achievements_form.html", context)


@login_required(login_url="/login/")
@require_POST
def delete_achievement(request, achievement_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    achievement.delete()
    messages.success(request, "Prestasi berhasil dihapus!")
    return redirect("main:show_achievements")

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
