from django.apps import AppConfig


class OpenedxEdlyDiscussionConfig(AppConfig):
    """
    Application Configuration for OPENEDX_EDLY_DISCUSSION.
    """
    name = 'openedx.features.openedx_edly_discussion'

    def ready(self):
        from openedx.features.openedx_edly_discussion.client.signals import handlers
        from django.conf import settings as django_settings
        if hasattr(django_settings, 'MIDDLEWARE_CLASSES'):
            django_settings.MIDDLEWARE_CLASSES.append(
                'openedx.features.openedx_edly_discussion.middleware.UserSessionSharingMiddleware'
            )
