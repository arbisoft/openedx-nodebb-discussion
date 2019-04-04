from celery.task import task
from django.conf import settings
import requests
from openedx.features.openedx_nodebb_discussion.client.users import NodeBBUser

RETRY_DELAY = 10


def handle_response(caller, task_name, status_code, response, username):
    """
    Logs the response of the specific NodeBB API call
    """
    if status_code >= 500:
        print('Retrying: {} task for user: {}'.format(task_name, username))
        caller.retry()
    elif status_code >= 400:
        print('Failure: {} task for user: {}, status_code: {}, response: {}'
              .format(task_name, username, status_code, response))
    elif 200 <= status_code < 300:
        print('Success: {} task for user: {}'.format(task_name, username))


@task(default_retry_delay=RETRY_DELAY, max_retries=None, routing_key=settings.HIGH_PRIORITY_QUEUE)
def task_create_user_on_nodebb(**user_data):
    status_code, response = NodeBBUser().create(**user_data)
    handle_response(task_create_user_on_nodebb, "User Creation", status_code, response, user_data['username'])


@task(default_retry_delay=RETRY_DELAY, max_retries=None, routing_key=settings.HIGH_PRIORITY_QUEUE)
def task_sync_user_profile_info_with_nodebb(username, **user_data):
    status_code, response = NodeBBUser().update(username=username, **user_data)
    handle_response(task_sync_user_profile_info_with_nodebb, "User Updating", status_code, response, username)


@task(default_retry_delay=RETRY_DELAY, max_retries=None)
def task_delete_user_from_nodebb(username):
    status_code, response = NodeBBUser().delete_user(username=username)
    handle_response(task_delete_user_from_nodebb, "User Deletion", status_code, response, username)
