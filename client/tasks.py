"""
Celery tasks to handle api requests of write api of NodeBB.
"""
from logging import getLogger

from celery.task import task
from django.conf import settings
from opaque_keys.edx.locator import CourseLocator
from openedx.features.openedx_edly_discussion.client.categories import NodeBBCategory
from openedx.features.openedx_edly_discussion.client.groups import NodeBBGroup
from openedx.features.openedx_edly_discussion.client.users import NodeBBUser
from openedx.features.openedx_edly_discussion.client.utils import (
    get_category_id_from_course_id,
    get_group_name_from_course_id,
    get_group_slug_from_category_id,
    get_group_slug_from_course_id,
    get_nodebb_uid_from_username
)

RETRY_DELAY = 60

log = getLogger(__name__)


def handle_response(response_details):
    """
    We are presuming here server is always running or it is an ngnix server which will always return some response.
    Logs the response of the specific NodeBB API call and retry the task if it fails due to the server inactivity.

    Args:
        response_details (dictionary): contains the following keys
            caller (method): Method from which response is logged.
            task_name (str): Task Name for which we are logging response
            job_type (str): Job Type for which we are logging response
            status_code (int): Api response code through which we will check our status.
            response (str): Received response from Api which we will log.
            entity (str): Can be anything like course_name or username or group_name
    """
    caller, task_name = response_details['caller'], response_details['task_name']
    job_type, status_code = response_details['job_type'], response_details['status_code']
    response, entity = response_details['response'], response_details['entity']

    if status_code >= 500:
        """
        In case of any internal server error, retry that task again.
        """
        log.warning('Retrying: {} task for {}: {}'.format(task_name, job_type, entity))
        caller.retry()
    elif status_code >= 400:
        """
        In case of any unauthorized request we don't need to retry the task so we log error.
        """
        log.error('Failure: {} task for {}: {}, status_code: {}, response: {}'
                  .format(task_name, job_type, entity, status_code, response))
    elif 200 <= status_code < 300:
        log.info('Success: {} task for {}: {}'.format(task_name, job_type, entity))


@task(default_retry_delay=RETRY_DELAY, max_retries=None, routing_key=settings.HIGH_PRIORITY_QUEUE)
def task_create_user_on_nodebb(**user_data):
    """
    Creates user on NodeBB.

    Args:
        **user_data (dictionary): Contains information of user to be created.
    """
    status_code, response = NodeBBUser().create(**user_data)

    response_details = {
        'caller': task_create_user_on_nodebb,
        'task_name': "User Creation",
        'job_type': "User",
        'status_code': status_code,
        'response': response,
        'entity': user_data['username']
    }

    handle_response(response_details)


