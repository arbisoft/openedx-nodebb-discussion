default_app_config = 'openedx.features.openedx_nodebb_discussion.apps.OpenedxNodebbDiscussionConfig'

from django.conf import settings


def is_feature_enabled():
    """
    Returns True if the NodeBB feature is enabled.
    """
    return settings.FEATURES.get('ENABLE_NODEBB_DISCUSSION', False)
