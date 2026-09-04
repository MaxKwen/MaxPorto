from django.shortcuts import render


COPY = {
    "en": {
        "language": "en",
        "switch_label": "ID",
        "switch_url": "/id/",
        "portfolio": "Professional portfolio",
        "role": "Data Science Enthusiast",
        "intro": "Exploring thoughtful solutions at the intersection of data, security, and technology.",
        "experience": "Experience",
        "experience_text": "Organization, internship, and committee experience will be added here.",
        "education": "Education",
        "education_text": "Education history and relevant learning journey will be added here.",
        "project": "Project",
        "project_text": "A Django backend project replicating core X.com interactions: authentication, posts, replies, and likes.",
        "achievements": "Achievements",
        "contact": "Let’s connect.",
        "contact_text": "Open to professional conversations and collaboration.",
        "github": "View on GitHub",
        "contact_button": "Contact Me",
    },
    "id": {
        "language": "id",
        "switch_label": "EN",
        "switch_url": "/",
        "portfolio": "Portofolio profesional",
        "role": "Penggemar Data Science",
        "intro": "Mengeksplorasi solusi yang terarah di persimpangan data, keamanan, dan teknologi.",
        "experience": "Pengalaman",
        "experience_text": "Pengalaman organisasi, magang, dan kepanitiaan akan ditambahkan di sini.",
        "education": "Pendidikan",
        "education_text": "Riwayat pendidikan dan perjalanan belajar akan ditambahkan di sini.",
        "project": "Proyek",
        "project_text": "Proyek backend Django yang mereplikasi interaksi inti X.com: autentikasi, post, balasan, dan suka.",
        "achievements": "Prestasi",
        "contact": "Mari terhubung.",
        "contact_text": "Terbuka untuk percakapan profesional dan kolaborasi.",
        "github": "Lihat di GitHub",
        "contact_button": "Hubungi Saya",
    },
}


def landing_page(request, language="en"):
    return render(
        request,
        "index.html",
        {"copy": COPY[language]},
    )
