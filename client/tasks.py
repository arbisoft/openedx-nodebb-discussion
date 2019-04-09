"""
Celery tasks to handle api requests of write api of nodebb.
"""
from logging import getLogger

from celery.task import task
from django.conf import settings
from openedx.features.openedx_nodebb_discussion.client.categories import NodeBBCategory
from openedx.features.openedx_nodebb_discussion.client.groups import NodeBBGroup
from openedx.features.openedx_nodebb_discussion.client.users import NodeBBUser
from openedx.features.openedx_nodebb_discussion.client.utils import (
    get_category_id_from_course_id, get_group_slug_from_course_id,
    get_group_slug_from_category_id, get_group_name_from_course_id,
    get_nodebb_uid_from_username
)

RETRY_DELAY = 10

log = getLogger(__name__)


def handle_response(caller, task_name, job_type, status_code, response, username):
    """
    Logs the response of the specific NodeBB API call
    """
    if status_code >= 500:
        """
        In case of any internal server error, retry that task again.
        """
        log.warning('Retrying: {} task for {}: {}'.format(task_name, job_type, username))
        caller.retry()
    elif status_code >= 400:
        """
        In case of any unauthorized request just log the error.
        """
        log.error('Failure: {} task for {}: {}, status_code: {}, response: {}'
                  .format(task_name, job_type, username, status_code, response))
    elif 200 <= status_code < 300:
        """
        In case of success, just log the success status.
        """
        log.info('Success: {} task for {}: {}'.format(task_name, job_type, username))


@task(default_retry_delay=RETRY_DELAY, max_retries=None, routing_key=settings.HIGH_PRIORITY_QUEUE)
def task_create_user_on_nodebb(**user_data):
    """
    Creates user on nodebb.
    """
    status_code, response = NodeBBUser().create(**user_data)
    handle_response(task_create_user_on_nodebb, "User Creation", "User", status_code, response, user_data['username'])


@task(default_retry_delay=RETRY_DELAY, max_retries=None, routing_key=settings.HIGH_PRIORITY_QUEUE)
def task_sync_user_profile_info_with_nodebb(username, **user_data):
    """
    Sync user profile on nodebb.
    """
    status_code, response = NodeBBUser().update(username=username, **user_data)
    handle_response(task_sync_user_profile_info_with_nodebb, "User Updating", "User", status_code, response, username)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def task_delete_user_from_nodebb(username):
    """
    Deletes user from nodebb.
    """
    status_code, response = NodeBBUser().delete_user(username=username)
    handle_response(task_delete_user_from_nodebb, "User Deletion", "User", status_code, response, username)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def task_create_category_on_nodebb(course_id, course_name, **course_data):
    """
    Creates a category corresponding to an openedx course.
    After successful creation of category also creates a
    group against that category on nodebb.
    """
    payload = {
        "name": course_name
    }
    status_code, response = NodeBBCategory().create(course_id, **payload)
    handle_response(task_create_category_on_nodebb, "Category Creation", "Course", status_code, response, course_name)
    if status_code == 200:
        _task_create_group_on_nodebb.delay(course_id, **course_data)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def _task_create_group_on_nodebb(course_id, **group_data):
    """
    Creates a group on nodebb.
    """
    status_code, response = NodeBBGroup().create(course_id, **group_data)
    handle_response(_task_create_group_on_nodebb, "Group Creation", "Group", status_code, response,
                    group_data['name'])
    if status_code == 200:
        _task_delete_default_permission_of_category_on_nodebb.delay(course_id)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def _task_delete_default_permission_of_category_on_nodebb(course_id):
    """
    Deletes default privileges fo category on nodebb.
    """
    category_id = get_category_id_from_course_id(course_id)
    status_code, response = NodeBBCategory().delete_default_permissions(category_id)
    handle_response(_task_delete_default_permission_of_category_on_nodebb, "Default Permission Deletion", "Group",
                    status_code,
                    response,
                    str(course_id))
    if status_code == 200:
        _task_add_course_group_permission_of_category_on_nodebb.delay(course_id)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def _task_add_course_group_permission_of_category_on_nodebb(course_id):
    """
    Add custom group permission of category on nodebb.
    """
    group_name = get_group_name_from_course_id(course_id)
    category_id = get_category_id_from_course_id(course_id)
    status_code, response = NodeBBCategory().add_course_group_permission(category_id, group_name)
    handle_response(_task_add_course_group_permission_of_category_on_nodebb, "Category Course Group Permission Add",
                    "Group",
                    status_code,
                    response,
                    str(course_id))


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def task_delete_category_from_nodebb(category_id):
    """
    Deletes category from nodebb.
    """
    status_code, response = NodeBBCategory().delete_category(category_id)
    handle_response(task_delete_category_from_nodebb, "Category Deletion",
                    "Category",
                    status_code,
                    response,
                    category_id)
    if status_code == 200:
        _task_delete_group_from_nodebb.delay(category_id)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def _task_delete_group_from_nodebb(category_id):
    """
    Deletes group from nodebb.
    """
    group_slug = get_group_slug_from_category_id(category_id)
    status_code, response = NodeBBGroup().delete_group(group_slug)
    handle_response(_task_delete_group_from_nodebb, "Group Deletion",
                    "Group",
                    status_code,
                    response,
                    group_slug)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def task_join_group_on_nodebb(username, course_id):
    """
    Enables the user to join nodebb group.
    """
    group_slug = get_group_slug_from_course_id(course_id)
    uid = get_nodebb_uid_from_username(username)
    status_code, response = NodeBBGroup().add_member(uid, group_slug, **{})
    handle_response(task_join_group_on_nodebb, "Group Membership", "Join Group", status_code, response, username)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def task_unjoin_group_on_nodebb(username, course_id):
    """
    Enables the user to un join the group.
    """
    group_slug = get_group_slug_from_course_id(course_id)
    uid = get_nodebb_uid_from_username(username)
    status_code, response = NodeBBGroup().delete_member(uid, group_slug, **{})
    handle_response(task_unjoin_group_on_nodebb, "Group Membership", "Unjoin Group", status_code, response, username)
