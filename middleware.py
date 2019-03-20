import jwt


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
                                         'secret', algorithm='HS256')
                response.set_cookie('token', encoded_jwt, domain="localhost")
            else:
                response.delete_cookie('token', domain="localhost")
        except AttributeError:
            pass
        return response
