#!/usr/bin/env python

# in case someone is trying this with python 2
from __future__ import print_function

import os
import requests

# URL Parse
try:
    # Python 2.x
    from urlparse import urlparse, urlunparse
except ImportError:
    # Python 3.x
    from urllib.parse import urlparse, urlunparse


def get_access_token(client_id, client_secret, refresh_token):
    refresh_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'scope': 'openid email profile',
    }
    r = requests.post("https://aai.egi.eu/oidc/token",
                      auth=(client_id, client_secret), data=refresh_data)
    return r.json()['access_token']


def get_keystone_url(os_auth_url, path):
    url = urlparse(os_auth_url)
    prefix = url.path.rstrip('/')
    if prefix.endswith('v2.0') or prefix.endswith('v3'):
        prefix = os.path.dirname(prefix)
    path = os.path.join(prefix, path)
    return urlunparse((url[0], url[1], path, url[3], url[4], url[5]))


def get_unscoped_token(os_auth_url, access_token, method='oidc'):
    url = get_keystone_url(
        os_auth_url,
        "/v3/OS-FEDERATION/identity_providers/egi.eu/protocols/%s/auth" %
        method)
    r = requests.post(url,
                      headers={'Authorization': 'Bearer %s' % access_token})
    if r.status_code != 201:
        return get_unscoped_token(os_auth_url, access_token, 'openid')
    else:
        return r.headers['X-Subject-Token']


def get_projects(os_auth_url, unscoped_token):
    url = get_keystone_url(os_auth_url, "/v3/auth/projects")
    r = requests.get(url, headers={'X-Auth-Token': unscoped_token})
    return r.json()['projects']


def main():
    # read from environment
    client_id = os.environ.get('CHECKIN_CLIENT_ID', '')
    client_secret = os.environ.get('CHECKIN_CLIENT_SECRET', '')
    refresh_token = os.environ.get('CHECKIN_REFRESH_TOKEN', '')

    os_auth_url = os.environ.get('OS_AUTH_URL', '')

    access_token = get_access_token(client_id, client_secret, refresh_token)
    unscoped_token = get_unscoped_token(os_auth_url, access_token)
    projects = get_projects(os_auth_url, unscoped_token)
    for p in projects:
        print('ID: %(id)s - Name: %(name)s - Enabled: %(enabled)s' % p)


if __name__ == '__main__':
    main()
