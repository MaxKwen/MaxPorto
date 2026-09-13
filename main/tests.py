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


class ProjectModelTest(TestCase):
    def test_project_stores_portfolio_data(self):
        project = Project.objects.create(
            title="Kusut-Kusut",
            description="Backend Django untuk interaksi sosial.",
            category="Backend",
            project_url="https://github.com/MaxKwen/kusutkusut-backend",
            thumbnail="https://example.com/kusut-kusut.png",
        )

        self.assertEqual(str(project), "Kusut-Kusut")
        self.assertEqual(project.category, "Backend")
        self.assertFalse(project.is_featured)
