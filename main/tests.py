import json
from importlib import import_module
from unittest.mock import patch

from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from main.models import Achievement, Experience, Project, Skill


class ProjectPageTest(TestCase):
    def test_project_page_css_allows_content_to_scroll(self):
        css = (settings.BASE_DIR / "static" / "css" / "style.css").read_text()
        desktop_rule = css.split("@media (min-width: 1001px)", 1)[1].split(
            "@media", 1
        )[0]

        self.assertNotIn("overflow: hidden", desktop_rule)
        self.assertIn("min-height: 100vh", desktop_rule)

    def test_project_page_uses_projects_template(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertTemplateUsed(response, "base.html")

    def test_project_page_links_to_create_project_form(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(
            response,
            f'href="{reverse("main:create_project")}"',
        )
        self.assertContains(response, "Add Project")

    def test_project_page_filters_projects_by_title(self):
        matching_project = Project.objects.create(
            title="Searchable Observatory",
            description="The project that should be shown.",
            category="Backend",
        )
        hidden_project = Project.objects.create(
            title="Hidden Greenhouse",
            description="The project that should be filtered out.",
            category="IoT",
        )

        response = self.client.get(
            reverse("main:show_projects"),
            {"title": "observatory"},
        )

        self.assertContains(response, matching_project.title)
        self.assertNotContains(response, hidden_project.title)
        self.assertContains(response, 'value="observatory"')

    def test_homepage_links_to_project_page(self):
        response = self.client.get(reverse("landing_page"))

        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

    def test_homepage_uses_base_template(self):
        response = self.client.get(reverse("landing_page"))

        self.assertTemplateUsed(response, "index.html")
        self.assertTemplateUsed(response, "base.html")

    def test_homepage_does_not_duplicate_project_cards(self):
        response = self.client.get(reverse("landing_page"))

        self.assertNotContains(response, 'class="project-card"')

    def test_project_data_appears_on_page(self):
        project = Project.objects.create(
            title="STUMO Wristband",
            description="Wearable untuk pemantauan kesehatan siswa.",
            category="IoT",
            project_url="https://example.com/stumo",
            thumbnail="https://example.com/stumo.png",
            is_featured=True,
        )

        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, project.title)
        self.assertContains(response, project.description)
        self.assertContains(response, project.category)
        self.assertContains(response, project.project_url)
        self.assertContains(response, project.thumbnail)
        self.assertContains(response, "Featured project")

    def test_project_page_shows_empty_state_without_data(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, "No projects have been added yet.")

    def test_indonesian_project_page_uses_indonesian_content(self):
        project = Project.objects.create(
            title="Cellulose Acetate Membrane Research",
            description="Research on an environmentally friendly CO2 adsorbent.",
            title_id="Riset Membran Selulosa Asetat",
            description_id="Riset adsorben CO2 yang ramah lingkungan.",
            category="Data Analysis / Research",
        )

        response = self.client.get(reverse("main:show_projects_id"))

        self.assertContains(response, 'lang="id"')
        self.assertContains(response, project.title_id)
        self.assertContains(response, project.description_id)
        self.assertNotContains(response, project.description)


class ProjectModelTest(TestCase):
    def test_project_stores_portfolio_data(self):
        project = Project.objects.create(
            title="Kusut-Kusut",
            description="Backend Django untuk interaksi sosial.",
            title_id="Kusut-Kusut",
            description_id="Backend Django untuk interaksi sosial.",
            category="Backend",
            project_url="https://github.com/MaxKwen/kusutkusut-backend",
            thumbnail="https://example.com/kusut-kusut.png",
        )

        self.assertEqual(str(project), "Kusut-Kusut")
        self.assertEqual(project.title_id, "Kusut-Kusut")
        self.assertEqual(
            project.description_id,
            "Backend Django untuk interaksi sosial.",
        )
        self.assertEqual(project.category, "Backend")
        self.assertFalse(project.is_featured)


class ProjectFormTest(TestCase):
    def test_project_form_exposes_portfolio_project_fields(self):
        forms_module = import_module("main.forms")
        project_form_class = getattr(forms_module, "ProjectForm", None)

        self.assertIsNotNone(project_form_class)
        self.assertEqual(
            list(project_form_class().fields),
            [
                "title",
                "description",
                "title_id",
                "description_id",
                "category",
                "project_url",
                "thumbnail",
                "is_featured",
            ],
        )

    def test_project_form_uses_helpful_labels_and_widgets(self):
        project_form_class = getattr(import_module("main.forms"), "ProjectForm")
        form = project_form_class()

        self.assertEqual(form.fields["title"].label, "Nama Proyek (Inggris)")
        self.assertEqual(form.fields["description"].widget.attrs["rows"], 4)
        self.assertEqual(
            form.fields["project_url"].widget.attrs["placeholder"],
            "https://github.com/username/project",
        )
        self.assertEqual(
            form.fields["thumbnail"].widget.attrs["placeholder"],
            "https://example.com/project.png",
        )
        self.assertEqual(form.fields["is_featured"].label, "Proyek Unggulan")


class ExperienceFormTest(TestCase):
    def test_experience_form_exposes_all_editable_fields(self):
        experience_form_class = getattr(
            import_module("main.forms"),
            "ExperienceForm",
            None,
        )

        self.assertIsNotNone(experience_form_class)
        self.assertEqual(
            list(experience_form_class().fields),
            [
                "title",
                "title_id",
                "organization",
                "organization_id",
                "description",
                "description_id",
                "category",
                "start_year",
                "end_year",
            ],
        )

    def test_experience_form_uses_helpful_labels_and_widgets(self):
        experience_form_class = getattr(import_module("main.forms"), "ExperienceForm")
        form = experience_form_class()

        self.assertEqual(form.fields["title"].label, "Posisi (Inggris)")
        self.assertEqual(form.fields["description"].widget.attrs["rows"], 4)
        self.assertEqual(form.fields["start_year"].widget.attrs["min"], 1900)
        self.assertEqual(form.fields["end_year"].required, False)

    def test_experience_form_saves_valid_data(self):
        experience_form_class = getattr(import_module("main.forms"), "ExperienceForm")
        form = experience_form_class(
            data={
                "title": "Teaching Assistant",
                "title_id": "Asisten Pengajar",
                "organization": "University of Indonesia",
                "organization_id": "Universitas Indonesia",
                "description": "Led weekly tutorials.",
                "description_id": "Memimpin tutorial mingguan.",
                "category": "Teaching",
                "start_year": 2026,
                "end_year": "",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        experience = form.save()
        self.assertEqual(experience.title, "Teaching Assistant")
        self.assertIsNone(experience.end_year)


class AchievementFormTest(TestCase):
    def test_achievement_form_exposes_all_editable_fields(self):
        achievement_form_class = getattr(
            import_module("main.forms"),
            "AchievementForm",
            None,
        )

        self.assertIsNotNone(achievement_form_class)
        self.assertEqual(
            list(achievement_form_class().fields),
            [
                "title",
                "title_id",
                "result",
                "result_id",
                "category",
                "year",
                "display_order",
            ],
        )

    def test_achievement_form_uses_helpful_labels_and_widgets(self):
        achievement_form_class = getattr(
            import_module("main.forms"),
            "AchievementForm",
        )
        form = achievement_form_class()

        self.assertEqual(form.fields["title"].label, "Prestasi (Inggris)")
        self.assertEqual(form.fields["year"].widget.attrs["min"], 1900)
        self.assertEqual(form.fields["year"].required, False)
        self.assertEqual(form.fields["display_order"].widget.attrs["min"], 0)

    def test_achievement_form_saves_valid_data(self):
        achievement_form_class = getattr(
            import_module("main.forms"),
            "AchievementForm",
        )
        form = achievement_form_class(
            data={
                "title": "OSN Informatics",
                "title_id": "Informatika OSN",
                "result": "National finalist",
                "result_id": "Finalis nasional",
                "category": "Competition",
                "year": 2023,
                "display_order": 1,
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        achievement = form.save()
        self.assertEqual(achievement.title, "OSN Informatics")
        self.assertEqual(achievement.display_order, 1)


class ExperienceCreateViewTest(TestCase):
    def test_create_experience_page_displays_experience_form(self):
        experience_form_class = getattr(import_module("main.forms"), "ExperienceForm")

        response = self.client.get(reverse("main:create_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experiences_form.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertIsInstance(response.context["form"], experience_form_class)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_create_experience_saves_valid_submission(self):
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Research Assistant",
                "title_id": "Asisten Riset",
                "organization": "University of Indonesia",
                "organization_id": "Universitas Indonesia",
                "description": "Supported applied research.",
                "description_id": "Mendukung riset terapan.",
                "category": "Research",
                "start_year": 2025,
                "end_year": 2026,
            },
        )

        self.assertRedirects(response, reverse("main:show_experiences"))
        experience = Experience.objects.get(title="Research Assistant")
        self.assertEqual(experience.title_id, "Asisten Riset")
        self.assertEqual(experience.end_year, 2026)

    def test_experience_page_links_to_create_form(self):
        response = self.client.get(reverse("main:show_experiences"))

        self.assertContains(
            response,
            f'href="{reverse("main:create_experience")}"',
        )
        self.assertContains(response, "Add Experience")


class AchievementCreateViewTest(TestCase):
    def test_create_achievement_page_displays_achievement_form(self):
        achievement_form_class = getattr(
            import_module("main.forms"),
            "AchievementForm",
        )

        response = self.client.get(reverse("main:create_achievement"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievements_form.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertIsInstance(response.context["form"], achievement_form_class)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_create_achievement_saves_valid_submission(self):
        response = self.client.post(
            reverse("main:create_achievement"),
            {
                "title": "Programming Competition",
                "title_id": "Kompetisi Pemrograman",
                "result": "Finalist",
                "result_id": "Finalis",
                "category": "Competition",
                "year": 2026,
                "display_order": 3,
            },
        )

        self.assertRedirects(response, reverse("main:show_achievements"))
        achievement = Achievement.objects.get(title="Programming Competition")
        self.assertEqual(achievement.title_id, "Kompetisi Pemrograman")
        self.assertEqual(achievement.display_order, 3)

    def test_achievement_page_links_to_create_form(self):
        response = self.client.get(reverse("main:show_achievements"))

        self.assertContains(
            response,
            f'href="{reverse("main:create_achievement")}"',
        )
        self.assertContains(response, "Add Achievement")


class ExperienceUpdateViewTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Original Role",
            title_id="Peran Awal",
            organization="Original Organization",
            organization_id="Organisasi Awal",
            description="Original description.",
            description_id="Deskripsi awal.",
            category="Organization",
            start_year=2025,
        )
        self.experience_count = Experience.objects.count()

    def test_update_experience_page_displays_bound_form(self):
        experience_form_class = getattr(import_module("main.forms"), "ExperienceForm")

        response = self.client.get(
            reverse("main:update_experience", args=[self.experience.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experiences_form.html")
        self.assertIsInstance(response.context["form"], experience_form_class)
        self.assertEqual(response.context["form"].instance, self.experience)
        self.assertContains(response, "Update Experience")

    def test_update_experience_saves_changes_without_creating_duplicate(self):
        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.pk]),
            {
                "title": "Updated Role",
                "title_id": "Peran Diperbarui",
                "organization": "Updated Organization",
                "organization_id": "Organisasi Diperbarui",
                "description": "Updated description.",
                "description_id": "Deskripsi diperbarui.",
                "category": "Teaching",
                "start_year": 2025,
                "end_year": 2026,
            },
        )

        self.assertRedirects(response, reverse("main:show_experiences"))
        self.assertEqual(Experience.objects.count(), self.experience_count)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated Role")
        self.assertEqual(self.experience.end_year, 2026)

    def test_experience_page_links_to_update_form(self):
        response = self.client.get(reverse("main:show_experiences"))

        self.assertContains(
            response,
            f'href="{reverse("main:update_experience", args=[self.experience.pk])}"',
        )
        self.assertContains(response, "Edit Experience")

    def test_update_experience_returns_not_found_for_unknown_entry(self):
        response = self.client.get(reverse("main:update_experience", args=[999999]))

        self.assertEqual(response.status_code, 404)

    def test_experience_card_aligns_actions_like_project_card(self):
        css = (settings.BASE_DIR / "static" / "css" / "style.css").read_text()
        experience_rule = css.split(".experience-card {", 1)[1].split("}", 1)[0]
        edit_button_rule = css.split(".projects-page .project-link {", 1)[1].split(
            "}", 1
        )[0]

        self.assertIn("display: flex", experience_rule)
        self.assertIn("flex-direction: column", experience_rule)
        self.assertIn("border: 1px solid var(--line)", edit_button_rule)
        self.assertIn("background: var(--surface)", edit_button_rule)
        self.assertIn("text-decoration: none", edit_button_rule)


class AchievementUpdateViewTest(TestCase):
    def setUp(self):
        self.achievement = Achievement.objects.create(
            title="Original Achievement",
            title_id="Prestasi Awal",
            result="Original result",
            result_id="Hasil awal",
            category="Competition",
            year=2025,
            display_order=10,
        )
        self.achievement_count = Achievement.objects.count()

    def test_update_achievement_page_displays_bound_form(self):
        achievement_form_class = getattr(
            import_module("main.forms"),
            "AchievementForm",
        )

        response = self.client.get(
            reverse("main:update_achievement", args=[self.achievement.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievements_form.html")
        self.assertIsInstance(response.context["form"], achievement_form_class)
        self.assertEqual(response.context["form"].instance, self.achievement)
        self.assertContains(response, "Update Achievement")

    def test_update_achievement_saves_changes_without_creating_duplicate(self):
        response = self.client.post(
            reverse("main:update_achievement", args=[self.achievement.pk]),
            {
                "title": "Updated Achievement",
                "title_id": "Prestasi Diperbarui",
                "result": "Updated result",
                "result_id": "Hasil diperbarui",
                "category": "Certification",
                "year": 2026,
                "display_order": 2,
            },
        )

        self.assertRedirects(response, reverse("main:show_achievements"))
        self.assertEqual(Achievement.objects.count(), self.achievement_count)
        self.achievement.refresh_from_db()
        self.assertEqual(self.achievement.title, "Updated Achievement")
        self.assertEqual(self.achievement.display_order, 2)

    def test_achievement_page_links_to_update_form(self):
        response = self.client.get(reverse("main:show_achievements"))

        self.assertContains(
            response,
            f'href="{reverse("main:update_achievement", args=[self.achievement.pk])}"',
        )
        self.assertContains(response, "Edit Achievement")

    def test_update_achievement_returns_not_found_for_unknown_entry(self):
        response = self.client.get(reverse("main:update_achievement", args=[999999]))

        self.assertEqual(response.status_code, 404)

    def test_achievement_card_aligns_actions_like_project_card(self):
        css = (settings.BASE_DIR / "static" / "css" / "style.css").read_text()
        achievement_rule = css.split(".achievement-card {", 1)[1].split("}", 1)[0]

        self.assertIn("display: flex", achievement_rule)
        self.assertIn("flex-direction: column", achievement_rule)


class ExperienceDeleteViewTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Experience to Delete",
            organization="University of Indonesia",
            description="Temporary experience.",
            category="Teaching",
            start_year=2026,
        )

    def test_delete_experience_removes_entry_and_redirects(self):
        response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.pk])
        )

        self.assertRedirects(response, reverse("main:show_experiences"))
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_delete_experience_rejects_get_request(self):
        response = self.client.get(
            reverse("main:delete_experience", args=[self.experience.pk])
        )

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_experience_page_displays_delete_confirmation(self):
        response = self.client.get(reverse("main:show_experiences"))

        self.assertContains(
            response,
            f'action="{reverse("main:delete_experience", args=[self.experience.pk])}"',
        )
        self.assertContains(response, f'id="delete-experience-{self.experience.pk}"')
        self.assertContains(response, "Delete Experience")


class AchievementDeleteViewTest(TestCase):
    def setUp(self):
        self.achievement = Achievement.objects.create(
            title="Achievement to Delete",
            result="Temporary result",
            category="Competition",
            year=2026,
            display_order=10,
        )

    def test_delete_achievement_removes_entry_and_redirects(self):
        response = self.client.post(
            reverse("main:delete_achievement", args=[self.achievement.pk])
        )

        self.assertRedirects(response, reverse("main:show_achievements"))
        self.assertFalse(Achievement.objects.filter(pk=self.achievement.pk).exists())

    def test_delete_achievement_rejects_get_request(self):
        response = self.client.get(
            reverse("main:delete_achievement", args=[self.achievement.pk])
        )

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Achievement.objects.filter(pk=self.achievement.pk).exists())

    def test_achievement_page_displays_delete_confirmation(self):
        response = self.client.get(reverse("main:show_achievements"))

        self.assertContains(
            response,
            f'action="{reverse("main:delete_achievement", args=[self.achievement.pk])}"',
        )
        self.assertContains(response, f'id="delete-achievement-{self.achievement.pk}"')
        self.assertContains(response, "Delete Achievement")


class ProjectCreateViewTest(TestCase):
    def test_create_project_page_displays_project_form(self):
        project_form_class = getattr(import_module("main.forms"), "ProjectForm")

        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertIsInstance(response.context["form"], project_form_class)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_create_project_saves_valid_submission(self):
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "Personal Portfolio",
                "description": "A portfolio built with Django.",
                "title_id": "Portofolio Pribadi",
                "description_id": "Portofolio yang dibuat dengan Django.",
                "category": "Backend",
                "project_url": "https://example.com/portfolio",
                "thumbnail": "https://example.com/portfolio.png",
                "is_featured": "on",
            },
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        project = Project.objects.get(title="Personal Portfolio")
        self.assertEqual(project.title_id, "Portofolio Pribadi")
        self.assertTrue(project.is_featured)

    def test_create_project_displays_success_message(self):
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "Message Test Project",
                "description": "A project created to test feedback.",
                "category": "Backend",
            },
            follow=True,
        )

        self.assertContains(response, "Proyek baru berhasil ditambahkan!")


class ProjectUpdateViewTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Original Project",
            description="Original description.",
            title_id="Proyek Awal",
            description_id="Deskripsi awal.",
            category="Backend",
        )
        self.project_count = Project.objects.count()

    def test_update_project_page_displays_bound_project_form(self):
        project_form_class = getattr(import_module("main.forms"), "ProjectForm")

        response = self.client.get(
            reverse("main:update_project", args=[self.project.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertIsInstance(response.context["form"], project_form_class)
        self.assertEqual(response.context["form"].instance, self.project)
        self.assertContains(response, "Update Project")

    def test_update_project_saves_changes_without_creating_duplicate(self):
        response = self.client.post(
            reverse("main:update_project", args=[self.project.pk]),
            {
                "title": "Updated Project",
                "description": "Updated description.",
                "title_id": "Proyek Diperbarui",
                "description_id": "Deskripsi diperbarui.",
                "category": "Full Stack",
                "project_url": "https://example.com/updated",
                "thumbnail": "",
                "is_featured": "on",
            },
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertEqual(Project.objects.count(), self.project_count)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Updated Project")
        self.assertEqual(self.project.category, "Full Stack")
        self.assertTrue(self.project.is_featured)

    def test_project_page_links_to_update_form(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(
            response,
            f'href="{reverse("main:update_project", args=[self.project.pk])}"',
        )
        self.assertContains(response, "Edit Project")

    def test_update_project_returns_not_found_for_unknown_project(self):
        response = self.client.get(reverse("main:update_project", args=[999999]))

        self.assertEqual(response.status_code, 404)


class ProjectDataDeliveryTest(TestCase):
    def test_projects_json_endpoint_serializes_projects(self):
        project = Project.objects.create(
            title="JSON Portfolio",
            description="Project exposed through the JSON endpoint.",
            category="Backend",
        )

        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        payload = json.loads(response.content)
        serialized_project = next(
            item for item in payload if item["pk"] == project.pk
        )
        self.assertEqual(serialized_project["model"], "main.project")
        self.assertEqual(serialized_project["fields"]["title"], project.title)

    def test_projects_json_endpoint_filters_title_case_insensitively(self):
        matching_project = Project.objects.create(
            title="NeedleProjectXylophone",
            description="The matching project.",
            category="Backend",
        )
        Project.objects.create(
            title="Unrelated Project",
            description="This project should not match.",
            category="Frontend",
        )

        response = self.client.get(
            reverse("main:get_projects_json"),
            {"title": "  needleproject  "},
        )

        payload = json.loads(response.content)
        self.assertEqual([item["pk"] for item in payload], [matching_project.pk])


class ExperienceDataDeliveryTest(TestCase):
    def test_experiences_json_endpoint_serializes_experiences(self):
        experience = Experience.objects.create(
            title="JSON Experience",
            organization="University of Indonesia",
            description="Experience exposed through the JSON endpoint.",
            category="Teaching",
            start_year=2026,
        )

        response = self.client.get(reverse("main:get_experiences_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        payload = json.loads(response.content)
        serialized_experience = next(
            item for item in payload if item["pk"] == experience.pk
        )
        self.assertEqual(serialized_experience["model"], "main.experience")
        self.assertEqual(
            serialized_experience["fields"]["title"],
            experience.title,
        )

    def test_experience_page_deserializes_json_response(self):
        experience = Experience.objects.create(
            title="Deserialized Experience",
            organization="University of Indonesia",
            description="Rendered after JSON deserialization.",
            category="Research",
            start_year=2026,
        )
        payload = serializers.serialize(
            "json",
            Experience.objects.filter(pk=experience.pk),
        )

        with patch("main.views.get_experiences_json") as get_json:
            get_json.return_value = HttpResponse(
                payload,
                content_type="application/json",
            )
            response = self.client.get(reverse("main:show_experiences"))

        get_json.assert_called_once()
        self.assertContains(response, experience.title)
        self.assertContains(response, experience.description)


class AchievementDataDeliveryTest(TestCase):
    def test_achievements_json_endpoint_serializes_achievements(self):
        achievement = Achievement.objects.create(
            title="JSON Achievement",
            result="Finalist",
            category="Competition",
            year=2026,
            display_order=10,
        )

        response = self.client.get(reverse("main:get_achievements_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        payload = json.loads(response.content)
        serialized_achievement = next(
            item for item in payload if item["pk"] == achievement.pk
        )
        self.assertEqual(serialized_achievement["model"], "main.achievement")
        self.assertEqual(
            serialized_achievement["fields"]["title"],
            achievement.title,
        )

    def test_achievement_page_deserializes_json_response(self):
        achievement = Achievement.objects.create(
            title="Deserialized Achievement",
            result="National finalist",
            category="Competition",
            year=2026,
            display_order=10,
        )
        payload = serializers.serialize(
            "json",
            Achievement.objects.filter(pk=achievement.pk),
        )

        with patch("main.views.get_achievements_json") as get_json:
            get_json.return_value = HttpResponse(
                payload,
                content_type="application/json",
            )
            response = self.client.get(reverse("main:show_achievements"))

        get_json.assert_called_once()
        self.assertContains(response, achievement.title)
        self.assertContains(response, achievement.result)


class ProjectDeleteViewTest(TestCase):
    def test_delete_project_removes_project_and_redirects(self):
        project = Project.objects.create(
            title="Disposable Prototype",
            description="A project to remove.",
            category="Prototype",
        )

        response = self.client.post(
            reverse("main:delete_project", args=[project.pk]),
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(pk=project.pk).exists())

    def test_project_page_displays_delete_confirmation(self):
        project = Project.objects.create(
            title="Project With Delete Button",
            description="A removable project.",
            category="Backend",
        )

        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(
            response,
            f'action="{reverse("main:delete_project", args=[project.pk])}"',
        )
        self.assertContains(response, f'id="delete-project-{project.pk}"')
        self.assertContains(response, "Delete Project")


class SeedProjectDataTest(TestCase):
    def test_three_featured_projects_are_available(self):
        expected_titles = {
            "Kusut-Kusut",
            "STUMO Wristband",
            "Cellulose Acetate Membrane Research",
        }

        projects = Project.objects.filter(title__in=expected_titles)

        self.assertEqual(set(projects.values_list("title", flat=True)), expected_titles)
        self.assertTrue(all(project.is_featured for project in projects))


class ExperienceModelTest(TestCase):
    def test_experience_stores_bilingual_portfolio_data(self):
        experience = Experience.objects.create(
            title="Teaching Assistant, Intro to Digital System",
            title_id="Asisten Pengajar, Sistem Digital Dasar",
            organization="Faculty of Computer Science, University of Indonesia",
            organization_id="Fakultas Ilmu Komputer, Universitas Indonesia",
            description="Led tutorials and evaluated weekly work.",
            description_id="Memimpin tutorial dan mengevaluasi tugas mingguan.",
            category="Teaching",
            start_year=2026,
        )

        self.assertEqual(str(experience), experience.title)
        self.assertTrue(experience.is_ongoing)
        self.assertIsNone(experience.end_year)


class ExperiencePageTest(TestCase):
    def setUp(self):
        Experience.objects.all().delete()

    def test_experience_page_uses_experiences_template(self):
        response = self.client.get(reverse("main:show_experiences"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experiences.html")
        self.assertTemplateUsed(response, "base.html")

    def test_navigation_links_to_matching_experience_pages(self):
        english_pages = [
            "landing_page",
            "main:show_projects",
            "main:show_skills",
            "main:show_achievements",
        ]
        indonesian_pages = [
            "landing_page_id",
            "main:show_projects_id",
            "main:show_skills_id",
            "main:show_achievements_id",
        ]

        for page_name in english_pages:
            with self.subTest(page_name=page_name):
                response = self.client.get(reverse(page_name))
                self.assertContains(
                    response,
                    f'href="{reverse("main:show_experiences")}"',
                )

        for page_name in indonesian_pages:
            with self.subTest(page_name=page_name):
                response = self.client.get(reverse(page_name))
                self.assertContains(
                    response,
                    f'href="{reverse("main:show_experiences_id")}"',
                )

    def test_experience_page_renders_experience_from_database(self):
        experience = Experience.objects.create(
            title="Teaching Assistant, Intro to Digital System",
            organization="Faculty of Computer Science, University of Indonesia",
            description="Led tutorials and evaluated weekly work.",
            category="Teaching",
            start_year=2026,
        )

        response = self.client.get(reverse("main:show_experiences"))

        self.assertContains(response, experience.title)
        self.assertContains(response, experience.organization)
        self.assertContains(response, experience.description)
        self.assertContains(response, "2026 — present")

    def test_indonesian_experience_page_uses_translated_data(self):
        experience = Experience.objects.create(
            title="Teaching Assistant",
            title_id="Asisten Pengajar",
            organization="University of Indonesia",
            organization_id="Universitas Indonesia",
            description="Led weekly tutorials.",
            description_id="Memimpin tutorial mingguan.",
            category="Teaching",
            start_year=2026,
        )

        response = self.client.get(reverse("main:show_experiences_id"))

        self.assertContains(response, 'lang="id"')
        self.assertContains(response, experience.title_id)
        self.assertContains(response, experience.organization_id)
        self.assertContains(response, experience.description_id)
        self.assertNotContains(response, experience.description)

    def test_homepage_does_not_duplicate_experience_cards(self):
        experience = Experience.objects.create(
            title="Standalone Experience Entry",
            organization="University of Indonesia",
            description="Shown only on the Experience page.",
            category="Teaching",
            start_year=2026,
        )

        response = self.client.get(reverse("landing_page"))

        self.assertNotContains(response, experience.title)
        self.assertNotContains(response, 'class="experience-card"')


class SeedExperienceDataTest(TestCase):
    def test_two_current_experiences_are_available(self):
        expected_titles = {
            "Teaching Assistant, Intro to Digital System",
            "Staff, Data Science Academy",
        }

        experiences = Experience.objects.filter(title__in=expected_titles)

        self.assertEqual(
            set(experiences.values_list("title", flat=True)),
            expected_titles,
        )
        self.assertTrue(all(experience.is_ongoing for experience in experiences))


class SkillModelTest(TestCase):
    def test_skill_stores_display_data(self):
        skill = Skill.objects.create(
            name="Python",
            category="language",
            icon="img/python.png",
            display_order=4,
        )

        self.assertEqual(str(skill), "Python")
        self.assertEqual(skill.category, "language")
        self.assertEqual(skill.icon, "img/python.png")
        self.assertEqual(skill.display_order, 4)


class SkillPageTest(TestCase):
    def setUp(self):
        Skill.objects.all().delete()

    def test_skill_page_uses_skills_template(self):
        response = self.client.get(reverse("main:show_skills"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skills.html")
        self.assertTemplateUsed(response, "base.html")

    def test_skill_page_renders_database_data_in_display_order(self):
        second_skill = Skill.objects.create(
            name="Django",
            category="backend",
            icon="img/django.png",
            display_order=2,
        )
        first_skill = Skill.objects.create(
            name="Python",
            category="language",
            icon="img/python.png",
            display_order=1,
        )

        response = self.client.get(reverse("main:show_skills"))
        content = response.content.decode()

        self.assertContains(response, first_skill.name)
        self.assertContains(response, second_skill.name)
        self.assertContains(response, "/static/img/python.png")
        self.assertContains(response, 'data-category="language"')
        self.assertLess(content.index(first_skill.name), content.index(second_skill.name))

    def test_skill_page_shows_empty_state_without_data(self):
        response = self.client.get(reverse("main:show_skills"))

        self.assertContains(response, "No skills have been added yet.")

    def test_homepages_link_to_matching_skill_pages(self):
        english_response = self.client.get(reverse("landing_page"))
        indonesian_response = self.client.get(reverse("landing_page_id"))

        self.assertContains(
            english_response,
            f'href="{reverse("main:show_skills")}"',
        )
        self.assertContains(
            indonesian_response,
            f'href="{reverse("main:show_skills_id")}"',
        )

    def test_homepage_does_not_duplicate_skill_cards(self):
        response = self.client.get(reverse("landing_page"))

        self.assertNotContains(response, 'class="skill-card"')

    def test_indonesian_skill_page_uses_localized_labels(self):
        response = self.client.get(reverse("main:show_skills_id"))

        self.assertContains(response, 'lang="id"')
        self.assertContains(response, "Keahlian")
        self.assertContains(response, "Semua")
        self.assertContains(response, "Bahasa Pemrograman")
        self.assertContains(response, "Alat")


class SeedSkillDataTest(TestCase):
    def test_twelve_portfolio_skills_are_available_in_order(self):
        expected_names = [
            "C",
            "C++",
            "Java",
            "Python",
            "JavaScript",
            "Git",
            "GitHub",
            "Jupyter Notebook",
            "Visual Studio Code",
            "Django",
            "HTML",
            "CSS",
        ]

        self.assertEqual(
            list(Skill.objects.values_list("name", flat=True)),
            expected_names,
        )


class AchievementModelTest(TestCase):
    def test_achievement_stores_bilingual_display_data(self):
        achievement = Achievement.objects.create(
            title="OSN Informatics",
            title_id="Informatika OSN",
            result="National finalist",
            result_id="Finalis nasional",
            category="Competition",
            year=None,
            display_order=1,
        )

        self.assertEqual(str(achievement), "OSN Informatics")
        self.assertIsNone(achievement.year)
        self.assertEqual(achievement.display_order, 1)


class AchievementPageTest(TestCase):
    def setUp(self):
        Achievement.objects.all().delete()

    def test_achievement_page_uses_achievements_template(self):
        response = self.client.get(reverse("main:show_achievements"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievements.html")
        self.assertTemplateUsed(response, "base.html")

    def test_achievement_page_renders_database_data_in_display_order(self):
        second_achievement = Achievement.objects.create(
            title="AMO",
            result="Bronze medal",
            category="Competition",
            year=2024,
            display_order=2,
        )
        first_achievement = Achievement.objects.create(
            title="OSN Informatics",
            result="National finalist",
            category="Competition",
            year=2023,
            display_order=1,
        )

        response = self.client.get(reverse("main:show_achievements"))
        content = response.content.decode()

        self.assertContains(response, first_achievement.title)
        self.assertContains(response, first_achievement.result)
        self.assertContains(response, first_achievement.category)
        self.assertContains(response, str(first_achievement.year))
        self.assertLess(
            content.index(first_achievement.title),
            content.index(second_achievement.title),
        )

    def test_indonesian_achievement_page_uses_translated_data(self):
        achievement = Achievement.objects.create(
            title="OSN Informatics",
            title_id="Informatika OSN",
            result="National finalist",
            result_id="Finalis nasional",
            category="Competition",
            display_order=1,
        )

        response = self.client.get(reverse("main:show_achievements_id"))

        self.assertContains(response, 'lang="id"')
        self.assertContains(response, achievement.title_id)
        self.assertContains(response, achievement.result_id)
        self.assertNotContains(response, achievement.result)

    def test_achievement_page_shows_empty_state_without_data(self):
        response = self.client.get(reverse("main:show_achievements"))

        self.assertContains(response, "No achievements have been added yet.")

    def test_homepages_link_to_matching_achievement_pages(self):
        english_response = self.client.get(reverse("landing_page"))
        indonesian_response = self.client.get(reverse("landing_page_id"))

        self.assertContains(
            english_response,
            f'href="{reverse("main:show_achievements")}"',
        )
        self.assertContains(
            indonesian_response,
            f'href="{reverse("main:show_achievements_id")}"',
        )

    def test_homepage_does_not_duplicate_achievement_cards(self):
        response = self.client.get(reverse("landing_page"))

        self.assertNotContains(response, "OSN Informatics")


class SeedAchievementDataTest(TestCase):
    def test_two_portfolio_achievements_are_available_in_order(self):
        self.assertEqual(
            list(Achievement.objects.values_list("title", flat=True)),
            ["OSN Informatics", "AMO"],
        )
