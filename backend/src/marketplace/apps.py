from django.apps import AppConfig


class MarketplaceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "marketplace"

    def ready(self) -> None:
        """Connect signal handlers when the app is ready."""
        from marketplace import signals

        # The signals module is imported but unused. However, the very act of
        # importing it causes the signal receivers to be registered with Django's
        # signal dispatcher. This is a common Django pattern.
        _ = signals
