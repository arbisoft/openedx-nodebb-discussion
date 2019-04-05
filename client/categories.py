#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Category Class for NodeBB Client
"""
from __future__ import unicode_literals

from openedx.features.openedx_nodebb_discussion.client import Client

from .utils import save_category_relation_into_db


class NodeBBCategory(Client):
    privileges = [
        "groups:find",
        "groups:read",
        "groups:topics:read",
        "groups:topics:create",
        "groups:topics:reply",
        "groups:topics:tag",
        "groups:posts:edit",
        "groups:posts:history",
        "groups:posts:delete",
        "groups:posts:upvote",
        "groups:posts:downvote",
        "groups:topics:delete",
        "groups:posts:view_deleted",
        "groups:purge",
        "groups:moderate"
    ]

    default_groups = [
        "registered-users",
        "guests",
        "spiders"
    ]

    def __init__(self):
        super(NodeBBCategory, self).__init__()

    def create(self, course_id, **kwargs):
        """Creates a new NodeBB Category.

        Args:
            course_id: Course_Key

            **kwargs: All other accepted user properties. You can find out
                what they are by referring to `updateProfile`.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        response_code, json_response = self.post('/api/v2/categories', **kwargs)

        if response_code == 200:
            save_category_relation_into_db(course_id=course_id, category_id=json_response['cid'])

        return response_code, json_response

    def delete_default_permissions(self, category_id):
        payload = {
            "privileges": self.privileges,
            "groups": self.default_groups
        }
        response_code, json_response = self.delete('/api/v2/categories/{}/privileges'.format(category_id), **payload)

        return response_code, json_response

    def add_course_group_permission(self, category_id, group_slug):
        payload = {
            "privileges": self.privileges,
            "groups": [
                group_slug
            ]
        }
        response_code, json_response = self.put('/api/v2/categories/{}/privileges'.format(category_id), **payload)

        return response_code, json_response
