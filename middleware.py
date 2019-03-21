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
                encoded_jwt = jwt.encode({'id': request.user.id,
                                          'username': request.user.username,
                                          'email': request.user.email},
                                         django_settings.OPENEDX_NODEBB_DISCUSSION['SECRET'],
                                         algorithm=django_settings.OPENEDX_NODEBB_DISCUSSION['ALGORITHM'])
                response.set_cookie('token', encoded_jwt, domain=django_settings.NODEBB_DOMAIN)
            else:
                response.delete_cookie('token', domain=django_settings.NODEBB_DOMAIN)
        except AttributeError:
            pass
        return response
