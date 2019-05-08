from courseware.tabs import EnrolledTab
from django.conf import settings
from django.utils.translation import ugettext_noop


class EdlyTab(EnrolledTab):
    """
    EdlyTab for Courses it will contain the embeded view of Edly Forum
    """
    # TODO: Edx Currently Using type as a Tab_Type but it is a keyword so change it. If found some better way.
    name = 'openedx_edly_discussion'
    type = 'openedx_edly_discussion'
    title = ugettext_noop('Discussion')
    view_name = 'edly_discussion_dashboard'

    @classmethod
    def is_enabled(cls, course, user=None):
        if not super(EdlyTab, cls).is_enabled(course, user):
            return False

        return settings.FEATURES.get('ENABLE_EDLY_DISCUSSION', False)
