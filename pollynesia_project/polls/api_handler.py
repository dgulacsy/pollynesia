import requests
import os
import logging

logger = logging.getLogger(__name__)


IPSTACK_API_KEY = os.environ.get('IPSTACK_API_KEY')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    # WARNING: Using static dummy IPv6 instead of 'ip' to see IPStack API functionality as it would not work when run locally
    return '2001:4c4e:24c0:3700:b5d8:4c11:7106:8282'


def get_location_from_ip(ip):
    r = requests.get(
        'http://api.ipstack.com/{0}?access_key={1}'.format(ip, IPSTACK_API_KEY))
    response_json = r.json()
    try:
        response_json = {
            'country': response_json['country_name'],
            'region': response_json['region_name'],
            'city': response_json['city'],
            'latitude': response_json['latitude'],
            'longitude': response_json['longitude']
        }
    except(KeyError):
        try:
            logger.warning('%s - %s' %
                           (response_json['type'], response_json['info']))
        except(KeyError):
            logger.warning('API response invalid')
            return None
        return None
    return response_json
