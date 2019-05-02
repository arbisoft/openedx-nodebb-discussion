"""
Django management command to join groups at NodeBB corresponding to edX course enrollments.
"""
from logging import getLogger

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from openedx.features.openedx_nodebb_discussion.client.tasks import task_join_group_on_nodebb
from openedx.features.openedx_nodebb_discussion.models import EdxNodeBBCategory, EdxNodeBBEnrollment
from student.models import CourseEnrollment

log = getLogger(__name__)


class Command(BaseCommand):
    help = """
    This command creates user membership in groups of NodeBB based on user enrollments in edX courses

    Example usage:
        manage.py ... sync_course_enrollments_with_nodebb
    """

    def handle(self, *args, **options):
        enrollments = CourseEnrollment.objects.filter(is_active=True)
        for enrollment in enrollments:
            category_relation = EdxNodeBBCategory.objects.filter(course_key=enrollment.course_id)
            if category_relation:
                edx_user = User.objects.filter(username=enrollment.username).first()
                enrollment_relation = EdxNodeBBEnrollment.objects.filter(edx_uid=edx_user, course_key=enrollment.course_id)
                if not enrollment_relation:
                    course_data = {
                        'organization': enrollment.course_id.org,
                        'course_name': enrollment.course_id.course,
                        'course_run': enrollment.course_id.run,
                    }
                    task_join_group_on_nodebb.delay(enrollment.username, **course_data)

        log.info('Command has been executed.')
