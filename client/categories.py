#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains the Category Class for NodeBB Client
"""
from __future__ import unicode_literals

from openedx.features.openedx_nodebb_discussion.client import Client
from openedx.features.openedx_nodebb_discussion.client.utils import save_category_relation_into_db


class NodeBBCategory(Client):
    """
    Category Class responsible to make connection with NodeBB Client for categories related operations.
    """
    default_privileges = [
        'groups:find',
        'groups:read',
        'groups:topics:read',
        'groups:topics:create',
        'groups:topics:reply',
        'groups:topics:tag',
        'groups:posts:edit',
        'groups:posts:history',
        'groups:posts:delete',
        'groups:posts:upvote',
        'groups:posts:downvote',
        'groups:topics:delete',
        'groups:posts:view_deleted',
        'groups:purge',
        'groups:moderate'
    ]

    default_groups = [
        'registered-users',
        'guests',
        'spiders'
    ]

    def __init__(self):
        super(NodeBBCategory, self).__init__()

    def create(self, course_id, **payload):
        """
        Creates a new NodeBB Category.

        Args:
            course_id (Course Key) : Course_Key

            **payload (Dictionary): All other params to pass for category creation, like category_name, type.

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.

        """
        response_code, json_response = self.post('/api/v2/categories', **payload)

        if response_code == 200:
            save_category_relation_into_db(course_id=course_id, category_id=json_response['cid'])

        return response_code, json_response

    def delete_default_permissions(self, category_id):
        """
        By default whenever a new category is created in NodeBB, the default groups have some default privileges
        of that category. So, first deletes those default privileges in order to assign some specific privileges
        to the groups that are related to that category.

        Args:
            category_id (int): Category from which we are going to delete privileges.

        Returns:
             tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        payload = {
            'privileges': self.default_privileges,
            'groups': self.default_groups
        }
        response_code, json_response = self.delete('/api/v2/categories/{}/privileges'.format(category_id), **payload)
        return response_code, json_response

    def add_course_group_permission(self, category_id, group_name):
        """
        Assigns group and privileges to category.

        Args:
            category_id (int): Category to assign group and privileges.
            group_name (str): Group to assign to Category.

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        payload = {
            'privileges': self.default_privileges,
            'groups': [
                group_name
            ]
        }
        response_code, json_response = self.put('/api/v2/categories/{}/privileges'.format(category_id), **payload)
        return response_code, json_response

    def delete_category(self, category_id):
        """
        Assigns group and privileges to category.

        Args:
            category_id (int): Category to delete.

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        response_code, json_response = self.delete('/api/v2/categories/{}'.format(category_id))
        return response_code, json_response
