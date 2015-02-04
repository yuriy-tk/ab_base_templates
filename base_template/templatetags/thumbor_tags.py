#encoding: utf-8
from libthumbor import CryptoURL
from django_jinja import library
from django.conf import settings


@library.global_function
def thumbor_url(image_url, width=0, height=0, smart=True):
    crypto = CryptoURL(key=settings.THUMBOR_SECURITY_KEY)
    return '%s%s' % (settings.THUMBOR_SERVER, crypto.generate(
        width=width,
        height=height,
        smart=smart,
        image_url=image_url
    ))

@library.global_function
def thumbor_list(_list, attr='src', width=0, height=0, smart=True):
    result_list = []
    for obj in _list:
        if isinstance(obj, dict):
            obj[attr] = thumbor_url(obj[attr], width=width, height=height, smart=smart)
            result_list.append(obj)
        else:
            result_list.append(thumbor_url(obj, width=width, height=height, smart=smart))
    return result_list