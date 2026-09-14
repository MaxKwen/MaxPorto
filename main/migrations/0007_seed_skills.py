from django.db import migrations


SKILLS = [
    ("C", "language", "img/c.png"),
    ("C++", "language", "img/c++.png"),
    ("Java", "language", "img/java.png"),
    ("Python", "language", "img/python.png"),
    ("JavaScript", "language", "img/js.png"),
    ("Git", "tool", "img/git.png"),
    ("GitHub", "tool", "img/github.png"),
    ("Jupyter Notebook", "tool", "img/jupyter.png"),
    ("Visual Studio Code", "tool", "img/vscode.png"),
    ("Django", "backend", "img/django.png"),
    ("HTML", "frontend", "img/html.png"),
    ("CSS", "frontend", "img/css.png"),
]


def seed_skills(apps, schema_editor):
    Skill = apps.get_model("main", "Skill")
    Skill.objects.bulk_create(
        Skill(name=name, category=category, icon=icon, display_order=order)
        for order, (name, category, icon) in enumerate(SKILLS, start=1)
    )


def remove_seeded_skills(apps, schema_editor):
    Skill = apps.get_model("main", "Skill")
    Skill.objects.filter(name__in=[skill[0] for skill in SKILLS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0006_skill"),
    ]

    operations = [
        migrations.RunPython(seed_skills, remove_seeded_skills),
    ]
