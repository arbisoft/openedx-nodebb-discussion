#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains the User Class for NodeBB Client
"""
from __future__ import unicode_literals

from openedx.features.openedx_nodebb_discussion.client import Client
from openedx.features.openedx_nodebb_discussion.client.utils import (
    save_user_relation_into_db, get_nodebb_uid_from_username
)


class NodeBBUser(Client):
    """
    User Class responsible to make connection with NodeBB Client for users related operations.
    """

    def __init__(self):
        super(NodeBBUser, self).__init__()

    def create(self, **payload):
        """
        Creates a new NodeBB user.

        Args:
            **payload (dictionary): All other accepted user properties. You can find out
                what they are by referring to `updateProfile`.

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.

        """
        response_code, json_response = self.post('/api/v2/users', **payload)

        if response_code == 200:
            save_user_relation_into_db(username=payload['username'], nodebb_uid=json_response['uid'])

        return response_code, json_response

    def _update(self, uid, endpoint, **kwargs):
        kwargs.update({'_uid': uid})
        return self.put(endpoint, **kwargs)

    def update(self, username, **kwargs):
        """
        Updates the user's NodeBB user properties.

        Accepted user properties can be found by referring to `updateProfile`.
        For a quick reference these are the accepted fields:

        username, email, fullname, website, location, birthday, signature

        Args:
            username (str): The edX username for the user we are deleting

            **kwargs (dictionary): A dictionary of user properties we are updating.

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.

        """
        uid = get_nodebb_uid_from_username(username)
        return self._update(uid, '/api/v2/users/%s' % uid, **kwargs)

    def delete_user(self, username):
        """
        Removes the associated NodeBB user.

        Warning! This operation is irreversible. Note that if `uid` is None
        then, no requests will be made and a 404 will be returned.

        Args:
            username (str): The edX username for the user we are deleting.

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.

        """
        uid = get_nodebb_uid_from_username(username)
        return self.delete('/api/v2/users/%s' % uid, **{'_uid': uid})
