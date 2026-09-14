from django.shortcuts import render

from main.models import Experience


COPY = {
    "en": {
        "language": "en",
        "switch_label": "ID",
        "switch_url": "/id/",
        "portfolio": "Professional portfolio",
        "role": "TA & Undergraduate CS Student @ University of Indonesia | Data Scientist Enthusiast",
        "experience": "Experience",
        "experience_empty": "No experience has been added yet.",
        "present": "present",
        "skills": "Skills",
        "project": "Project",
        "achievements": "Achievements",
    },
    "id": {
        "language": "id",
        "switch_label": "EN",
        "switch_url": "/",
        "portfolio": "Portofolio profesional",
        "role": "Asisten Pengajar & Mahasiswa S1 Ilmu Komputer UI | Penggemar Data Science",
        "experience": "Pengalaman",
        "experience_empty": "Belum ada pengalaman yang ditambahkan.",
        "present": "sekarang",
        "skills": "Skills",
        "project": "Project",
        "achievements": "Achievements",
    },
}


def landing_page(request, language="en"):
    return render(
        request,
        "index.html",
        {
            "copy": COPY[language],
            "experience_list": Experience.objects.order_by("-start_year", "id"),
        },
    )
