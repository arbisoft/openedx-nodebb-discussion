"""
Django management command to create users at nodeBB corresponding to edx-platform users.
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from student.models import UserProfile
from openedx.features.openedx_nodebb_discussion.client.tasks import (
    task_create_user_on_nodebb, task_sync_user_profile_info_with_nodebb
)
from openedx.features.openedx_nodebb_discussion.models import NodeBBUserRelation


class Command(BaseCommand):
    help = """
    This command creates users in nodeBB according to all User and UserProfile instances in edx-platform.

    example:
        manage.py ... sync_users_with_nodebb
    """

    def handle(self, *args, **options):
        nodebb_relations = NodeBBUserRelation.objects.all()
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

                profile = user_profiles.filter(user=edx_user)
                if profile:
                    profile_data = {
                        'fullname': profile[0].name,
                        'location': '{}, {}'.format(
                            profile[0].city, profile[0].country.name),
                        'birthday': '01/01/%s' % profile[0].year_of_birth
                    }
                    task_sync_user_profile_info_with_nodebb.delay(username=edx_user.username, **profile_data)
