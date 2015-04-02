from django.conf import settings

MEDIA_VERSION = getattr(settings, 'MEDIA_VERSION', 'v1')
BASE_MEDIA_URL = getattr(settings, 'BASE_MEDIA_URL', 'http://img.s3.ua/ab/')
STATIC_URL_IMG = getattr(settings, 'STATIC_URL_IMG', 'http://img.s3.ua/ab/')
STATIC_URL_CSS = getattr(settings, 'STATIC_URL_CSS', 'http://css.s3.ua/ab/')
STATIC_URL_JS = getattr(settings, 'STATIC_URL_JS', 'http://js.s3.ua/ab/')
BASE_STATIC_URL = getattr(settings, 'BASE_STATIC_URL', 'http://s3.ua/ab/')

BASE_PIPELINE_CSS = {
    'proto': {
        'source_filenames': (
          'proto/less/*.less',
        ),
        'output_filename': 'css/proto/base.css',
    },
    'proto_v2': {
        'source_filenames': (
          'proto_v2/less/*.less',
        ),
        'output_filename': 'css/proto_v2/base.css',
    },
}

if hasattr(settings, 'PIPELINE_CSS'):
    settings.PIPELINE_CSS.update(BASE_PIPELINE_CSS)
else:
    settings.PIPELINE_CSS = BASE_PIPELINE_CSS