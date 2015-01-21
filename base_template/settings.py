from django.conf import settings

MEDIA_VERSION = getattr(settings, 'MEDIA_VERSION', 'v1')
BASE_MEDIA_URL = getattr(settings, 'BASE_MEDIA_URL', 'http://img.s3.ua/ab/')
STATIC_URL_IMG = getattr(settings, 'STATIC_URL_IMG', 'http://img.s3.ua/ab/')
STATIC_URL_CSS = getattr(settings, 'STATIC_URL_CSS', 'http://css.s3.ua/ab/')
STATIC_URL_JS = getattr(settings, 'STATIC_URL_JS', 'http://js.s3.ua/ab/')
BASE_STATIC_URL = getattr(settings, 'BASE_STATIC_URL', 'http://s3.ua/ab/')