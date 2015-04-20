#encoding: utf-8
import json
import time
import requests
import urllib2
from lxml import etree
from datetime import datetime
from jinja2 import Markup
from django_jinja import library
from django.utils.translation import get_language, ugettext_lazy as _
from django.template.loader import render_to_string
from django.conf import settings as django_settings
from django.core.cache import cache

from base_template import settings


@library.global_function
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

    return Markup(render_to_string(template, {'path': path, 'settings': django_settings,
                                              'current_language': get_language()}))

@library.global_function
def get_host():
    return django_settings.HOST


@library.global_function
def locale():
    _language = get_language()
    if _language == django_settings.LANGUAGE_CODE:
        return ''
    return '/%s' % _language


@library.global_function
def language():
    return get_language()


def do_media(domain, path):
    return '{0}{1}?{2}'.format(domain, path, settings.MEDIA_VERSION)


def do_media_inline(domain, path):
    response = requests.get(do_media(domain, path))
    if response.status_code == 200:
        return response.text
    return ''


@library.global_function
def image(path):
    return do_media(settings.BASE_MEDIA_URL, path)


@library.global_function
def static_image(path):
    return do_media(settings.STATIC_URL_IMG, path)


@library.global_function
def stylesheet(path):
    return do_media(settings.STATIC_URL_CSS, path)


@library.global_function
def stylesheet_inline(path):
    return Markup('<style>%s</style>' % do_media_inline(settings.STATIC_URL_CSS, path))



@library.global_function
def javascript(path):
    return do_media(settings.STATIC_URL_JS, path)


@library.global_function
def plugin(path):
    return do_media(settings.BASE_STATIC_URL, path)


@library.global_function
def now(_format):
    return datetime.now().strftime(_format)


def human_time(d):
    mon = [_(u'января'), _(u'февраля'), _(u'марта'), _(u'апреля'), _(u'мая'), _(u'июня'),
           _(u'июля'), _(u'августа'), _(u'сентября'), _(u'октября'), _(u'ноября'), _(u'декабря'),]
    n = datetime.now()         # Текущее время
    deltas = time.mktime(n.timetuple()) - time.mktime(d.timetuple())   # Дельта в секундах
    delta = deltas / 60                 # Дельта в минутах
    if deltas < 1:
        deltas = 1
    if deltas < 60:                     # Секунды
        return _(u"%d сек. назад") % deltas
    elif delta < 60:                    # Минуты
        return _(u"%d мин. назад") % delta
    elif delta < (n.hour * 60 + n.minute):
        shour = round(delta/60)
        if shour in (1,21):
            shours = _(u"час")
        elif shour in (2,3,4,22,23,24):
            shours = _(u"часа")
        else:
            shours = _(u"часов")
        return _(u"%(hour)d %(hours)s назад") % {'hour': shour, 'hours': shours}
    elif delta < (n.hour * 60 + n.minute + 60 * 24):
        return _(u"вчера, %(hour)02d:%(minute)02d") % {'hour': d.hour, 'minute': d.minute}
    elif d.year == n.year:
        return _(u"%(day)d %(month)s") % {'day': d.day, 'month': mon[d.month - 1]}
    else:
        return _(u"%(day)d %(month)s %(year)d") % {'day':d.day, 'month': mon[d.month - 1],'year': d.year}


@library.filter
def human_time_from_string(time_string, _format='%Y-%m-%d %H:%M:%S'):
    try:
        obj = datetime.strptime(time_string, _format)
        return human_time(obj)
    except Exception, e:
        return str(time_string)


@library.filter
def price_format(price):
    """
    Visually divides input string with spaces.
    For example:
        >>> price_format('1324567890')
        '1 234 567 890'
    """
    p = price.strip()
    d = len(p) % 3
    l = [p[i:i+3] for i in xrange(d, len(p), 3)]
    return p[:d] + ' ' + ' '.join(l)


@library.global_function
def currency_json():
    currency_json = cache.get('currency_json')
    if not currency_json:
        response = requests.get('http://avtobazar.ua/api/v1/currency/?format=json')
        currency_json = response.json()
        cache.set('currency_json', currency_json, 60*60*3)
    return Markup(json.dumps(currency_json['objects']))


@library.global_function
def get_url_for_pattern(pattern, data):
    return pattern % data

@library.global_function
def render_spares_catalog_link(make, make_translit):
    common = u'/zapchasti/catalog/'
    if make and make_translit:
        cache_key = 'zapchasti-link-{0}-{1}'.format(make, make_translit)
        if cache.get(cache_key):
            return cache.get(cache_key)
        try:
            xml_data = urllib2.urlopen(
                'http://avtobazar.ua/zapchasti/catalog/get_ab_mark.php?markid=%s' % make,
                timeout=1).read()
        except IOError:
            pass
        else:
            try:
                xml = etree.XML(xml_data)
            except (ValueError, etree.XMLSyntaxError):
                pass
            else:
                make_id = xml.find('id').text
                if make_translit and not make_id == 'None':
                    result = u'/zapchasti/catalog/%s-%s/' % (make_translit, make_id)
                    cache.set(cache_key, result, 60*60)
                    return result
    return common



def get_currency_rate(currency):
    from classifier.models import Classifier
    cache_key = 'currency:rate:%s' % currency
    if cache.get(cache_key):
        rate = cache.get(cache_key)
    else:
        rate = Classifier.objects.get(translit=currency).rate
        cache.set(cache_key, rate, 60*60*24)
    return rate


@library.filter
def price_by_currency(price, currency):
    rate = get_currency_rate(currency)
    try:
        return int(round(float(price)/rate))
    except:
        return 0


@library.filter
def price_currency(price, currency):
    return price_by_currency(price, currency)


@library.filter
def price_to_usd(price, currency):
    rate = get_currency_rate(currency)
    return int(round(float(price)*rate))


@library.global_function
def adverts_count_all(period='index', template='base_template/common/adverts_count_all.jinja'):
    mongodb = django_settings.MONGODB
    count = None
    if mongodb:
        count = mongodb.adverts_count.find_one({'type': 'all'})
    context = {'period': period, 'count': count, 'mongodb': bool(mongodb)}
    if count is None:
        context['count'] = {
            'total': None,
            'hour': None,
            'day': None,
            'index': None,
        }
    elif period != 'index':
        context['count_period'] = count[period]
    return Markup(render_to_string(template, context))


@library.global_function
def render_alternate_link(request):
    html = []
    current_language = get_language()
    path = request.get_full_path()
    if path[1:3] == current_language:
        path = path[3:]
    for lang, title in settings.LANGUAGES:
        if not lang == current_language:
            if not lang == settings.LANGUAGE_CODE:
                path = '/%s%s' % (lang, path)
            html.append(u'<link rel="alternate" hreflang="%s" href="http://avtobazar.ua%s" />' % (lang, path))
    html.append(u'<meta http-equiv="content-Language" content="%s" />' % current_language)
    return  Markup(''.join(html))