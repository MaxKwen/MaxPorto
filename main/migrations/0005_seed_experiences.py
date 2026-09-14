from django.db import migrations


EXPERIENCES = [
    {
        "title": "Teaching Assistant, Intro to Digital System",
        "title_id": "Asisten Pengajar, Sistem Digital Dasar",
        "organization": "Faculty of Computer Science, University of Indonesia",
        "organization_id": "Fakultas Ilmu Komputer, Universitas Indonesia",
        "description": (
            "Designed laboratory problems, led tutorials, supervised practical "
            "sessions, and evaluated weekly work."
        ),
        "description_id": (
            "Menyusun soal laboratorium, memimpin tutorial, mengawasi sesi "
            "praktikum, dan mengevaluasi tugas mingguan."
        ),
        "category": "Teaching",
        "start_year": 2026,
        "end_year": None,
    },
    {
        "title": "Staff, Data Science Academy",
        "title_id": "Staf, Data Science Academy",
        "organization": "COMPFEST, University of Indonesia",
        "organization_id": "COMPFEST, Universitas Indonesia",
        "description": (
            "Coordinated industry speakers and mentors, technical documentation, "
            "and candidate screening for participating teams."
        ),
        "description_id": (
            "Mengoordinasikan pembicara dan mentor industri, dokumentasi teknis, "
            "serta seleksi kandidat untuk tim peserta."
        ),
        "category": "Organization",
        "start_year": 2026,
        "end_year": None,
    },
]


def seed_experiences(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")
    Experience.objects.bulk_create(Experience(**data) for data in EXPERIENCES)


def remove_seeded_experiences(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")
    Experience.objects.filter(
        title__in=[experience["title"] for experience in EXPERIENCES]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_experience"),
    ]

    operations = [
        migrations.RunPython(seed_experiences, remove_seeded_experiences),
    ]
