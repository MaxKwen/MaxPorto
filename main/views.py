from django.shortcuts import render

from main.models import Experience, Project, Skill


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
        "intro": "Selected work across software, connected devices, and applied research.",
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
        "intro": "Karya pilihan dalam perangkat lunak, perangkat terhubung, dan riset terapan.",
        "featured": "Proyek unggulan",
        "view_project": "Lihat proyek",
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
        "contact": "Contact",
        "switch_label": "ID",
        "eyebrow": "Portfolio / Experience",
        "intro": "Roles where I contribute through teaching, collaboration, and technical work.",
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
        "contact": "Kontak",
        "switch_label": "EN",
        "eyebrow": "Portofolio / Pengalaman",
        "intro": "Peran tempat saya berkontribusi melalui pengajaran, kolaborasi, dan pekerjaan teknis.",
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
        "contact": "Contact",
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
        "contact": "Kontak",
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


def show_projects(request, language="en"):
    context = {
        "copy": PROJECT_COPY[language],
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)


def show_experiences(request, language="en"):
    context = {
        "copy": EXPERIENCE_COPY[language],
        "experience_list": Experience.objects.order_by("-start_year", "id"),
    }
    return render(request, "experiences.html", context)


def show_skills(request, language="en"):
    context = {"copy": SKILL_COPY[language], "skill_list": Skill.objects.all()}
    return render(request, "skills.html", context)
