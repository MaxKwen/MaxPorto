from django.db import migrations


PROJECTS = [
    {
        "title": "Kusut-Kusut",
        "description": (
            "A Django backend project replicating core X.com interactions: "
            "authentication, posts, replies, and likes."
        ),
        "title_id": "Kusut-Kusut",
        "description_id": (
            "Proyek backend Django yang mereplikasi interaksi inti X.com: "
            "authentication, post, reply, dan like."
        ),
        "category": "Backend / Django",
        "project_url": "https://github.com/MaxKwen/kusutkusut-backend",
        "thumbnail": "",
        "is_featured": True,
    },
    {
        "title": "STUMO Wristband",
        "description": (
            "A Wi-Fi-enabled bracelet that transmits student temperature, "
            "heart rate, and oxygen data to health officers in real time."
        ),
        "title_id": "STUMO Wristband",
        "description_id": (
            "Gelang berbasis Wi-Fi yang mengirim data suhu tubuh, detak "
            "jantung, dan oksigen siswa kepada petugas kesehatan secara real time."
        ),
        "category": "IoT / Health Technology",
        "project_url": "",
        "thumbnail": "",
        "is_featured": True,
    },
    {
        "title": "Cellulose Acetate Membrane Research",
        "description": (
            "Research on eco-friendly CO2 adsorbents with BRIN mentorship, "
            "including analysis of glycerol's effect on air-purification efficiency."
        ),
        "title_id": "Riset Membran Selulosa Asetat",
        "description_id": (
            "Riset adsorben CO2 ramah lingkungan dengan bimbingan BRIN, "
            "termasuk analisis pengaruh gliserol terhadap efisiensi pemurnian udara."
        ),
        "category": "Data Analysis / Research",
        "project_url": "https://pubmed.ncbi.nlm.nih.gov/38286141/",
        "thumbnail": "",
        "is_featured": True,
    },
]


def add_projects(apps, schema_editor):
    project = apps.get_model("main", "Project")
    project.objects.bulk_create(project(**data) for data in PROJECTS)


def remove_projects(apps, schema_editor):
    project = apps.get_model("main", "Project")
    project.objects.filter(
        title__in=[data["title"] for data in PROJECTS]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_project_description_id_project_title_id"),
    ]

    operations = [
        migrations.RunPython(add_projects, remove_projects),
    ]
