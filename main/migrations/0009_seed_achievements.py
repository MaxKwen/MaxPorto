from django.db import migrations


ACHIEVEMENTS = [
    {
        "title": "OSN Informatics",
        "title_id": "Informatika OSN",
        "result": "National finalist",
        "result_id": "Finalis nasional",
        "category": "Competition",
        "year": None,
        "display_order": 1,
    },
    {
        "title": "AMO",
        "title_id": "AMO",
        "result": "Bronze medal",
        "result_id": "Medali perunggu",
        "category": "Competition",
        "year": None,
        "display_order": 2,
    },
]


def seed_achievements(apps, schema_editor):
    Achievement = apps.get_model("main", "Achievement")
    Achievement.objects.bulk_create(
        Achievement(**achievement) for achievement in ACHIEVEMENTS
    )


def remove_seeded_achievements(apps, schema_editor):
    Achievement = apps.get_model("main", "Achievement")
    Achievement.objects.filter(
        title__in=[achievement["title"] for achievement in ACHIEVEMENTS]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0008_achievement"),
    ]

    operations = [
        migrations.RunPython(seed_achievements, remove_seeded_achievements),
    ]
