from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x%#vo$sp5*!tjc!!^yme2gmj_s8ywo0u98-1(1g56v*afc&37b'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


DEFAULT_CURRENCY = "CZK"



try:
    from .local import *
except ImportError:
    pass
