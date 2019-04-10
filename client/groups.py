#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains the Group Class for NodeBB Client
"""
from __future__ import unicode_literals

from openedx.features.openedx_nodebb_discussion.client import Client
from openedx.features.openedx_nodebb_discussion.client.utils import save_group_relation_into_db


class NodeBBGroup(Client):
    """
    Group Class responsible to make connection with NodeBB Client for groups related operations.
    """
    def __init__(self):
        super(NodeBBGroup, self).__init__()

    def create(self, course_id, **payload):
        """
        Creates a new NodeBB Group.

        Args:
            course_id (Course Key): Course Key of course for which we have to create group.

            **payload (dictionary): Payload to send to Api contains name of group.

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        response_code, json_response = self.post('/api/v2/groups', **payload)

        if response_code == 200:
            save_group_relation_into_db(course_id, group_slug=json_response['slug'], group_name=json_response['name'])

        return response_code, json_response

    def delete_group(self, group_slug):
        """
        Delete a NodeBB Group.

        Args:
            group_slug (str): Slug of group to be deleted.

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        response_code, json_response = self.delete('/api/v2/groups/{}'.format(group_slug))
        return response_code, json_response

    def add_member(self, uid, group_slug):
        """
        Add member to the NodeBB group.

        Args:
            uid (int): NodeBB uid of user to be add to group
            group_slug (str): Slug of group user joining.

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.

        """
        response_code, json_response = self.put('/api/v2/groups/{}/membership/{}'.format(group_slug, uid))
        return response_code, json_response

    def delete_member(self, uid, group_slug):
        """
        Delete member from NodeBB group.

        Args:
            uid (int): NodeBB uid of user to be add to group
            group_slug (str): Slug of group user joining.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        response_code, json_response = self.delete('/api/v2/groups/{}/membership/{}'.format(group_slug, uid))
        return response_code, json_response
