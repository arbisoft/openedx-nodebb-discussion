"""
Base class which contains the basic methods to interaction with the write api of NodeBB.
"""
import json

import requests
import urlparse
from django.conf import settings as django_settings

NODEBB_ADMIN_UID = 1


class Client(object):
    """
    Client Class responsible to make connection with NodeBB and perform all calls.
    """
    def __init__(self):
        self._configure()

    def _configure(self):
        self.endpoint = django_settings.NODEBB_SETTINGS['URL']
        self.admin_uid = NODEBB_ADMIN_UID
        self.headers = {
            'Authorization': 'Bearer {}'.format(django_settings.OPENEDX_NODEBB_DISCUSSION['NODEBB_API_TOKEN']),
            'Content-Type': 'application/json'
        }

    def _request(self, method, path, **kwargs):
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

        response = requests.request(
            method,
            urlparse.urljoin(self.endpoint, path),
            headers=self.headers,
            data=json.dumps(kwargs)
        )
        status_code, reason = response.status_code, response.reason

        if reason != 'OK':
            return status_code, reason

        try:
            json_response = response.json()
            if 'payload' in json_response:
                json_response = json_response['payload']
            return status_code, json_response
        except ValueError:
            return status_code, {}

    def post(self, path, **kwargs):
        """
        Sends a POST request to NodeBB.

        Args:
            path (str): Api path to make call
            kwargs (dictionary): All other necessary data to make post call to API

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        return self._request('POST', path, **kwargs)

    def put(self, path, **kwargs):
        """
        Sends a PUT request to NodeBB.

        Args:
            path (str): Api path to make call
            kwargs (dictionary): All other necessary data to make put call to API

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        return self._request('PUT', path, **kwargs)

    def delete(self, path, **kwargs):
        """
        Sends a Delete request to NodeBB.

        Args:
            path (str): Api path to make call
            kwargs (dictionary): All other necessary data to make delete call to API

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        return self._request('DELETE', path, **kwargs)
