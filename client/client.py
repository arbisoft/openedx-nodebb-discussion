import json

import requests
import urlparse
from django.conf import settings as django_settings


class Client(object):

    def __init__(self):
        self._configure()

    def _configure(self):
        self.endpoint = "http://172.16.16.24:4568"
        self.admin_uid = "1"
        self.headers = {
            'authorization': "Bearer {}".format(django_settings.OPENEDX_NODEBB_DISCUSSION['NODEBB_API_TOKEN']),
            'content-type': "application/json"
        }

    def _request(self, method, path, **kwargs):
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
        code, reason = response.status_code, response.reason

        if response.reason != 'OK':  # Not a success response.
            return code, reason

        # ValueError occurs when `.json()` reads invalid JSON.
        try:
            json_response = response.json()
            if 'payload' in json_response:
                json_response = json_response['payload']
            return code, json_response
        except ValueError:
            return code, {}

    def get(self, path, **kwargs):
        return self._request('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self._request('POST', path, **kwargs)

    def put(self, path, **kwargs):
        return self._request('PUT', path, **kwargs)

    def delete(self, path, **kwargs):
        return self._request('DELETE', path, **kwargs)
