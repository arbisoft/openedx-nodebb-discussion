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

NODEBB_ADMIN_UID = 1
BAD_REQUEST = 400
CONNECTION_ERROR = 500
