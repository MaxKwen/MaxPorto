"""Public view imports retained for URL configurations and callers."""

from main.copy import ACHIEVEMENT_COPY, EXPERIENCE_COPY, PROJECT_COPY, SKILL_COPY
from main.permissions import is_editor
from .auth import (
    register,
    login_user,
    logout_user,
)
from .projects import (
    toggle_project_star,
    get_projects_json,
    show_projects,
    create_project,
    update_project,
    delete_project,
    create_project_ajax,
)
from .experiences import (
    get_experiences_json,
    show_experiences,
    toggle_experience_star,
    create_experience,
    create_experience_ajax,
    update_experience,
    delete_experience,
)
from .achievements import (
    get_achievements_json,
    show_achievements,
    create_achievement_ajax,
    toggle_achievement_star,
    create_achievement,
    update_achievement,
    delete_achievement,
)
from .skills import (
    show_skills,
)

__all__ = [
    "ACHIEVEMENT_COPY",
    "EXPERIENCE_COPY",
    "PROJECT_COPY",
    "SKILL_COPY",
    "is_editor",

    "register",
    "login_user",
    "logout_user",
    "toggle_project_star",
    "get_projects_json",
    "show_projects",
    "create_project",
    "update_project",
    "delete_project",
    "create_project_ajax",
    "get_experiences_json",
    "show_experiences",
    "toggle_experience_star",
    "create_experience",
    "create_experience_ajax",
    "update_experience",
    "delete_experience",
    "get_achievements_json",
    "show_achievements",
    "create_achievement_ajax",
    "toggle_achievement_star",
    "create_achievement",
    "update_achievement",
    "delete_achievement",
    "show_skills",
]
