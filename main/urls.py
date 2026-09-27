from django.urls import path

from main.views import (
    create_achievement,
    create_experience,
    create_project,
    delete_achievement,
    delete_experience,
    delete_project,
    get_achievements_json,
    get_experiences_json,
    get_projects_json,
    show_achievements,
    show_experiences,
    show_projects,
    show_skills,
    update_achievement,
    update_experience,
    update_project,
    register,
    login_user,
    logout_user,
    toggle_star,
)

app_name = "main"

urlpatterns = [
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path(
        "api/experiences/",
        get_experiences_json,
        name="get_experiences_json",
    ),
    path(
        "api/achievements/",
        get_achievements_json,
        name="get_achievements_json",
    ),
    path("experience/", show_experiences, name="show_experiences"),
    path("experience/add/", create_experience, name="create_experience"),
    path(
        "experience/<int:experience_id>/edit/",
        update_experience,
        name="update_experience",
    ),
    path(
        "experience/<int:experience_id>/delete/",
        delete_experience,
        name="delete_experience",
    ),
    path(
        "id/experience/",
        show_experiences,
        {"language": "id"},
        name="show_experiences_id",
    ),
    path("achievements/", show_achievements, name="show_achievements"),
    path(
        "achievements/add/",
        create_achievement,
        name="create_achievement",
    ),
    path(
        "achievements/<int:achievement_id>/edit/",
        update_achievement,
        name="update_achievement",
    ),
    path(
        "achievements/<int:achievement_id>/delete/",
        delete_achievement,
        name="delete_achievement",
    ),
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
        "projects/<int:project_id>/edit/",
        update_project,
        name="update_project",
    ),
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
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path(
        "projects/<int:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),
]
