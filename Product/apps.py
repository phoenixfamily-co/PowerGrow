from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Product'

    def ready(self):
        from . import jobs
        jobs.start()