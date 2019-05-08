#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains the Group Class for NodeBB Client
"""
from __future__ import unicode_literals

from openedx.features.openedx_nodebb_discussion.client import Client
from openedx.features.openedx_nodebb_discussion.client.utils import (
    save_course_enrollment_in_db, get_edx_user_from_nodebb_uid,
    get_course_id_from_group_slug, remove_course_enrollment_from_db,
    save_group_relation_into_db
)


class NodeBBGroup(Client):
    """
    Group Class responsible to make connection with NodeBB Client for groups related operations.
    """

    def create(self, course_id, **payload):
        """
        Creates a new NodeBB Group.

        Args:
            course_id (CourseKey): Id of course for which we have to create group.

            **payload (dictionary): Payload to send to Api contains name of group.

            payload: {
                name: "name-organization-run",
            }

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
        return self.delete('/api/v2/groups/{}'.format(group_slug))

    def add_member(self, uid, group_slug):
        """
        Add member to the NodeBB group and save its corresponding record in database.

        Args:
            uid (int): NodeBB user id of the  user to be add to group
            group_slug (str): Slug of group user joining.

        Returns:
            tuple: Tuple in the form (response_code, json_response) received from requests call.

        """
        response_code, json_response = self.put('/api/v2/groups/{}/membership/{}'.format(group_slug, uid))

        if response_code == 200:
            course_id = get_course_id_from_group_slug(group_slug)
            edx_user = get_edx_user_from_nodebb_uid(uid)
            save_course_enrollment_in_db(edx_user, course_id)

        return response_code, json_response

    def remove_member(self, uid, group_slug):
        """
        Remove member from NodeBB group and update database accordingly.

        Args:
            uid (int): NodeBB user id of the user to remove from group
            group_slug (str): Slug of group from which the user is being removed.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        response_code, json_response = self.delete('/api/v2/groups/{}/membership/{}'.format(group_slug, uid))

        if response_code == 200:
            course_id = get_course_id_from_group_slug(group_slug)
            edx_user = get_edx_user_from_nodebb_uid(uid)
            remove_course_enrollment_from_db(edx_user, course_id)

        return response_code, json_response
