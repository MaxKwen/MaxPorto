from django.test import TestCase
from django.urls import reverse

from main.models import Achievement, Experience, Project, Skill


class ProjectPageTest(TestCase):
    def test_project_page_uses_projects_template(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_homepage_links_to_project_page(self):
        response = self.client.get(reverse("landing_page"))

        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

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

    def test_homepages_link_to_matching_experience_pages(self):
        english_response = self.client.get(reverse("landing_page"))
        indonesian_response = self.client.get(reverse("landing_page_id"))

        self.assertContains(
            english_response,
            f'href="{reverse("main:show_experiences")}"',
        )
        self.assertContains(
            indonesian_response,
            f'href="{reverse("main:show_experiences_id")}"',
        )

    def test_experience_data_appears_on_page(self):
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

        response = self.client.get(reverse("main:show_experiences"))

        self.assertContains(response, experience.title)
        self.assertContains(response, experience.organization)
        self.assertContains(response, experience.description)
        self.assertContains(response, experience.category)
        self.assertContains(response, "2026 — present")

    def test_indonesian_page_uses_indonesian_content(self):
        experience = Experience.objects.create(
            title="Staff, Data Science Academy",
            title_id="Staf, Data Science Academy",
            organization="COMPFEST, University of Indonesia",
            organization_id="COMPFEST, Universitas Indonesia",
            description="Coordinated speakers and mentors.",
            description_id="Mengoordinasikan pembicara dan mentor.",
            category="Organization",
            start_year=2026,
        )

        response = self.client.get(reverse("main:show_experiences_id"))

        self.assertContains(response, experience.title_id)
        self.assertContains(response, experience.organization_id)
        self.assertContains(response, experience.description_id)
        self.assertContains(response, "2026 — sekarang")
        self.assertNotContains(response, experience.description)

    def test_experience_page_shows_empty_state_without_data(self):
        response = self.client.get(reverse("main:show_experiences"))

        self.assertContains(response, "No experience has been added yet.")

    def test_homepage_does_not_duplicate_experience_cards(self):
        response = self.client.get(reverse("landing_page"))

        self.assertNotContains(
            response,
            "Teaching Assistant, Intro to Digital System",
        )


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


class ContactRemovalTest(TestCase):
    def test_contact_section_and_navigation_are_removed_from_all_pages(self):
        page_names = [
            "landing_page",
            "landing_page_id",
            "main:show_projects",
            "main:show_projects_id",
            "main:show_experiences",
            "main:show_experiences_id",
            "main:show_skills",
            "main:show_skills_id",
            "main:show_achievements",
            "main:show_achievements_id",
        ]

        for page_name in page_names:
            with self.subTest(page_name=page_name):
                response = self.client.get(reverse(page_name))
                self.assertNotContains(response, 'id="contact"')
                self.assertNotContains(response, "#contact")
                self.assertNotContains(response, ">Contact<")
                self.assertNotContains(response, ">Kontak<")
