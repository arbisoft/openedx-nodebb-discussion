"""
Django management command to join groups at NodeBB corresponding to edX course enrollments.
"""
from logging import getLogger

from django.core.management.base import BaseCommand
from openedx.features.openedx_nodebb_discussion.client.tasks import task_join_group_on_nodebb
from openedx.features.openedx_nodebb_discussion.models import EdxNodeBBCategory
from student.models import CourseEnrollment

log = getLogger(__name__)


class Command(BaseCommand):
    help = """
    This command create user membership in group of NodeBB based on user enrollments in edX courses

    Example usage:
        manage.py ... sync_course_enrollments_with_nodebb
    """

    def handle(self, *args, **options):
        enrollments = CourseEnrollment.objects.filter(is_active=True)
        for enrollment in enrollments:
            category_relation = EdxNodeBBCategory.objects.filter(course_key=enrollment.course_id)
            if category_relation:
                task_join_group_on_nodebb.delay(enrollment.username, enrollment.course_id)

        log.info('Command has been executed.')
