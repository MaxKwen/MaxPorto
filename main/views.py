from django.shortcuts import render

from main.models import Project


def show_projects(request):
    context = {
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)
