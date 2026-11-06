from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import Client, TestCase
from django.urls import reverse

from main.forms import AchievementForm, ExperienceForm
from main.models import Achievement, Experience


class PortfolioAjaxTest(TestCase):
    """Exercise both AJAX contracts against Django's isolated test database."""

    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create(username="ajax-owner", is_superuser=True)
        cls.member = get_user_model().objects.create(username="ajax-member")
        cls.editor = get_user_model().objects.create(username="ajax-editor")
        cls.editor.groups.add(Group.objects.create(name="Editor"))

    def setUp(self):
        self.sections = [
            {
                "prefix": "experience",
                "model": Experience,
                "form": ExperienceForm,
                "payload": {
                    "title": "AJAX Role", "title_id": "Peran AJAX",
                    "organization": "AJAX Organization", "organization_id": "Organisasi AJAX",
                    "description": "AJAX description", "description_id": "Deskripsi AJAX",
                    "category": "Teaching", "start_year": 2025, "end_year": 2026,
                },
                "texts": ["title", "title_id", "organization", "organization_id", "description", "description_id", "category"],
                "required_texts": ["title", "organization", "description", "category"],
                "search_fields": ["title", "title_id", "organization", "organization_id"],
                "modal": "experience-form-modal",
                "modal_roles": ("owner", "editor"),
            },
            {
                "prefix": "achievement",
                "model": Achievement,
                "form": AchievementForm,
                "payload": {
                    "title": "AJAX Award", "title_id": "Prestasi AJAX",
                    "result": "AJAX finalist", "result_id": "Finalis AJAX",
                    "category": "Competition", "year": 2026, "display_order": 5,
                },
                "texts": ["title", "title_id", "result", "result_id", "category"],
                "required_texts": ["title", "result", "category"],
                "search_fields": ["title", "title_id", "result", "result_id"],
                "modal": "add-achievement-modal",
                "modal_roles": ("owner",),
            },
        ]
        for section in self.sections:
            prefix = section["prefix"]
            section["api"] = reverse(f"main:get_{prefix}s_json")
            section["create"] = reverse(f"main:create_{prefix}_ajax")
            section["page"] = reverse(f"main:show_{prefix}s")
            section["item"] = section["model"].objects.create(**section["payload"])

    def fields_for(self, section, client=None):
        response = (client or self.client).get(section["api"])
        self.assertEqual(response.status_code, 200)
        return next(item["fields"] for item in response.json() if item["pk"] == section["item"].pk)

    def test_public_json_is_manual_and_preserves_all_model_fields(self):
        with patch("django.core.serializers.serialize", side_effect=AssertionError("Use manual JSON")):
            for section in self.sections:
                with self.subTest(model=section["prefix"]):
                    fields = self.fields_for(section)
                    for name, value in section["payload"].items():
                        self.assertEqual(fields[name], value)

    def test_search_matches_each_english_and_indonesian_field(self):
        for section in self.sections:
            for field in section["search_fields"]:
                with self.subTest(model=section["prefix"], field=field):
                    marker = f"needle-{field}"
                    section["model"].objects.filter(pk=section["item"].pk).update(**{field: marker})
                    response = self.client.get(section["api"], {"q": f"  {marker.upper()}  "})
                    self.assertEqual([item["pk"] for item in response.json()], [section["item"].pk])

    def test_unmatched_search_returns_empty_array(self):
        for section in self.sections:
            with self.subTest(model=section["prefix"]):
                self.assertEqual(self.client.get(section["api"], {"q": "never-matches-ajax"}).json(), [])

    def test_blank_search_returns_full_list_and_does_not_write(self):
        for section in self.sections:
            with self.subTest(model=section["prefix"]):
                expected = section["model"].objects.count()
                self.assertEqual(len(self.client.get(section["api"], {"q": "  "}).json()), expected)
                self.assertEqual(section["model"].objects.count(), expected)

    def test_empty_database_returns_empty_array(self):
        for section in self.sections:
            with self.subTest(model=section["prefix"]):
                section["model"].objects.all().delete()
                self.assertEqual(self.client.get(section["api"]).json(), [])

    def test_experience_order_is_latest_start_year_then_id(self):
        section = self.sections[0]
        Experience.objects.all().delete()
        older = Experience.objects.create(**{**section["payload"], "start_year": 2024})
        first = Experience.objects.create(**{**section["payload"], "start_year": 2026})
        second = Experience.objects.create(**{**section["payload"], "start_year": 2026})
        self.assertEqual([item["pk"] for item in self.client.get(section["api"]).json()], [first.pk, second.pk, older.pk])

    def test_achievement_order_is_display_order_then_title(self):
        section = self.sections[1]
        Achievement.objects.all().delete()
        later = Achievement.objects.create(**{**section["payload"], "display_order": 2})
        second = Achievement.objects.create(**{**section["payload"], "title": "B", "display_order": 1})
        first = Achievement.objects.create(**{**section["payload"], "title": "A", "display_order": 1})
        self.assertEqual([item["pk"] for item in self.client.get(section["api"]).json()], [first.pk, second.pk, later.pk])

    def test_json_star_state_is_specific_to_logged_in_user(self):
        for section in self.sections:
            with self.subTest(model=section["prefix"]):
                section["item"].starred_by.add(self.member)
                for user, is_starred in [(None, False), (self.member, True), (self.editor, False)]:
                    self.client.logout()
                    if user:
                        self.client.force_login(user)
                    fields = self.fields_for(section)
                    self.assertEqual(fields["star_count"], 1)
                    self.assertEqual(fields["is_starred"], is_starred)
                    self.assertEqual(fields["starred_by"], [[self.member.username]])
                    self.assertEqual(fields["starred_by_names"], self.member.username)

    def test_roles_control_json_permissions_and_modal_visibility(self):
        for user, can_update, can_delete in [(None, False, False), (self.member, False, False), (self.editor, True, False), (self.owner, True, True)]:
            self.client.logout()
            if user:
                self.client.force_login(user)
            for section in self.sections:
                with self.subTest(user=user, model=section["prefix"]):
                    fields = self.fields_for(section)
                    self.assertEqual(fields["can_update"], can_update)
                    self.assertEqual(fields["can_delete"], can_delete)
                    response = self.client.get(section["page"])
                    modal = f'id="{section["modal"]}"'
                    role = {self.owner: "owner", self.editor: "editor"}.get(user)
                    if role in section["modal_roles"]:
                        self.assertContains(response, modal)
                        self.assertIsInstance(response.context["form"], section["form"])
                    else:
                        self.assertNotContains(response, modal)

    def test_guest_member_and_editor_cannot_create_even_with_valid_data(self):
        for user in [None, self.member, self.editor]:
            self.client.logout()
            if user:
                self.client.force_login(user)
            for section in self.sections:
                with self.subTest(user=user, model=section["prefix"]):
                    before = section["model"].objects.count()
                    response = self.client.post(section["create"], section["payload"])
                    self.assertEqual(response.status_code, 403)
                    self.assertIn("message", response.json())
                    self.assertEqual(section["model"].objects.count(), before)

    def test_owner_creates_one_row_and_receives_json_201(self):
        self.client.force_login(self.owner)
        for section in self.sections:
            with self.subTest(model=section["prefix"]):
                before = section["model"].objects.count()
                response = self.client.post(section["create"], section["payload"])
                self.assertEqual(response.status_code, 201)
                self.assertEqual(section["model"].objects.count(), before + 1)
                item = section["model"].objects.get(pk=response.json()["pk"])
                for name, value in section["payload"].items():
                    self.assertEqual(getattr(item, name), value)
                self.assertEqual(item.starred_by.count(), 0)

    def test_invalid_submission_returns_field_errors_without_writing(self):
        self.client.force_login(self.owner)
        for section in self.sections:
            with self.subTest(model=section["prefix"]):
                before = section["model"].objects.count()
                response = self.client.post(section["create"], {})
                self.assertEqual(response.status_code, 400)
                for field in section["required_texts"]:
                    self.assertIn(field, response.json()["errors"])
                    self.assertIn("message", response.json()["errors"][field][0])
                self.assertEqual(section["model"].objects.count(), before)

    def test_create_endpoints_reject_non_post_methods(self):
        self.client.force_login(self.owner)
        for section in self.sections:
            for method in ["get", "put", "patch", "delete"]:
                with self.subTest(model=section["prefix"], method=method):
                    before = section["model"].objects.count()
                    response = getattr(self.client, method)(section["create"])
                    self.assertEqual(response.status_code, 405)
                    self.assertEqual(section["model"].objects.count(), before)

    def test_create_requires_csrf_and_accepts_rendered_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        for section in self.sections:
            with self.subTest(model=section["prefix"]):
                before = section["model"].objects.count()
                page = client.get(section["page"])
                self.assertContains(page, "csrfmiddlewaretoken")
                self.assertEqual(client.post(section["create"], section["payload"]).status_code, 403)
                self.assertEqual(client.post(section["create"], {**section["payload"], "csrfmiddlewaretoken": "x" * 64}).status_code, 403)
                self.assertEqual(section["model"].objects.count(), before)
                response = client.post(section["create"], {**section["payload"], "csrfmiddlewaretoken": client.cookies["csrftoken"].value})
                self.assertEqual(response.status_code, 201)
                self.assertEqual(section["model"].objects.count(), before + 1)

    def test_all_text_fields_are_stripped_before_persistence(self):
        self.client.force_login(self.owner)
        for section in self.sections:
            with self.subTest(model=section["prefix"]):
                payload = dict(section["payload"])
                for name in section["texts"]:
                    payload[name] = f' <b>{payload[name]}</b><img src="x" onerror="alert(1)"> '
                response = self.client.post(section["create"], payload)
                self.assertEqual(response.status_code, 201)
                item = section["model"].objects.get(pk=response.json()["pk"])
                for name in section["texts"]:
                    self.assertEqual(getattr(item, name), section["payload"][name])

    def test_html_only_required_text_is_rejected(self):
        self.client.force_login(self.owner)
        for section in self.sections:
            for field in section["required_texts"]:
                with self.subTest(model=section["prefix"], field=field):
                    before = section["model"].objects.count()
                    response = self.client.post(section["create"], {**section["payload"], field: '<img src="x" onerror="alert(1)">'})
                    self.assertEqual(response.status_code, 400)
                    self.assertIn(field, response.json()["errors"])
                    self.assertEqual(section["model"].objects.count(), before)

    def test_optional_translations_and_years_may_be_blank(self):
        self.client.force_login(self.owner)
        for section in self.sections:
            with self.subTest(model=section["prefix"]):
                payload = dict(section["payload"])
                for field in section["texts"]:
                    if field.endswith("_id"):
                        payload[field] = ""
                year_field = "end_year" if section["model"] is Experience else "year"
                payload[year_field] = ""
                response = self.client.post(section["create"], payload)
                self.assertEqual(response.status_code, 201)
                self.assertIsNone(getattr(section["model"].objects.get(pk=response.json()["pk"]), year_field))

    def test_year_ranges_and_display_order_are_validated(self):
        self.client.force_login(self.owner)
        for section in self.sections:
            fields = ["start_year", "end_year"] if section["model"] is Experience else ["year"]
            cases = [(field, value) for field in fields for value in [1899, 2101, "not-a-year"]]
            if section["model"] is Achievement:
                cases.append(("display_order", -1))
            for field, value in cases:
                with self.subTest(model=section["prefix"], field=field, value=value):
                    before = section["model"].objects.count()
                    response = self.client.post(section["create"], {**section["payload"], field: value})
                    self.assertEqual(response.status_code, 400)
                    self.assertIn(field, response.json()["errors"])
                    self.assertEqual(section["model"].objects.count(), before)

    def test_reversed_experience_year_range_is_rejected(self):
        self.client.force_login(self.owner)
        section = self.sections[0]
        before = Experience.objects.count()
        response = self.client.post(section["create"], {**section["payload"], "start_year": 2026, "end_year": 2025})
        self.assertEqual(response.status_code, 400)
        self.assertIn("end_year", response.json()["errors"])
        self.assertEqual(Experience.objects.count(), before)

    def test_success_language_and_unknown_language_fallback(self):
        self.client.force_login(self.owner)
        for section in self.sections:
            for language, expected in [("id", "berhasil ditambahkan"), ("en", "added successfully"), ("unknown", "added successfully")]:
                with self.subTest(model=section["prefix"], language=language):
                    response = self.client.post(section["create"], {**section["payload"], "language": language})
                    self.assertEqual(response.status_code, 201)
                    self.assertIn(expected, response.json()["message"])

    def test_templates_supply_loading_empty_error_search_and_retry_states(self):
        for section in self.sections:
            with self.subTest(model=section["prefix"]):
                response = self.client.get(section["page"], {"q": '"<script>alert(1)</script>'})
                for suffix in ["loading", "empty", "error", "grid", "retry", "search-form", "search-input", "card-template", "copy"]:
                    self.assertContains(response, f'id="{section["prefix"]}-{suffix}"')
                self.assertNotContains(response, '<script>alert(1)</script>')
                self.assertContains(response, "&lt;script&gt;")
