"""
Base class which contains the basic methods to interaction with the write api of NodeBB.
"""
import json

import requests
import urlparse
from django.conf import settings as django_settings


class Client(object):
    """
    Client Class responsible to make connection with NodeBB and perform all calls.
    """
    def __init__(self):
        self._configure()

    def _configure(self):
        self.endpoint = 'http://172.16.16.24:4568'
        self.admin_uid = django_settings.OPENEDX_NODEBB_DISCUSSION['NODEBB_ADMIN_UID']
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
            kwargs (dictionary): All others data to post and put to Api along with call

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        if '_uid' not in kwargs:
            kwargs.update({'_uid': self.admin_uid})

        # `_uid` is None, there's nothing we can do at this point.
        if kwargs['_uid'] is None:
            return 404, 'Not Found'

        # Query the NodeBB instance, extracting the status code and fail reason.
        response = requests.request(
            method,
            urlparse.urljoin(self.endpoint, path),
            headers=self.headers,
            data=json.dumps(kwargs)
        )
        status_code, reason = response.status_code, response.reason

        if response.reason != 'OK':  # Not a success response.
            return status_code, reason

        # ValueError occurs when `.json()` reads invalid JSON.
        try:
            json_response = response.json()
            if 'payload' in json_response:
                json_response = json_response['payload']
            return status_code, json_response
        except ValueError:
            return status_code, {}

    def post(self, path, **kwargs):
        """
        Handles all type of post calls made to NodeBB.

        Args:
            path (str): Api path to make call
            kwargs (dictionary): All others data to post and put to Api along with call

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        return self._request('POST', path, **kwargs)

    def put(self, path, **kwargs):
        """
        Handles all type of put calls made to NodeBB.

        Args:
            path (str): Api path to make call
            kwargs (dictionary): All others data to post and put to Api along with call

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        return self._request('PUT', path, **kwargs)

    def delete(self, path, **kwargs):
        """
        Handles all type of delete calls made to NodeBB.

        Args:
            path (str): Api path to make call
            kwargs (dictionary): All others data to post and put to Api along with call

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        return self._request('DELETE', path, **kwargs)
