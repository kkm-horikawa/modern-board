"""API application configuration."""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Configuration for the API application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    verbose_name = "API"
