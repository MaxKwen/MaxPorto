from django.urls import path

from main.views import show_experiences, show_projects

app_name = "main"

urlpatterns = [
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
