"""
Contains the MiddleWare Class for NodeBB
"""

import jwt

from django.conf import settings as django_settings


class UserSessionSharingMiddleware(object):
    """
    Middleware to set jwt login token on sign in
    Used for session sharing with NodeBB community
    """

    def process_response(self, request, response):
        try:
            if request.user.is_authenticated():
                user_data = {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email
                }
                jwt_secret = django_settings.OPENEDX_NODEBB_DISCUSSION['DISCUSSION_JWT_SECRET']
                jwt_algorithm = django_settings.OPENEDX_NODEBB_DISCUSSION['DISCUSSION_JWT_ALGORITHM']

                encoded_jwt = jwt.encode(user_data, jwt_secret, jwt_algorithm)
                response.set_cookie('token', encoded_jwt, domain=django_settings.NODEBB_SETTINGS['DOMAIN'])
            else:
                response.delete_cookie('token', domain=django_settings.NODEBB_SETTINGS['DOMAIN'])
        except AttributeError:
            pass
        return response