@task(default_retry_delay=RETRY_DELAY, max_retries=None, routing_key=settings.HIGH_PRIORITY_QUEUE)
def task_update_user_profile_on_nodebb(username, **user_data):
    """
    Sync user profile on NodeBB.

    Args:
        username (str): Username of edX User to be updated.
        **user_data (dictionary): Contains information of user to be created.
    """
    status_code, response = NodeBBUser().update(username=username, **user_data)

    response_details = {
        'caller': task_update_user_profile_on_nodebb,
        'task_name': "User Updating",
        'job_type': "User",
        'status_code': status_code,
        'response': response,
        'entity': username
    }

    handle_response(response_details)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def task_delete_user_from_nodebb(username):
    """
    Deletes user from NodeBB.

    Args:
        username (str): Username of edX User to be deleted.
    """
    status_code, response = NodeBBUser().delete_user(username=username)

    response_details = {
        'caller': task_delete_user_from_nodebb,
        'task_name': "User Deletion",
        'job_type': "User",
        'status_code': status_code,
        'response': response,
        'entity': username
    }

    handle_response(response_details)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def task_create_category_on_nodebb(**course_data):
    """
    Creates a category corresponding to an edX course.
    After successful creation of category also creates a
    group against that category on NodeBB.

    Args:
        **course_data (dictionary): Extra data related to course like course full name.
    """
    payload = {
        'name': course_data['display_name']
    }

    course_id = CourseLocator(course_data['organization'], course_data['course_name'], course_data['course_run'])
    status_code, response = NodeBBCategory().create(course_id, **payload)

    response_details = {
        'caller': task_create_category_on_nodebb,
        'task_name': "Category Creation",
        'job_type': "Course",
        'status_code': status_code,
        'response': response,
        'entity': course_data['display_name']
    }

    handle_response(response_details)
    if status_code == 200:
        _task_create_group_on_nodebb.delay(**course_data)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def _task_create_group_on_nodebb(**group_data):
    """
    Creates a group on NodeBB.

    Args:
        **group_data (dictionary): Extra data related to group like course full name.
    """
    course_id = CourseLocator(group_data['organization'], group_data['course_name'], group_data['course_run'])
    payload = {
        'name': '{}-{}-{}-{}'.format(group_data['display_name'], group_data['organization'],
                                     group_data['course_name'], group_data['course_run'])
    }
    status_code, response = NodeBBGroup().create(course_id, **payload)

    response_details = {
        'caller': _task_create_group_on_nodebb,
        'task_name': "Group Creation",
        'job_type': "Group",
        'status_code': status_code,
        'response': response,
        'entity': group_data['display_name']
    }

    handle_response(response_details)

    if status_code == 200:
        _task_delete_default_permission_of_category_on_nodebb.delay(**group_data)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def _task_delete_default_permission_of_category_on_nodebb(**group_data):
    """
    Deletes default privileges of category on NodeBB.

    Args:
        **group_data (dictionary): Extra data related to group like course full name.
    """
    course_id = CourseLocator(group_data['organization'], group_data['course_name'], group_data['course_run'])
    category_id = get_category_id_from_course_id(course_id)
    status_code, response = NodeBBCategory().delete_default_permissions(category_id)

    response_details = {
        'caller': _task_delete_default_permission_of_category_on_nodebb,
        'task_name': "Default Permission Deletion",
        'job_type': "Group",
        'status_code': status_code,
        'response': response,
        'entity': str(course_id)
    }

    handle_response(response_details)

    if status_code == 200:
        _task_add_course_group_permission_of_category_on_nodebb.delay(**group_data)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def _task_add_course_group_permission_of_category_on_nodebb(**group_data):
    """
    Add custom group permission of category on NodeBB.

    Args:
        **group_data (dictionary): Extra data related to group like course full name.
    """
    course_id = CourseLocator(group_data['organization'], group_data['course_name'], group_data['course_run'])
    group_name = get_group_name_from_course_id(course_id)
    category_id = get_category_id_from_course_id(course_id)
    status_code, response = NodeBBCategory().add_course_group_permission(category_id, group_name)

    response_details = {
        'caller': _task_add_course_group_permission_of_category_on_nodebb,
        'task_name': "Adding Category Group Permission",
        'job_type': "Group",
        'status_code': status_code,
        'response': response,
        'entity': str(course_id)
    }

    handle_response(response_details)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def task_delete_category_from_nodebb(category_id):
    """
    Deletes category from NodeBB.

    Args:
        category_id (int): NodeBB cid of category we want to delete.
    """
    status_code, response = NodeBBCategory().delete_category(category_id)

    response_details = {
        'caller': task_delete_category_from_nodebb,
        'task_name': "Category Deletion",
        'job_type': "Category",
        'status_code': status_code,
        'response': response,
        'entity': category_id
    }

    handle_response(response_details)

    if status_code == 200:
        _task_delete_group_from_nodebb.delay(category_id)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def _task_delete_group_from_nodebb(category_id):
    """
    Deletes group from NodeBB.

    Args:
        category_id (int): NodeBB cid of category for extracting its related group_slug.
    """
    group_slug = get_group_slug_from_category_id(category_id)
    status_code, response = NodeBBGroup().delete_group(group_slug)

    response_details = {
        'caller': _task_delete_group_from_nodebb,
        'task_name': "Group Deletion",
        'job_type': "Group",
        'status_code': status_code,
        'response': response,
        'entity': group_slug
    }

    handle_response(response_details)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def task_join_group_on_nodebb(username, **group_data):
    """
    Register the user in NodeBB group.

    Args:
        username (str): Username of edX User who is joining group.
        **group_data (dictionary): Extra data related to group like course full name.
    """
    course_id = CourseLocator(group_data['organization'], group_data['course_name'], group_data['course_run'])
    group_slug = get_group_slug_from_course_id(course_id)
    uid = get_nodebb_uid_from_username(username)
    status_code, response = NodeBBGroup().add_member(uid, group_slug)

    response_details = {
        'caller': task_join_group_on_nodebb,
        'task_name': "Group Membership",
        'job_type': "Join Group",
        'status_code': status_code,
        'response': response,
        'entity': username
    }

    handle_response(response_details)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def task_unjoin_group_on_nodebb(username, **group_data):
    """
    Unregister the user from NodeBB group.

    Args:
        username (str): Username of edX User who is leaving the group.
        **group_data (dictionary): Extra data related to group like course full name.
    """
    course_id = CourseLocator(group_data['organization'], group_data['course_name'], group_data['course_run'])
    group_slug = get_group_slug_from_course_id(course_id)
    uid = get_nodebb_uid_from_username(username)
    status_code, response = NodeBBGroup().remove_member(uid, group_slug)

    response_details = {
        'caller': task_unjoin_group_on_nodebb,
        'task_name': "Group Membership",
        'job_type': "Un join Group",
        'status_code': status_code,
        'response': response,
        'entity': username
    }

    handle_response(response_details)
