from django.apps import AppConfig


class ThemeConfig(AppConfig):
    name = 'theme'

    def ready(self):
        import theme.signals
