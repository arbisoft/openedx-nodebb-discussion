"""
Base class which contains the basic methods to interaction with the write api of NodeBB.
"""
import json
import urlparse

import requests

from django.conf import settings as django_settings
from openedx.features.openedx_edly_discussion.client.constants import BAD_REQUEST, CONNECTION_ERROR, NODEBB_ADMIN_UID


class Client(object):
    """
    Client Class responsible to make connection with NodeBB and perform all calls.
    """

    def __init__(self):
        self._configure()

    def _configure(self):
        self.endpoint = django_settings.EDLY_DISCUSSION_SETTINGS['URL']
        self.admin_uid = NODEBB_ADMIN_UID
        self.headers = {
            'Authorization': 'Bearer {}'.format(django_settings.EDLY_DISCUSSION_SECRETS['API_MASTER_TOKEN']),
            'Content-Type': 'application/json'
        }

    def _call(self, method, path, **kwargs):
        """
        Hidden Method of Client this function will generate all of the Api Call's and return response.

        Args:
            method (str): Api call method can be Post, Put, and Delete
            path (str): Api path to make call
            kwargs (dictionary): All other necessary data to make POST, PUT or DELETE calls to API

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        if '_uid' not in kwargs:
            kwargs.update({'_uid': self.admin_uid})

        try:
            response = requests.request(
                method,
                urlparse.urljoin(self.endpoint, path),
                headers=self.headers,
                data=json.dumps(kwargs)
            )
            status_code, response_msg = response.status_code, response.json()
            try:
                if 'payload' in response_msg:
                    response_msg = response_msg['payload']
            except ValueError:
                response_msg = {}

        except requests.exceptions.ConnectionError as err:
            status_code, response_msg = CONNECTION_ERROR, err
        except requests.exceptions.RequestException as err:
            status_code, response_msg = BAD_REQUEST, err

        return status_code, response_msg

    def post(self, path, **kwargs):
        """
        Sends a POST request to NodeBB.

        Args:
            path (str): Api path to make call
            kwargs (dictionary): All other necessary data to make post call to API

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        return self._call('POST', path, **kwargs)

    def put(self, path, **kwargs):
        """
        Sends a PUT request to NodeBB.

        Args:
            path (str): Api path to make call
            kwargs (dictionary): All other necessary data to make put call to API

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        return self._call('PUT', path, **kwargs)

    def delete(self, path, **kwargs):
        """
        Sends a Delete request to NodeBB.

        Args:
            path (str): Api path to make call
            kwargs (dictionary): All other necessary data to make delete call to API

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        return self._call('DELETE', path, **kwargs)
