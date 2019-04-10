"""
Contains some common functions of the related app
to store and retrieve data from database.
"""
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from openedx.features.openedx_nodebb_discussion.models import EdxNodeBBUser, EdxNodeBBCategory


def save_user_relation_into_db(username, nodebb_uid):
    """
    Saves NodeBB uid against edx_userid in EdxNodeBBUser table.

    Args:
        username (str): edX username of user
        nodebb_uid (int): NodeBB uid for edX user
    """
    relation = EdxNodeBBUser()
    relation.edx_uid = get_object_or_404(User, username=username)
    relation.nodebb_uid = nodebb_uid
    relation.save()


def get_nodebb_uid_from_username(username):
    """
    Extract nodebb_uid from table EdxNodeBBUser using username.

    Args:
        username (str): edX username of user

    Returns:
        int: returns nodebb_uid get from model
    """
    edx_user = get_object_or_404(User, username=username)
    user_relation = get_object_or_404(EdxNodeBBUser, edx_uid=edx_user)
    return user_relation.nodebb_uid


def save_category_relation_into_db(course_id, category_id):
    """
    Saves NodeBB cid against edx_courseid in EdxNodeBBCategory table.

    Args:
        course_id: Course Key of course for which category is created.
        category_id: NodeBB cid for edX course.
    """
    category_relation = EdxNodeBBCategory()
    category_relation.course_key = course_id
    category_relation.nodebb_cid = category_id
    category_relation.save()


def save_group_relation_into_db(course_id, group_slug, group_name):
    """
    Saves NodeBB group_slug against edx_courseid in EdxNodeBBCategory table.

    Args:
        course_id: Course Key of course for which category is created.
        group_slug: NodeBB group_slug for edX course.
        group_name: NodeBB group_name for edX course.
    """
    group_relation = get_object_or_404(EdxNodeBBCategory, course_key=course_id)
    group_relation.nodebb_group_slug = group_slug
    group_relation.nodebb_group_name = group_name
    group_relation.save()


def get_category_id_from_course_id(course_id):
    """
    Extract nodebb_cid from table EdxNodeBBCategory using course_id.

    Args:
        course_id (Course Key): Course Key of edX Course for which cid is require.

    Returns:
        int: returns nodebb_cid get from model
    """
    category_relation = get_object_or_404(EdxNodeBBCategory, course_key=course_id)
    return category_relation.nodebb_cid


def get_group_slug_from_course_id(course_id):
    """
    Extract group_slug from table EdxNodeBBCategory using course_id.

    Args:
        course_id (Course Key): Course Key of edX Course for which group_slug is require.

    Returns:
        str: returns nodebb_group_slug get from model
    """
    category_relation = get_object_or_404(EdxNodeBBCategory, course_key=course_id)
    return category_relation.nodebb_group_slug


def get_group_slug_from_category_id(category_id):
    """
    Extract group_slug from table EdxNodeBBCategory using course_id.

    Args:
        category_id (int): nodebb_cid for edX Course for which group_slug is require.

    Returns:
        str: returns nodebb_group_slug get from model
    """
    category_relation = get_object_or_404(EdxNodeBBCategory, nodebb_cid=category_id)
    return category_relation.nodebb_group_slug


def get_group_name_from_course_id(course_id):
    """
    Extract group_name from table EdxNodeBBCategory using course_id.

    Args:
      course_id (Course Key): Course Key of edX Course for which group_name is require.

    Returns:
        str: returns nodebb_group_name get from model
    """
    category_relation = get_object_or_404(EdxNodeBBCategory, course_key=course_id)
    return category_relation.nodebb_group_name
