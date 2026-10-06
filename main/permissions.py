"""Shared portfolio permission helpers."""


def is_editor(user):
    return user.is_authenticated and user.groups.filter(name="Editor").exists()
