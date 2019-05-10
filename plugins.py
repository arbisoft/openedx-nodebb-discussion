from courseware.tabs import EnrolledTab
from django.conf import settings
from django.utils.translation import ugettext_noop


class NodeBBTab(EnrolledTab):
    """
    NodeBBTab for Courses it will contain the embeded view of NodeBB Forum
    """
    # TODO: Edx Currently Using type as a Tab_Type but it is a keyword so change it. If found some better way.
    name = 'openedx_nodebb_discussion'
    type = 'openedx_nodebb_discussion'
    title = ugettext_noop('NodeBB Discussion')
    view_name = 'nodebb_dashboard'

    @classmethod
    def is_enabled(cls, course, user=None):
        if not super(NodeBBTab, cls).is_enabled(course, user):
            return False

        return settings.FEATURES.get('ENABLE_NODEBB_DISCUSSION', False)
