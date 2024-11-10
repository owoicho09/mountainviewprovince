from django.apps import AppConfig


class StudentauthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "studentauth"

    def ready(self):
        import studentauth.signals