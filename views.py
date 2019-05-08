from courseware.courses import get_course_with_access, has_access
from django.conf import settings as django_settings
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from django_comment_client.utils import has_discussion_privileges
from opaque_keys.edx.keys import CourseKey
from openedx.features.openedx_edly_discussion.client.utils import get_category_id_from_course_id
from student.models import CourseEnrollment


class EdlyDiscussionDashboardView(TemplateView):
    """
    View methods related to the Edly Discussion dashboard.
    """

    def get(self, request, course_id):
        """
        Renders the EDLY DISCUSSION dashboard, which is shown on the EDLY DISCUSSION
        tab. Raises a 404 if the course specified by course_id does not exist, the
        user is not registered for the course, or the EDLY DISCUSSION feature is not enabled.
        """
        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, 'load', course_key)
        category_id = get_category_id_from_course_id(course_key)
        if not CourseEnrollment.is_enrolled(request.user, course.id) and \
                not has_access(request.user, 'staff', course, course.id):
            raise Http404

        user = request.user
        context = {
            'course': course,
            'edly_discussion_url': django_settings.EDLY_DISCUSSION_SETTINGS['URL'],
            'category_id': category_id,
            'user_info': {
                'username': user.username,
                'privileged': has_discussion_privileges(user, course_key),
                'staff': bool(has_access(user, 'staff', course_key)),
            },
        }
        return render_to_response('openedx_edly_discussion/dashboard.html', context)
