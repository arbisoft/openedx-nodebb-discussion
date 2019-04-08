#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Group Class for NodeBB Client
"""
from __future__ import unicode_literals

from openedx.features.openedx_nodebb_discussion.client import Client

from .utils import save_group_relation_into_db, get_group_slug_from_course_id, get_nodebb_uid_from_username


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
            save_group_relation_into_db(course_id, group_slug=json_response['slug'])

        return response_code, json_response

    def add_member(self, uid, group_slug, **kwargs):
        """Add member to the nodebb group.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        return self.put('/api/v2/groups/%s/membership/%s' % (group_slug, uid), **kwargs)

    def delete_member(self, uid, group_slug, **kwargs):
        """Delete member from nodebb group.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        return self.delete('/api/v2/groups/%s/membership/%s' % (group_slug, uid), **kwargs)
