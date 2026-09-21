from django.urls import path

from main.views import (
    create_project,
    delete_project,
    get_projects_json,
    show_achievements,
    show_experiences,
    show_projects,
    show_skills,
)

app_name = "main"

urlpatterns = [
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("experience/", show_experiences, name="show_experiences"),
    path(
        "id/experience/",
        show_experiences,
        {"language": "id"},
        name="show_experiences_id",
    ),
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
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path(
        "projects/<int:project_id>/delete/",
        delete_project,
        name="delete_project",
    ),
    path(
        "id/projects/",
        show_projects,
        {"language": "id"},
        name="show_projects_id",
    ),
]
