from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "nama": "Maximus Quinn Hertada",
        "npm": "2506613552",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "nama": "Maximus Quinn Hertada",
        "experience_list": Experience.objects.all(),
        "switch_label": "ID",
        "switch_url": "/id/",
    }
    return render(request, "experience.html", context)
