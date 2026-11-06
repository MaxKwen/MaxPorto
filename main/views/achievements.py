"""Halaman, API JSON, CRUD, dan star prestasi."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from main.copy import ACHIEVEMENT_COPY
from main.forms import AchievementForm
from main.models import Achievement
from main.permissions import is_editor


# Halaman HTML
def show_achievements(request, language="en"):
    context = {
        "copy": ACHIEVEMENT_COPY[language],
        "search_query": request.GET.get("q", "").strip(),
        "is_editor": is_editor(request.user),
    }
    # Modal dipakai pemilik (tambah/edit) dan Editor (edit saja)
    if request.user.is_superuser or context["is_editor"]:
        form = AchievementForm()
        for name, label in ACHIEVEMENT_COPY[language].get("form_labels", {}).items():
            form.fields[name].label = label
        for name, field in form.fields.items():
            field.widget.attrs["aria-describedby"] = f"achievement-error-{name}"
        form.fields["title"].widget.attrs["autofocus"] = True
        context["form"] = form
    return render(request, "achievements/list.html", context)


# API JSON untuk daftar dan pencarian AJAX
def get_achievements_json(request):
    search_query = request.GET.get("q", "").strip()
    achievements = Achievement.objects.prefetch_related("starred_by")
    if search_query:
        achievements = achievements.filter(
            Q(title__icontains=search_query)
            | Q(title_id__icontains=search_query)
            | Q(result__icontains=search_query)
            | Q(result_id__icontains=search_query)
        )

    can_update = request.user.is_superuser or is_editor(request.user)
    data = []
    for achievement in achievements:
        starred_users = list(achievement.starred_by.all())
        data.append(
            {
                "model": "main.achievement",
                "pk": achievement.pk,
                "fields": {
                    "title": achievement.title,
                    "title_id": achievement.title_id,
                    "result": achievement.result,
                    "result_id": achievement.result_id,
                    "category": achievement.category,
                    "year": achievement.year,
                    "display_order": achievement.display_order,
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
                        "main:update_achievement", args=[achievement.pk]
                    ),
                    "delete_url": reverse(
                        "main:delete_achievement", args=[achievement.pk]
                    ),
                    "star_url": reverse(
                        "main:toggle_achievement_star", args=[achievement.pk]
                    ),
                },
            }
        )

    return JsonResponse(data, safe=False)


# Tambah melalui form halaman
@login_required(login_url="/login/")
def create_achievement(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = AchievementForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Prestasi baru berhasil ditambahkan!")
        return redirect("main:show_achievements")

    context = {
        "copy": ACHIEVEMENT_COPY["en"],
        "form": form,
        "form_title": "Add Achievement",
        "form_eyebrow": "Portfolio / Achievements",
        "form_heading": "Add Achievement",
        "form_intro": "Add an achievement to your portfolio.",
        "submit_label": "Tambah Prestasi",
    }
    return render(request, "achievements/form.html", context)


# Tambah melalui modal AJAX
@require_POST
def create_achievement_ajax(request):
    language = request.POST.get("language", "en")
    copy = ACHIEVEMENT_COPY.get(language, ACHIEVEMENT_COPY["en"])
    if not request.user.is_superuser:
        return JsonResponse({"message": copy["permission_denied"]}, status=403)

    form = AchievementForm(request.POST)
    if form.is_valid():
        achievement = form.save()
        return JsonResponse(
            {"message": copy["add_success"], "pk": achievement.pk}, status=201
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


# Edit melalui form halaman
@login_required(login_url="/login/")
def update_achievement(request, achievement_id):
    if not request.user.is_superuser and not is_editor(request.user):
        raise PermissionDenied
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    form = AchievementForm(request.POST or None, instance=achievement)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Prestasi berhasil diperbarui!")
        return redirect("main:show_achievements")

    context = {
        "copy": ACHIEVEMENT_COPY["en"],
        "form": form,
        "form_title": "Update Achievement",
        "form_eyebrow": "Portfolio / Achievements",
        "form_heading": "Update Achievement",
        "form_intro": "Update this achievement in your portfolio.",
        "submit_label": "Simpan Perubahan",
    }
    return render(request, "achievements/form.html", context)


# Hapus melalui POST
@login_required(login_url="/login/")
@require_POST
def delete_achievement(request, achievement_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    achievement.delete()
    messages.success(request, "Prestasi berhasil dihapus!")
    return redirect("main:show_achievements")


# Toggle star untuk pengguna login
@login_required(login_url="/login/")
@require_POST
def toggle_achievement_star(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)

    if request.user in achievement.starred_by.all():
        achievement.starred_by.remove(request.user)
    else:
        achievement.starred_by.add(request.user)

    return redirect("main:show_achievements")
