# -*- coding: utf-8 -*-

from django.apps import AppConfig


class OpenedxNodebbDiscussionConfig(AppConfig):
    """
    Application Configuration for OPENEDX_NODEBB_DISCUSSION.
    """
    name = 'openedx.features.openedx_nodebb_discussion'

    def ready(self):
        from openedx.features.openedx_nodebb_discussion.client.signals import handlers
        from django.conf import settings as django_settings
        if hasattr(django_settings, 'MIDDLEWARE_CLASSES'):
            django_settings.MIDDLEWARE_CLASSES.append(
                'openedx.features.openedx_nodebb_discussion.middleware.UserSessionSharingMiddleware'
            )
