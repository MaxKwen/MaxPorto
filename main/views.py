from django.shortcuts import render

from main.models import Project


PROJECT_COPY = {
    "en": {
        "language": "en",
        "page_title": "Projects",
        "meta_description": "Projects by Maximus Quinn Hertada.",
        "experience": "Experience",
        "skills": "Skills",
        "projects": "Projects",
        "achievements": "Achievements",
        "contact": "Contact",
        "switch_label": "ID",
        "eyebrow": "Portfolio / Projects",
        "featured": "Featured project",
        "view_project": "View project",
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
        "contact": "Kontak",
        "switch_label": "EN",
        "eyebrow": "Portofolio / Proyek",
        "featured": "Proyek unggulan",
        "view_project": "Lihat proyek",
        "empty_state": "Belum ada proyek yang ditambahkan.",
    },
}


def show_projects(request, language="en"):
    context = {
        "copy": PROJECT_COPY[language],
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)
