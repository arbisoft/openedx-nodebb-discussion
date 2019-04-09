"""
Django management command to sync edx with nodebb.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = """
    This command syncs the edx with nodebb using the other custom commands.

    example:
        manage.py ... sync_edx_with_nodebb
    """

    def handle(self, *args, **options):
        call_command('sync_users_with_nodebb')
        call_command('sync_courses_with_nodebb')
        call_command('sync_course_enrollments_with_nodebb')
