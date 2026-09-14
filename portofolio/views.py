from django.shortcuts import render


COPY = {
    "en": {
        "language": "en",
        "switch_label": "ID",
        "switch_url": "/id/",
        "portfolio": "Professional portfolio",
        "role": "TA & Undergraduate CS Student @ University of Indonesia | Data Scientist Enthusiast",
        "experience": "Experience",
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
        "skills": "Skills",
        "project": "Project",
        "achievements": "Achievements",
    },
}


def landing_page(request, language="en"):
    return render(
        request,
        "index.html",
        {"copy": COPY[language]},
    )
