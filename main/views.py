from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.forms import AchievementForm, ExperienceForm, ProjectForm
from main.models import Achievement, Experience, Project, Skill


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
        "edit_experience": "Edit Experience",
        "delete_experience": "Delete Experience",
        "delete_title": "Delete experience?",
        "delete_prompt": "Are you sure you want to delete",
        "cancel": "Cancel",
        "confirm_delete": "Yes, delete",
        "present": "present",
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
        "edit_experience": "Edit Pengalaman",
        "delete_experience": "Hapus Pengalaman",
        "delete_title": "Hapus pengalaman?",
        "delete_prompt": "Apakah kamu yakin ingin menghapus",
        "cancel": "Batal",
        "confirm_delete": "Ya, hapus",
        "present": "sekarang",
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
        "edit_achievement": "Edit Achievement",
        "delete_achievement": "Delete Achievement",
        "delete_title": "Delete achievement?",
        "delete_prompt": "Are you sure you want to delete",
        "cancel": "Cancel",
        "confirm_delete": "Yes, delete",
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
        "edit_achievement": "Edit Prestasi",
        "delete_achievement": "Hapus Prestasi",
        "delete_title": "Hapus prestasi?",
        "delete_prompt": "Apakah kamu yakin ingin menghapus",
        "cancel": "Batal",
        "confirm_delete": "Ya, hapus",
        "empty_state": "Belum ada prestasi yang ditambahkan.",
    },
}


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")


def show_projects(request, language="en"):
    json_response = get_projects_json(request)
    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()
    context = {
        "copy": PROJECT_COPY[language],
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)


def create_project(request):
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


def update_project(request, project_id):
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


@require_POST
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    messages.success(request, "Proyek berhasil dihapus!")
    return redirect("main:show_projects")


def show_experiences(request, language="en"):
    context = {
        "copy": EXPERIENCE_COPY[language],
        "experience_list": Experience.objects.order_by("-start_year", "id"),
    }
    return render(request, "experiences.html", context)


def create_experience(request):
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


def update_experience(request, experience_id):
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


@require_POST
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    experience.delete()
    messages.success(request, "Pengalaman berhasil dihapus!")
    return redirect("main:show_experiences")


def show_skills(request, language="en"):
    context = {"copy": SKILL_COPY[language], "skill_list": Skill.objects.all()}
    return render(request, "skills.html", context)


def show_achievements(request, language="en"):
    context = {
        "copy": ACHIEVEMENT_COPY[language],
        "achievement_list": Achievement.objects.all(),
    }
    return render(request, "achievements.html", context)


def create_achievement(request):
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


def update_achievement(request, achievement_id):
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


@require_POST
def delete_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    achievement.delete()
    messages.success(request, "Prestasi berhasil dihapus!")
    return redirect("main:show_achievements")
