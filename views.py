from courseware.courses import get_course_with_access, has_access
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from django_comment_client.utils import has_discussion_privileges
from opaque_keys.edx.keys import CourseKey
from student.models import CourseEnrollment

from . import is_feature_enabled


class NodebbDashboardView(TemplateView):
    """
    View methods related to the nodebb dashboard.
    """

    def get(self, request, course_id):
        """
        Renders the teams dashboard, which is shown on the "Teams" tab.
        Raises a 404 if the course specified by course_id does not exist, the
        user is not registered for the course, or the teams feature is not enabled.
        """
        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, "load", course_key)

        if not is_feature_enabled():
            raise Http404

        if not CourseEnrollment.is_enrolled(request.user, course.id) and \
                not has_access(request.user, 'staff', course, course.id):
            raise Http404

        user = request.user

        context = {
            "course": course,
            "user_info": {
                "username": user.username,
                "privileged": has_discussion_privileges(user, course_key),
                "staff": bool(has_access(user, 'staff', course_key)),
            },
        }
        return render_to_response("openedx_nodebb_discussion/nodebb.html", context)
