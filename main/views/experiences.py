"""Halaman, API JSON, CRUD, dan star pengalaman."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from main.copy import EXPERIENCE_COPY
from main.forms import ExperienceForm
from main.models import Experience
from main.permissions import is_editor


# Halaman HTML
def show_experiences(request, language="en"):
    context = {
        "copy": EXPERIENCE_COPY[language],
        "search_query": request.GET.get("q", "").strip(),
        "is_editor": is_editor(request.user),
    }
    if request.user.is_superuser:
        form = ExperienceForm()
        for name, label in EXPERIENCE_COPY[language].get("form_labels", {}).items():
            form.fields[name].label = label
        for name, field in form.fields.items():
            field.widget.attrs["aria-describedby"] = f"experience-error-{name}"
        form.fields["title"].widget.attrs["autofocus"] = True
        context["form"] = form
    return render(request, "experiences/list.html", context)


# API JSON untuk daftar dan pencarian AJAX
def get_experiences_json(request):
    search_query = request.GET.get("q", "").strip()
    experiences = Experience.objects.prefetch_related("starred_by").order_by(
        "-start_year", "id"
    )
    if search_query:
        experiences = experiences.filter(
            Q(title__icontains=search_query)
            | Q(title_id__icontains=search_query)
            | Q(organization__icontains=search_query)
            | Q(organization_id__icontains=search_query)
        )

    can_update = request.user.is_superuser or is_editor(request.user)
    data = []
    for experience in experiences:
        starred_users = list(experience.starred_by.all())
        data.append(
            {
                "model": "main.experience",
                "pk": experience.pk,
                "fields": {
                    "title": experience.title,
                    "title_id": experience.title_id,
                    "organization": experience.organization,
                    "organization_id": experience.organization_id,
                    "description": experience.description,
                    "description_id": experience.description_id,
                    "category": experience.category,
                    "start_year": experience.start_year,
                    "end_year": experience.end_year,
                    "starred_by": [[user.username] for user in starred_users],
                    "star_count": len(starred_users),
                    "is_starred": request.user.is_authenticated
                    and any(user.pk == request.user.pk for user in starred_users),
                    "starred_by_names": ", ".join(
                        user.username for user in starred_users
                    ),
                    "can_update": can_update,
                    "can_delete": request.user.is_superuser,
                    "update_url": reverse(
                        "main:update_experience", args=[experience.pk]
                    ),
                    "delete_url": reverse(
                        "main:delete_experience", args=[experience.pk]
                    ),
                    "star_url": reverse(
                        "main:toggle_experience_star", args=[experience.pk]
                    ),
                },
            }
        )

    return JsonResponse(data, safe=False)


# Tambah melalui form halaman
@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experiences")

    context = {
        "copy": EXPERIENCE_COPY["en"],
        "form": form,
        "form_title": "Add Experience",
        "form_eyebrow": "Portfolio / Experience",
        "form_heading": "Add Experience",
        "form_intro": "Add a role or organization to your portfolio.",
        "submit_label": "Tambah Pengalaman",
    }
    return render(request, "experiences/form.html", context)


# Tambah melalui modal AJAX
@require_POST
def create_experience_ajax(request):
    language = request.POST.get("language", "en")
    copy = EXPERIENCE_COPY.get(language, EXPERIENCE_COPY["en"])
    if not request.user.is_superuser:
        return JsonResponse({"message": copy["permission_denied"]}, status=403)

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": copy["add_success"], "pk": experience.pk}, status=201
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


# Edit melalui form halaman
@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not request.user.is_superuser and not is_editor(request.user):
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experiences")

    context = {
        "copy": EXPERIENCE_COPY["en"],
        "form": form,
        "form_title": "Update Experience",
        "form_eyebrow": "Portfolio / Experience",
        "form_heading": "Update Experience",
        "form_intro": "Update this experience in your portfolio.",
        "submit_label": "Simpan Perubahan",
    }
    return render(request, "experiences/form.html", context)


# Hapus melalui POST
@login_required(login_url="/login/")
@require_POST
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)
    experience.delete()
    messages.success(request, "Pengalaman berhasil dihapus!")
    return redirect("main:show_experiences")


# Toggle star untuk pengguna login
@login_required(login_url="/login/")
@require_POST
def toggle_experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.user in experience.starred_by.all():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)

    return redirect("main:show_experiences")
