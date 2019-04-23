#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains the Category Class for NodeBB Client
"""

from openedx.features.openedx_nodebb_discussion.client import Client
from openedx.features.openedx_nodebb_discussion.client.utils import save_category_relation_into_db

DEFAULT_PRIVILEGES = [
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

DEFAULT_GROUPS = [
    'registered-users',
    'guests',
    'spiders'
]


class NodeBBCategory(Client):
    """
    Category Class responsible to make connection with NodeBB Client for categories related operations.
    """

    def create(self, course_id, **payload):
        """
        Creates a new NodeBB Category.

        Args:
            course_id (CourseKey) : Id of course for which we have to create group.

            **payload (dictionary): All other params to pass for category creation, like category_name, type.
            payload: {
                name: "course_name"
            }

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
        of that category. So, we first have to delete the default privileges in order to assign group specific
        privileges.

        Args:
            category_id (int): Category from which we are going to delete privileges.

        Returns:
             tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        payload = {
            'privileges': DEFAULT_PRIVILEGES,
            'groups': DEFAULT_GROUPS
        }

        return self.delete('/api/v2/categories/{}/privileges'.format(category_id), **payload)

    def add_course_group_permission(self, category_id, group_name):
        """
        Assign privileges to the group and then add the group into category.

        Args:
            category_id (int): Category to assign group and privileges.
            group_name (str): Group to assign to Category.

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        payload = {
            'privileges': DEFAULT_PRIVILEGES,
            'groups': [
                group_name
            ]
        }
        return self.put('/api/v2/categories/{}/privileges'.format(category_id), **payload)

    def delete_category(self, category_id):
        """
        Delete Category from NodeBB.

        Args:
            category_id (int): Category to delete.

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.
        """
        return self.delete('/api/v2/categories/{}'.format(category_id))
