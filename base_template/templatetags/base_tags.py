#encoding: utf-8
from django import template
from django_jinja import library
from django.utils.translation import get_language
from django.template.loader import render_to_string
from django.conf import settings as django_settings

from base_template import settings



register = template.Library()


@library.global_function
@register.simple_tag
def locale_switcher(request, template='base_template/common/locale_switcher.jinja'): 
    locales = [lang_code for lang_code, name in django_settings.LANGUAGES]
    path = request.path
    if path[1:3] in locales:
        path = request.path[3:]
    GET = request.GET
    if hasattr(request, 'GET_backuped'):
        GET = request.GET_backuped
    if GET:
        path = u'{0}?{1}'.format(path, GET.urlencode())

    return render_to_string(template, {'path': path, 'settings': django_settings, 'current_language': get_language()})

@library.global_function
@register.simple_tag
def get_host():
    return django_settings.HOST


@library.global_function
@register.simple_tag
def locale():
    _language = get_language()
    if _language == django_settings.LANGUAGE_CODE:
        return ''
    return '/%s' % _language


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