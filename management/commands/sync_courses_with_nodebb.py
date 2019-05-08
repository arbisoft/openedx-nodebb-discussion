"""
Django management command to create categories at NodeBB corresponding to edX courses.
"""
from logging import getLogger

from django.core.management.base import BaseCommand
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.features.openedx_edly_discussion.client.tasks import task_create_category_on_nodebb
from openedx.features.openedx_edly_discussion.models import EdxNodeBBCategory

log = getLogger(__name__)


class Command(BaseCommand):
    help = """
    This command creates categories in NodeBB corresponding to all Courses in edX.

    Example usage:
        manage.py ... sync_courses_with_nodebb
    """

    def handle(self, *args, **options):
        edx_courses = CourseOverview.objects.all()
        nodebb_categories = EdxNodeBBCategory.objects.all()
        for edx_course in edx_courses:
            category_relation = nodebb_categories.filter(course_key=edx_course.id)
            if not category_relation:
                course_data = {
                    'organization': edx_course.id.org,
                    'course_name': edx_course.id.course,
                    'course_run': edx_course.id.run,
                    'display_name': edx_course.display_name
                }
                task_create_category_on_nodebb.delay(course_display_name=edx_course.display_name, **course_data)
        log.info('Command has been executed')
