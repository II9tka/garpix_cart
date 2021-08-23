from garpixcms.settings import *  # noqa

INSTALLED_APPS += [
    'garpix_cart',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

CART_SESSION_KEY = 'cart'
