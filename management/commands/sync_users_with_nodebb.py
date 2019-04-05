"""
Django management command to create users at nodeBB corresponding to edx-platform users.
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from openedx.features.openedx_nodebb_discussion.client.tasks import task_create_user_on_nodebb
from openedx.features.openedx_nodebb_discussion.models import NodeBBUserRelation


class Command(BaseCommand):
    help = """
    This command creates users in nodeBB according to all UserExtendedProfile instances in edx-platform.

    example:
        manage.py ... create_nodebb_users
    """

    def handle(self, *args, **options):
        nodebb_relations = NodeBBUserRelation.objects.all()
        edx_users = User.objects.all()
        for edx_user in edx_users:
            nodebb_user = nodebb_relations.filter(edx_uid=edx_user)
            if not nodebb_user:
                user_data = {
                    'username': edx_user.username,
                    'email': edx_user.email,
                    'joindate': edx_user.date_joined.strftime("%s")
                }
                task_create_user_on_nodebb.delay(**user_data)
