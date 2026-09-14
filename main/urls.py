from django.urls import path

from main.views import show_achievements, show_experiences, show_projects, show_skills

app_name = "main"

urlpatterns = [
    path("achievements/", show_achievements, name="show_achievements"),
    path(
        "id/achievements/",
        show_achievements,
        {"language": "id"},
        name="show_achievements_id",
    ),
    path("skills/", show_skills, name="show_skills"),
    path(
        "id/skills/",
        show_skills,
        {"language": "id"},
        name="show_skills_id",
    ),
    path("experience/", show_experiences, name="show_experiences"),
    path(
        "id/experience/",
        show_experiences,
        {"language": "id"},
        name="show_experiences_id",
    ),
    path("projects/", show_projects, name="show_projects"),
    path(
        "id/projects/",
        show_projects,
        {"language": "id"},
        name="show_projects_id",
    ),
]
