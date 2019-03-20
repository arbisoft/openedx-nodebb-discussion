from courseware.tabs import EnrolledTab
from django.utils.translation import ugettext_noop
from django.conf import settings


class NodeBBTab(EnrolledTab):
    """A new course tab."""

    name = "openedx_nodebb_discussion"
    type = "openedx_nodebb_discussion"
    title = ugettext_noop("NodeBB Discussion")
    view_name = "nodebb_dashboard"

    @classmethod
    def is_enabled(cls, course, user=None):
        if not super(NodeBBTab, cls).is_enabled(course, user):
            return False

        return settings.FEATURES.get('ENABLE_NODEBB_DISCUSSION', False)
