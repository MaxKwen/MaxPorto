from django.urls import path

from main.views import show_projects

app_name = "main"

urlpatterns = [
    path("projects/", show_projects, name="show_projects"),
]
