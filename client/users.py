#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains the User Class for NodeBB Client
"""
from __future__ import unicode_literals

from openedx.features.openedx_edly_discussion.client import Client
from openedx.features.openedx_edly_discussion.client.utils import (
    get_nodebb_uid_from_username,
    save_user_relation_into_db
)


class NodeBBUser(Client):
    """
    User Class responsible to make connection with NodeBB Client for users related operations.
    """

    def create(self, **payload):
        """
        Creates a new NodeBB user.

        Args:
            **payload (dictionary): All other accepted user properties. You can find out
                what they are by referring to `updateProfile`.

            payload: {
                username: "edx",
                email: "edx@example.com",
                joindate (secs): "215518413254"
            }

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.

        """
        response_code, json_response = self.post('/api/v2/users', **payload)
        if response_code == 200:
            save_user_relation_into_db(username=payload['username'], nodebb_uid=json_response['uid'])

        return response_code, json_response

    def update(self, username, **payload):
        """
        Updates the user's NodeBB user properties.

        Accepted user properties can be found by referring to `updateProfile`.
        For a quick reference these are the accepted fields:

        username, email, fullname, website, location, birthday, signature

        Args:
            username (str): The edX username for the user we are deleting

            **payload (dictionary): A dictionary of user properties we are updating.

            payload: {
                fullname: "Edx User",
                location: "Lahore, Pakistan"
                birthday: "01/01/2019"
            }

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.

        """
        uid = get_nodebb_uid_from_username(username)
        payload.update({'_uid': uid})
        return self.put('/api/v2/users/{}'.format(uid), **payload)

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
        return self.delete('/api/v2/users/{}'.format(uid), **{'_uid': uid})
