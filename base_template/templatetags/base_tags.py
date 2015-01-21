#encoding: utf-8
from django import template
from django_jinja import library
from django.utils.translation import get_language

from base_template import settings


register = template.Library()

@register.simple_tag
@library.global_function
def language():
    return get_language()


def do_media(domain, path):
    return '{0}{1}?{2}'.format(domain, path, settings.MEDIA_VERSION)


@library.global_function
@register.simple_tag
def image(path):
    return do_media(settings.BASE_MEDIA_URL, path)


@library.global_function
@register.simple_tag
def static_image(path):
    return do_media(settings.STATIC_URL_IMG, path)

@library.global_function
@register.simple_tag
def stylesheet(path):
    return do_media(settings.STATIC_URL_CSS, path)


@library.global_function
@register.simple_tag
def javascript(path):
    return do_media(settings.STATIC_URL_JS, path)


@library.global_function
@register.simple_tag
def plugin(path):
    return do_media(settings.BASE_STATIC_URL, path)