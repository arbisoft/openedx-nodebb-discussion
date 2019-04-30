"""
Contains some common functions of the related app
to store and retrieve data from database.
"""
from django.contrib.auth.models import User
from openedx.features.openedx_nodebb_discussion.models import (
    EdxNodeBBUser, EdxNodeBBCategory, EdxNodeBBEnrollment,
)


def save_user_relation_into_db(username, nodebb_uid):
    """
    Saves NodeBB uid against edx_userid in EdxNodeBBUser table.

    Args:
        username (str): edX username of user
        nodebb_uid (int): NodeBB uid for edX user
    """
    edx_user = User.objects.filter(username=username).first()

    if edx_user:
        relation = EdxNodeBBUser()
        relation.edx_uid = edx_user
        relation.nodebb_uid = nodebb_uid
        relation.save()


def get_nodebb_uid_from_username(username):
    """
    Extracts nodebb_uid from table EdxNodeBBUser using username.

    Args:
        username (str): edX username of user

    Returns:
        int: returns nodebb_uid get from model
    """
    user_relation = EdxNodeBBUser.objects.filter(edx_uid__username=username).first()

    if user_relation:
        return user_relation.nodebb_uid

    return None


def save_category_relation_into_db(course_id, category_id):
    """
    Saves NodeBB cid against edx_courseid in EdxNodeBBCategory table.

    Args:
        course_id (CourseKey): CourseKey of course for which category is created.
        category_id (int): NodeBB cid for edX course.
    """
    category_relation = EdxNodeBBCategory()
    category_relation.course_key = course_id
    category_relation.nodebb_cid = category_id
    category_relation.save()


def save_group_relation_into_db(course_id, group_slug, group_name):
    """
    Saves NodeBB group_slug against edx_courseid in EdxNodeBBCategory table.

    Args:
        course_id (CourseKey): Id of course for which category is created.
        group_slug (str): NodeBB group_slug for edX course.
        group_name (str): NodeBB group_name for edX course.
    """
    
    group_relation = EdxNodeBBCategory.objects.filter(course_key=course_id).first()

    if group_relation:
        group_relation.nodebb_group_slug = group_slug
        group_relation.nodebb_group_name = group_name
        group_relation.save()


def get_category_id_from_course_id(course_id):
    """
    Extracts nodebb_cid from table EdxNodeBBCategory using course_id.

    Args:
        course_id (CourseKey): Id of edX Course for which cid is required.

    Returns:
        int: returns nodebb_cid get from model
    """
    category_relation = EdxNodeBBCategory.objects.filter(course_key=course_id).first()

    if category_relation:
        return category_relation.nodebb_cid

    return None


def get_group_slug_from_course_id(course_id):
    """
    Extracts group_slug from table EdxNodeBBCategory using course_id.

    Args:
        course_id (CourseKey): Id of edX Course for which group_slug is required.

    Returns:
        str: returns nodebb_group_slug get from model
    """
    category_relation = EdxNodeBBCategory.objects.filter(course_key=course_id).first()

    if category_relation:
        return category_relation.nodebb_group_slug

    return None


def get_group_slug_from_category_id(category_id):
    """
    Extracts group_slug from table EdxNodeBBCategory using course_id.

    Args:
        category_id (int): nodebb_cid for edX Course for which group_slug is required.

    Returns:
        str: returns nodebb_group_slug get from model
    """
    category_relation = EdxNodeBBCategory.objects.filter(nodebb_cid=category_id).first()

    if category_relation:
        return category_relation.nodebb_group_slug

    return None


def get_group_name_from_course_id(course_id):
    """
    Extracts group_name from table EdxNodeBBCategory using course_id.

    Args:
      course_id (CourseKey): Id of edX Course for which group_name is required.

    Returns:
        str: returns nodebb_group_name get from model
    """
    category_relation = EdxNodeBBCategory.objects.filter(course_key=course_id).first()

    if category_relation:
        return category_relation.nodebb_group_name

    return None


def get_course_id_from_group_slug(group_slug):
    """
    Extracts course id from table EdxNodeBBCategory using group_slug.

    Args:
        group_slug (str): NodeBB group_slug for edX course.

    Returns:
        CourseKey: returns course_id stored in the model corresponding to group_slug        
    """
    category_relation = EdxNodeBBCategory.objects.filter(nodebb_group_slug=group_slug).first()

    if category_relation:
        return category_relation.course_key
    
    return None


def get_edx_user_from_nodebb_uid(nodebb_uid):
    """
    Extracts edx user from table EdxNodeBBUser using nodebb_uid.

    Args:
        nodebb_uid (int): NodeBB uid for edx user.

    Returns:
        User: returns edx user storted in the model corresponding to nodebb_uid.
    """
    user_relation = EdxNodeBBUser.objects.filter(nodebb_uid=nodebb_uid).first()

    if user_relation:
        return user_relation.edx_uid

    return None    


def save_course_enrollment_in_db(edx_user, course_id):
    """
    Saves edx_user and course_id in EdxNodeBBEnrollment table.

    Args:
        edx_user (User): Edx User to save course enrollment.
        course_id (Course Key): Edx Course Key to save course enrollment.    
    """
    course_enrollment = EdxNodeBBEnrollment.objects.filter(edx_uid=edx_user, course_key=course_id)

    if not course_enrollment:
        enrollment = EdxNodeBBEnrollment()
        enrollment.edx_uid = edx_user
        enrollment.course_key = course_id
        enrollment.save()


def remove_course_enrollment_from_db(edx_user, course_id):
    """"
    Dellets course enrollment details from EdxNodeBBEnrollment table.

    
    Args:
        edx_user (User): Edx User to delete course enrollment.
        course_id (Course Key): Edx Course Key to delete course enrollment.    
    """
    course_enrollment = EdxNodeBBEnrollment.objects.filter(edx_uid=edx_user, course_key=course_id)

    if course_enrollment:
        course_enrollment.delete()
