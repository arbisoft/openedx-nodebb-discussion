from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.features.openedx_nodebb_discussion.client.tasks import (
    task_create_user_on_nodebb, task_sync_user_profile_info_with_nodebb,
    task_delete_user_from_nodebb, task_create_category_on_nodebb,
    task_delete_category_from_nodebb, task_delete_user_from_nodebb,
    task_create_category_on_nodebb, task_join_group_on_nodebb,
    task_unjoin_group_on_nodebb
)
from openedx.features.openedx_nodebb_discussion.models import EdxNodeBBCategory
from student.models import UserProfile, CourseEnrollment


@receiver(post_save, sender=User)
def create_and_update_user_on_nodebb(sender, instance, created, update_fields, **kwargs):
    if created:
        user_data = {
            'username': instance.username,
            'email': instance.email,
            'joindate': instance.date_joined.strftime("%s")
        }
        task_create_user_on_nodebb.delay(**user_data)
    elif update_fields and 'last_login' not in update_fields:
        """
            On login `last_login` field change for ignoring this change we used this check.
            We are expecting last_login will never changed from django admin panel.
        """
        user_data = {
            'fullname': '{} {}'.format(instance.first_name, instance.last_name)
        }
        task_sync_user_profile_info_with_nodebb.delay(username=instance.username, **user_data)


@receiver(post_save, sender=UserProfile)
def sync_user_profile_info_with_nodebb(sender, instance, **kwargs):
    user = instance.user
    user_data = {
        'fullname': instance.name,
        'location': '{}, {}'.format(
            instance.city, instance.country.name),
        'birthday': '01/01/%s' % instance.year_of_birth
    }
    task_sync_user_profile_info_with_nodebb.delay(username=user.username, **user_data)


@receiver(pre_delete, sender=User)
def delete_user_from_nodebb(sender, instance, **kwargs):
    task_delete_user_from_nodebb.delay(username=instance.username)


@receiver(post_save, sender=CourseOverview)
def create_category_on_nodebb(sender, instance, created, update_fields, **kwargs):
    if created:
        course_data = {
            'name': '{}-{}-{}-{}'.format(instance.display_name, instance.id.org, instance.id.course, instance.id.run),
        }
        task_create_category_on_nodebb.delay(course_id=instance.id, course_name=instance.display_name, **course_data)


@receiver(pre_delete, sender=EdxNodeBBCategory)
def delete_category_from_nodebb(sender, instance, **kwargs):
    category_id = instance.nodebb_cid
    task_delete_category_from_nodebb.delay(category_id)


@receiver(post_save, sender=CourseEnrollment)
def manage_membership_on_nodebb_group(sender, instance, **kwargs):
    if instance.is_active:
        task_join_group_on_nodebb.delay(instance.username, instance.course_id)
    elif not instance.is_active and not kwargs['created']:
        task_unjoin_group_on_nodebb.delay(instance.username, instance.course_id)
