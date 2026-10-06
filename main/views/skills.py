"""Halaman katalog keahlian yang dirender dari model."""

from django.shortcuts import render

from main.copy import SKILL_COPY
from main.models import Skill


# Halaman HTML
def show_skills(request, language="en"):
    context = {"copy": SKILL_COPY[language], "skill_list": Skill.objects.all()}
    return render(request, "skills/list.html", context)
