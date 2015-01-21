from django.conf import settings

MEDIA_VERSION = getattr(settings, 'MEDIA_VERSION', 'v1')
BASE_MEDIA_URL = getattr(settings, 'BASE_MEDIA_URL', 'v1')
STATIC_URL_IMG = getattr(settings, 'STATIC_URL_IMG', 'v1')
STATIC_URL_CSS = getattr(settings, 'STATIC_URL_CSS', 'v1')
STATIC_URL_JS = getattr(settings, 'STATIC_URL_JS', 'v1')
BASE_STATIC_URL = getattr(settings, 'BASE_STATIC_URL', 'v1')