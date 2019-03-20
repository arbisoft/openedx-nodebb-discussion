# -*- coding: utf-8 -*-

from django.apps import AppConfig


class OpenedxNodebbDiscussionConfig(AppConfig):
    """
        Application Configuration for OPENEDX_NODEBB_DISCUSSION.
    """
    name = 'openedx.features.openedx_nodebb_discussion'

    def ready(self):
        from django.conf import settings
        settings.MIDDLEWARE_CLASSES.append(
            'openedx.features.openedx_nodebb_discussion.middleware.UserSessionSharingMiddleware')
