from os import environ

# all auth site id
SITE_ID = int(environ.get('SITE_ID', 2))

# all auth configs

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SOCIALACCOUNT_LOGIN_ON_GET = True

ACCOUNT_DEFAULT_HTTP_PROTOCOL = environ.get(
    'ACCOUNT_DEFAULT_HTTP_PROTOCOL', 'https'
)
