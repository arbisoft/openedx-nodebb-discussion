"""
Django management command to create categories at nodeBB corresponding to edx-platform courses.
"""
from django.core.management.base import BaseCommand
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.features.openedx_nodebb_discussion.client.tasks import task_create_category_on_nodebb
from openedx.features.openedx_nodebb_discussion.models import NodeBBCategoryRelation


class Command(BaseCommand):
    help = """
    This command creates categories in nodeBB according to all Courses in edx-platform.

    example:
        manage.py ... sync_courses_with_nodebb
    """

    def handle(self, *args, **options):
        edx_courses = CourseOverview.objects.all()
        nodebb_categories = NodeBBCategoryRelation.objects.all()

        for edx_course in edx_courses:
            category_relation = nodebb_categories.filter(course_key=edx_course.id)
            if not category_relation:
                category_data = {
                    'name': '{}-{}-{}-{}'.format(
                        edx_course.display_name, edx_course.id.org, edx_course.id.course,
                        edx_course.id.run
                    ),
                }
                task_create_category_on_nodebb.delay(course_id=edx_course.id, **category_data)
