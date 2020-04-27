"""
Contains signals, responsible to sync edX with NodeBB.
As some related event is occurred in edX the signal is received
and a relevant request is made to NodeBB write api to make that
change at NodeBB side too.
"""
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.features.openedx_edly_discussion.client.tasks import (
    task_create_category_on_nodebb,
    task_create_user_on_nodebb,
    task_delete_category_from_nodebb,
    task_delete_user_from_nodebb,
    task_join_group_on_nodebb,
    task_unjoin_group_on_nodebb,
    task_update_user_profile_on_nodebb
)
from openedx.features.openedx_edly_discussion.models import EdxNodeBBCategory
from student.models import CourseEnrollment, UserProfile


@receiver(post_save, sender=User)
def create_and_update_user_on_nodebb(sender, instance, created, update_fields, **kwargs):
    """
    Creates a new user at Nodebb side when a new user is created at edX side. OR
    Update the previous one if some relevant changes occur.

    Args:
        sender (str): Name of Sender model
        instance: Newly created or updated entry of Model.
        created: Flag will be true if new instance created or false if upgraded.
        update_fields:  Contains frozen_set of the names of updated fields.
        **kwargs:  All remaining fields.
    """
    if created:
        user_data = {
            'username': instance.username,
            'email': instance.email,
            'joindate': instance.date_joined.strftime('%s')
        }
        task_create_user_on_nodebb.delay(**user_data)


@receiver(post_save, sender=UserProfile)
def update_user_profile_on_nodebb(sender, instance, **kwargs):
    """
    If some changed occurs in the User Profile, makes sure that
    these changes are also made at Nodebb side.

    Args:
        sender (str): Name of Sender model
        instance: Newly created or updated entry of Model.
        **kwargs:  All remaining fields.
    """
    user = instance.user
    user_data = {
        'fullname': instance.name,
        'location': '{}, {}'.format(
            instance.city, instance.country.name),
        'birthday': '01/01/{}'.format(instance.year_of_birth)
    }
    task_update_user_profile_on_nodebb.delay(username=user.username, **user_data)


@receiver(pre_delete, sender=User)
def delete_user_from_nodebb(sender, instance, **kwargs):
    """
    Deletes the user from NodeBB if it is deleted from edX.

    Args:
        sender (str): Name of Sender model
        instance: Entry of model which is being deleted.
        **kwargs:  All remaining fields.
    """
    task_delete_user_from_nodebb.delay(username=instance.username)


@receiver(post_save, sender=CourseOverview)
def create_category_on_nodebb(sender, instance, created, update_fields, **kwargs):
    """
    Whenever a new course is created in edX, creates a new category in NodeBB.

    Args:
        sender (str): Name of Sender model
        instance: Newly created entry of Model.
        created: Flag will be true if new instance created or false if upgraded.
        update_fields:  Contains frozen_set of the names of updated fields.
        **kwargs:  All remaining fields.
    """
    if created:
        course_data = {
            'organization': instance.id.org,
            'course_name': instance.id.course,
            'course_run': instance.id.run,
            'display_name': instance.display_name
        }
        task_create_category_on_nodebb.delay(**course_data)


@receiver(pre_delete, sender=EdxNodeBBCategory)
def delete_category_from_nodebb(sender, instance, **kwargs):
    """
    Deletes the category from NodeBB if it is deleted from edX.

    Args:
        sender (str): Name of Sender model
        instance: Entry of model which is being deleted.
        **kwargs:  All remaining fields.
    """
    category_id = instance.nodebb_cid
    task_delete_category_from_nodebb.delay(category_id)


@receiver(post_save, sender=CourseEnrollment)
def manage_membership_on_nodebb_group(sender, instance, **kwargs):
    """
    Join or un-join course related group based on enrollment status of edX user.

    Args:
        sender (str): Name of Sender model
        instance: Newly created or updated entry of Model.
        **kwargs:  All remaining fields.
    """
    course_data = {
        'organization': instance.course_id.org,
        'course_name': instance.course_id.course,
        'course_run': instance.course_id.run,
    }
    if instance.is_active:
        task_join_group_on_nodebb.delay(instance.username, **course_data)
    elif not instance.is_active and not kwargs['created']:
        task_unjoin_group_on_nodebb.delay(instance.username, **course_data)
