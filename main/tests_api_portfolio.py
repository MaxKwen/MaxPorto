"""Test API DRF Tugas 6 untuk Experience dan Achievement (matriks empat peran)."""

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Achievement, Experience

PASSWORD = "test-password-123"


class PortfolioSectionAPITestMixin:
    """Skenario bersama; subclass mengisi model, nama route, dan data contoh."""

    model = None
    route = ""          # prefix nama URL, mis. "experience" -> api:experience-list
    page = ""           # nama route halaman HTML bagian ini
    initial = {}        # data awal objek uji
    payload = {}        # data valid untuk POST/PUT
    search_hit = ""     # kata kunci yang cocok dengan objek awal
    text_fields = ()    # field teks yang dibersihkan strip_tags
    required_fields = ()

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password=PASSWORD, email="owner@example.com",
        )
        self.user = User.objects.create_user(
            username="member", password=PASSWORD, email="member@example.com",
        )
        self.editor = User.objects.create_user(username="editor", password=PASSWORD)
        self.editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        # Migrasi seed mengisi tabel; mulai dari kondisi yang terkendali
        self.model.objects.all().delete()
        self.item = self.model.objects.create(**self.initial)
        self.list_url = reverse(f"api:{self.route}-list")
        self.detail_url = reverse(f"api:{self.route}-detail", args=[self.item.pk])
        self.star_url = reverse(f"api:{self.route}-star", args=[self.item.pk])

    # ---------- helper ----------

    def as_user(self, user):
        self.client.force_authenticate(user=user)

    def snapshot(self):
        """Isi database yang harus tetap sama setelah permintaan ditolak."""
        return list(self.model.objects.order_by("pk").values())

    def assert_denied_without_change(self, response, before):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.snapshot(), before)

    # ---------- baca (semua peran) ----------

    def test_guest_can_read_list_and_detail_without_sensitive_data(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        item = response.data[0]
        self.assertEqual(item["id"], self.item.pk)
        self.assertEqual(item["star_count"], 0)
        self.assertFalse(item["is_starred"])
        for forbidden in ("email", "password", "starred_by", "fields", "pk"):
            self.assertNotIn(forbidden, item)
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_uses_query_parameter_and_allows_empty_results(self):
        response = self.client.get(self.list_url, {"q": self.search_hit.upper()})
        self.assertEqual([item["id"] for item in response.data], [self.item.pk])
        response = self.client.get(self.list_url, {"q": "no-such-entry"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_missing_object_returns_404(self):
        url = reverse(f"api:{self.route}-detail", args=[self.item.pk + 999])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)
        self.as_user(self.owner)
        self.assertEqual(self.client.delete(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_browsable_api_page_opens(self):
        response = self.client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("text/html", response["Content-Type"])

    # ---------- tulis: pengunjung dan pengguna biasa ----------

    def test_guest_and_member_cannot_write(self):
        for user in (None, self.user):
            with self.subTest(user=user):
                self.as_user(user)
                before = self.snapshot()
                self.assert_denied_without_change(
                    self.client.post(self.list_url, self.payload, format="json"), before,
                )
                self.assert_denied_without_change(
                    self.client.patch(self.detail_url, {"title": "Changed"}, format="json"), before,
                )
                self.assert_denied_without_change(
                    self.client.put(self.detail_url, self.payload, format="json"), before,
                )
                self.assert_denied_without_change(self.client.delete(self.detail_url), before)

    # ---------- tulis: Editor ----------

    def test_editor_can_patch_and_put(self):
        self.as_user(self.editor)
        response = self.client.patch(self.detail_url, {"title": "Edited"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, "Edited")
        # PATCH tidak menyentuh field lain
        self.assertEqual(self.item.category, self.initial["category"])

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, self.payload["title"])

    def test_editor_cannot_create_or_delete(self):
        self.as_user(self.editor)
        before = self.snapshot()
        self.assert_denied_without_change(
            self.client.post(self.list_url, self.payload, format="json"), before,
        )
        self.assert_denied_without_change(self.client.delete(self.detail_url), before)
        self.assertTrue(self.model.objects.filter(pk=self.item.pk).exists())

    # ---------- tulis: pemilik ----------

    def test_owner_can_create_and_delete(self):
        self.as_user(self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = self.model.objects.get(pk=response.data["id"])
        self.assertEqual(created.title, self.payload["title"])

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(self.model.objects.filter(pk=self.item.pk).exists())

    def test_wrong_method_returns_405(self):
        self.as_user(self.owner)
        self.assertEqual(
            self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
        )
        self.assertEqual(
            self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    # ---------- validasi ----------

    def test_text_fields_are_stripped_before_saving(self):
        self.as_user(self.owner)
        dirty = {name: f"<b>{name}</b> <script>x</script>" for name in self.text_fields}
        response = self.client.post(self.list_url, {**self.payload, **dirty}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = self.model.objects.get(pk=response.data["id"])
        for name in self.text_fields:
            stored = getattr(created, name)
            self.assertNotIn("<", stored, name)
            self.assertTrue(stored.startswith(name), name)

    def test_required_text_that_becomes_empty_is_rejected(self):
        self.as_user(self.owner)
        before = self.snapshot()
        for name in self.required_fields:
            for value in (" ", "<i></i>"):
                with self.subTest(field=name, value=value):
                    response = self.client.post(
                        self.list_url, {**self.payload, name: value}, format="json",
                    )
                    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                    self.assertIn(name, response.data)
        self.assertEqual(self.snapshot(), before)

    def test_computed_star_fields_are_read_only(self):
        self.as_user(self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.user.pk],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertFalse(self.model.objects.get(pk=response.data["id"]).starred_by.exists())

    # ---------- star ----------

    def test_guest_cannot_star(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(self.item.starred_by.exists())

    def test_star_toggles_for_request_user_only(self):
        for user in (self.user, self.editor, self.owner):
            with self.subTest(user=user.username):
                self.as_user(user)
                # Mencoba "menitipkan" user lain lewat body harus diabaikan
                response = self.client.post(self.star_url, {"user": self.owner.pk}, format="json")
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertTrue(response.data["is_starred"])
                self.assertTrue(self.item.starred_by.filter(pk=user.pk).exists())
                response = self.client.post(self.star_url)
                self.assertFalse(response.data["is_starred"])
                self.assertFalse(self.item.starred_by.filter(pk=user.pk).exists())
        self.assertFalse(self.item.starred_by.exists())

    def test_star_status_is_specific_to_viewer(self):
        self.item.starred_by.add(self.user)
        self.as_user(self.user)
        self.assertTrue(self.client.get(self.detail_url).data["is_starred"])
        self.as_user(self.editor)
        data = self.client.get(self.detail_url).data
        self.assertFalse(data["is_starred"])
        self.assertEqual(data["star_count"], 1)
        self.assertEqual(data["starred_by_names"], "member")

    # ---------- CSRF dengan session sungguhan ----------

    def test_session_write_without_csrf_token_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password=PASSWORD))
        before = self.snapshot()
        response = client.post(self.list_url, self.payload, format="json")
        self.assert_denied_without_change(response, before)
        self.assertIn("CSRF", str(response.data["detail"]))
        response = client.patch(self.detail_url, {"title": "No token"}, format="json")
        self.assert_denied_without_change(response, before)

    def test_session_write_with_token_from_page_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="editor", password=PASSWORD))
        # Halaman bagian ini harus menyetel cookie csrftoken untuk Editor
        page = client.get(reverse(self.page))
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.patch(
            self.detail_url, {"title": "With token"}, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, "With token")


class ExperienceAPITest(PortfolioSectionAPITestMixin, APITestCase):
    model = Experience
    route = "experience"
    page = "main:show_experiences"
    initial = {
        "title": "Teaching Assistant", "organization": "Faculty of Computer Science",
        "description": "Assisted labs.", "category": "Teaching", "start_year": 2024,
    }
    payload = {
        "title": "Research Assistant", "title_id": "Asisten Riset",
        "organization": "AI Lab", "organization_id": "Lab AI",
        "description": "Built models.", "description_id": "Membangun model.",
        "category": "Research", "start_year": 2025, "end_year": 2026,
    }
    search_hit = "computer science"
    text_fields = (
        "title", "title_id", "organization", "organization_id",
        "description", "description_id", "category",
    )
    required_fields = ("title", "organization", "description", "category")

    def test_year_rules(self):
        self.as_user(self.owner)
        for changes in ({"start_year": 1800}, {"end_year": 2200}, {"start_year": 2025, "end_year": 2020}):
            with self.subTest(changes=changes):
                response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # PATCH end_year saja tetap dibandingkan dengan start_year yang tersimpan
        response = self.client.patch(self.detail_url, {"end_year": 2020}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("end_year", response.data)
        self.item.refresh_from_db()
        self.assertIsNone(self.item.end_year)
        # end_year kosong berarti masih berlangsung
        response = self.client.post(self.list_url, {**self.payload, "end_year": None}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_is_ordered_by_latest_start_year(self):
        newer = Experience.objects.create(**{**self.initial, "start_year": 2026})
        ids = [item["id"] for item in self.client.get(self.list_url).data]
        self.assertEqual(ids, [newer.pk, self.item.pk])


class AchievementAPITest(PortfolioSectionAPITestMixin, APITestCase):
    model = Achievement
    route = "achievement"
    page = "main:show_achievements"
    initial = {
        "title": "Data Science Olympiad", "result": "National finalist",
        "category": "Competition", "year": 2025,
    }
    payload = {
        "title": "Programming Contest", "title_id": "Kontes Pemrograman",
        "result": "Winner", "result_id": "Juara", "category": "Competition",
        "year": 2026, "display_order": 2,
    }
    search_hit = "national"
    text_fields = ("title", "title_id", "result", "result_id", "category")
    required_fields = ("title", "result", "category")

    def test_year_and_display_order_rules(self):
        self.as_user(self.owner)
        for changes in ({"year": 1800}, {"year": 2200}, {"display_order": -1}):
            with self.subTest(changes=changes):
                response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # year boleh kosong; display_order memakai default model bila tidak dikirim
        data = {key: value for key, value in self.payload.items() if key != "display_order"}
        response = self.client.post(self.list_url, {**data, "year": None}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["year"])
        self.assertEqual(response.data["display_order"], 0)

    def test_list_follows_display_order(self):
        first = Achievement.objects.create(**{**self.initial, "title": "Zeta", "display_order": 0})
        self.item.display_order = 5
        self.item.save()
        ids = [item["id"] for item in self.client.get(self.list_url).data]
        self.assertEqual(ids, [first.pk, self.item.pk])
