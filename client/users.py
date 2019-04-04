#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    User Class for NodeBB Client
"""
from __future__ import unicode_literals

from openedx.features.openedx_nodebb_discussion.client import Client

from .utils import save_relation_into_db, get_nodebb_uid_from_username


class NodeBBUser(Client):
    def __init__(self):
        super(NodeBBUser, self).__init__()

    def create(self, **kwargs):
        """Creates a new NodeBB user.

        Args:
            **kwargs: All other accepted user properties. You can find out
                what they are by referring to `updateProfile`.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        response_code, json_response = self.post('/api/v2/users', **kwargs)

        if response_code == 200:
            save_relation_into_db(username=kwargs['username'], nodebb_uid=json_response['uid'])

        return response_code, json_response

    def _update(self, uid, endpoint, **kwargs):
        kwargs.update({'_uid': uid})
        return self.put(endpoint, **kwargs)

    def update(self, username, **kwargs):
        """Updates the user's NodeBB user properties.

        Accepted user properties can be found by referring to `updateProfile`.
        For a quick reference these are the accepted fields:

        username, email, fullname, website, location, birthday, signature

        Args:
            username (str): The edx username for the user we are deleting

            **kwargs: A dictionary of user properties we are updating.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        uid = get_nodebb_uid_from_username(username)
        return self._update(uid, '/api/v2/users/%s' % uid, **kwargs)

    def delete_user(self, username):
        """Removes the associated NodeBB user.

        Warning! This operation is irreversible. Note that if `uid` is None
        then, no requests will be made and a 404 will be returned.

        Args:
            username (str): The edx username for the user we are deleting

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        uid = get_nodebb_uid_from_username(username)
        return self.delete('/api/v2/users/%s' % uid, **{'_uid': uid})
