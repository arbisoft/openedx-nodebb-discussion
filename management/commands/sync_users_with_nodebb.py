"""
Django management command to create users at NodeBB corresponding to edX users.
"""
from logging import getLogger

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from openedx.features.openedx_edly_discussion.client.tasks import (
    task_create_user_on_nodebb,
    task_update_user_profile_on_nodebb
)
from openedx.features.openedx_edly_discussion.models import EdxNodeBBUser
from student.models import UserProfile

log = getLogger(__name__)


class Command(BaseCommand):
    help = """
    This command creates users in NodeBB according to all User and UserProfile instances in edX.

    Example usage:
        manage.py ... sync_users_with_nodebb
    """

    def handle(self, *args, **options):
        nodebb_relations = EdxNodeBBUser.objects.all()
        edx_users = User.objects.all()
        user_profiles = UserProfile.objects.all()

        for edx_user in edx_users:
            nodebb_user = nodebb_relations.filter(edx_uid=edx_user)
            if not nodebb_user:
                user_data = {
                    'username': edx_user.username,
                    'email': edx_user.email,
                    'joindate': edx_user.date_joined.strftime("%s")
                }
                task_create_user_on_nodebb.delay(**user_data)

                profile = user_profiles.filter(user=edx_user).first()
                if profile:
                    profile_data = {
                        'fullname': profile.name,
                        'location': '{}, {}'.format(
                            profile.city, profile.country.name),
                        'birthday': '01/01/%s' % profile.year_of_birth
                    }
                    task_update_user_profile_on_nodebb.delay(username=edx_user.username, **profile_data)
        log.info('Command has been executed.')
