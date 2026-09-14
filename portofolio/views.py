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
        "award_osn": "OSN Informatics",
        "award_osn_detail": "National finalist",
        "award_amo": "AMO",
        "award_amo_detail": "Bronze medal",
        "contact": "Let’s connect.",
        "contact_button": "Contact Me",
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
        "award_osn": "Informatika OSN",
        "award_osn_detail": "Finalis nasional",
        "award_amo": "AMO",
        "award_amo_detail": "Medali perunggu",
        "contact": "Contact",
        "contact_button": "Hubungi Saya",
    },
}


def landing_page(request, language="en"):
    return render(
        request,
        "index.html",
        {"copy": COPY[language]},
    )
