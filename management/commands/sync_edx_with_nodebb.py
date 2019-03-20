"""
Django management command to sync edX with NodeBB.
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """
    This command syncs the edX with NodeBB using the other custom commands.

    Example usage:
        manage.py ... sync_edx_with_nodebb
    """

    def handle(self, *args, **options):
        call_command('sync_users_with_nodebb')
        call_command('sync_courses_with_nodebb')
        call_command('sync_course_enrollments_with_nodebb')
