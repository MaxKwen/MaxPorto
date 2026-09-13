from django.test import TestCase
from django.urls import reverse

from main.models import Project


class ProjectPageTest(TestCase):
    def test_project_page_uses_projects_template(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_homepage_links_to_project_page(self):
        response = self.client.get(reverse("landing_page"))

        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

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
