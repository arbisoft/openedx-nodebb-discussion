#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    User Class for NodeBB Client
"""
from __future__ import unicode_literals

from openedx.features.openedx_nodebb_discussion.client import Client

from .utils import save_category_relation_into_db


class NodeBBCategory(Client):
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
