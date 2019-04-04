from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from openedx.features.openedx_nodebb_discussion.models import NodeBBUserRelation


def save_relation_into_db(username, nodebb_uid):
    relation = NodeBBUserRelation()
    relation.edx_uid = get_object_or_404(User, username=username)
    relation.nodebb_uid = nodebb_uid
    relation.save()


def get_nodebb_uid_from_username(username):
    edx_user = get_object_or_404(User, username=username)
    user_relation = get_object_or_404(NodeBBUserRelation, edx_uid=edx_user)
    return user_relation.nodebb_uid
