"""Guard the feature-based template, stylesheet, and view layout."""

from html.parser import HTMLParser
from importlib import import_module

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.test import TestCase
from django.urls import resolve, reverse


class PageMarkup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stylesheets = []
        self.main_count = 0
        self.title_count = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and attrs.get("rel") == "stylesheet":
            href = attrs.get("href", "")
            if href.startswith("/static/"):
                self.stylesheets.append(href.removeprefix("/static/"))
        if tag == "main":
            self.main_count += 1
        if tag == "title":
            self.title_count += 1


class FeatureStructureTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create(
            username="structure-owner", is_superuser=True
        )

    def test_pages_load_shared_and_only_their_own_stylesheets(self):
        pages = [
            ("landing_page", "home/index.html", ["home"]),
            ("landing_page_id", "home/index.html", ["home"]),
            ("main:show_projects", "projects/list.html", ["forms", "projects"]),
            ("main:show_projects_id", "projects/list.html", ["forms", "projects"]),
            ("main:show_experiences", "experiences/list.html", ["forms", "experiences"]),
            ("main:show_experiences_id", "experiences/list.html", ["forms", "experiences"]),
            ("main:show_achievements", "achievements/list.html", ["forms", "achievements"]),
            ("main:show_achievements_id", "achievements/list.html", ["forms", "achievements"]),
            ("main:show_skills", "skills/list.html", ["skills"]),
            ("main:show_skills_id", "skills/list.html", ["skills"]),
            ("main:login", "auth/login.html", ["forms"]),
            ("main:register", "auth/register.html", ["forms"]),
            ("main:create_project", "projects/form.html", ["forms"]),
            ("main:create_experience", "experiences/form.html", ["forms"]),
            ("main:create_achievement", "achievements/form.html", ["forms"]),
        ]
        for user in [None, self.owner]:
            self.client.logout()
            if user:
                self.client.force_login(user)
            for route, template, styles in pages:
                if route.startswith("main:create_") and not user:
                    continue
                with self.subTest(user=user, route=route):
                    response = self.client.get(reverse(route))
                    self.assertEqual(response.status_code, 200)
                    self.assertTemplateUsed(response, template)
                    markup = PageMarkup()
                    markup.feed(response.content.decode())
                    expected = [f"css/{name}.css" for name in ["base", "components", *styles]]
                    self.assertEqual(markup.stylesheets, expected)
                    for asset in expected:
                        self.assertIsNotNone(finders.find(asset), asset)
                    self.assertEqual(markup.main_count, 1)
                    self.assertEqual(markup.title_count, 1)

    def test_every_template_compiles_including_unreferenced_components(self):
        template_root = settings.BASE_DIR / "templates"
        for path in template_root.rglob("*.html"):
            name = path.relative_to(template_root).as_posix()
            with self.subTest(template=name):
                get_template(name)

    def test_routes_point_to_feature_modules_and_public_imports_remain_valid(self):
        modules = {
            "auth": ["register", "login_user", "logout_user"],
            "projects": [
                "show_projects", "get_projects_json", "create_project",
                "create_project_ajax", "update_project", "delete_project",
                "toggle_project_star",
            ],
            "experiences": [
                "show_experiences", "get_experiences_json", "create_experience",
                "create_experience_ajax", "update_experience", "delete_experience",
                "toggle_experience_star",
            ],
            "achievements": [
                "show_achievements", "get_achievements_json", "create_achievement",
                "create_achievement_ajax", "update_achievement", "delete_achievement",
                "toggle_achievement_star",
            ],
            "skills": ["show_skills"],
        }
        public_views = import_module("main.views")
        for feature, names in modules.items():
            module = import_module(f"main.views.{feature}")
            for name in names:
                with self.subTest(view=name):
                    self.assertIs(getattr(public_views, name), getattr(module, name))
        for route, feature in [
            ("main:login", "auth"),
            ("main:show_projects", "projects"),
            ("main:show_experiences", "experiences"),
            ("main:show_achievements", "achievements"),
            ("main:show_skills", "skills"),
        ]:
            self.assertEqual(resolve(reverse(route)).func.__module__, f"main.views.{feature}")
