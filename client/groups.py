#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Group Class for NodeBB Client
"""
from __future__ import unicode_literals

from openedx.features.openedx_nodebb_discussion.client import Client

from .utils import save_group_relation_into_db


class NodeBBGroup(Client):
    def __init__(self):
        super(NodeBBGroup, self).__init__()

    def create(self, course_id, **kwargs):
        """Creates a new NodeBB Group.

        Args:

            **kwargs: All other accepted user properties. You can find out
                what they are by referring to `updateProfile`.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        response_code, json_response = self.post('/api/v2/groups', **kwargs)

        if response_code == 200:
            save_group_relation_into_db(course_id, group_slug=json_response['slug'], group_name=json_response['name'])

        return response_code, json_response

    def delete_group(self, group_slug):
        response_code, json_response = self.delete('/api/v2/groups/{}'.format(group_slug))
        return response_code, json_response
