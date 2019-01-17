#!/usr/bin/env python

# in case someone is trying this with python 2
from __future__ import print_function

import json
import os
import requests

# URL Parse
try:
    # Python 2.x
    from urlparse import urlparse, urlunparse, urljoin
except ImportError:
    # Python 3.x
    from urllib.parse import urlparse, urlunparse, urljoin


def get_access_token(checkin_url, client_id, client_secret, refresh_token):
    refresh_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'scope': 'openid email profile',
    }
    r = requests.post(urljoin(checkin_url, "oidc/token"),
                      auth=(client_id, client_secret), data=refresh_data)
    return r.json()['access_token']


def get_keystone_url(os_auth_url, path):
    url = urlparse(os_auth_url)
    prefix = url.path.rstrip('/')
    if prefix.endswith('v2.0') or prefix.endswith('v3'):
        prefix = os.path.dirname(prefix)
    path = os.path.join(prefix, path)
    return urlunparse((url[0], url[1], path, url[3], url[4], url[5]))


def get_unscoped_token(os_auth_url, access_token):
    url = get_keystone_url(
        os_auth_url,
        "/v3/OS-FEDERATION/identity_providers/egi.eu/protocols/oidc/auth")
    r = requests.post(url,
                      headers={'Authorization': 'Bearer %s' % access_token})
    return r.headers['X-Subject-Token']


def get_scoped_token(os_auth_url, os_project_id, unscoped_token):
    url = get_keystone_url(os_auth_url, "/v3/auth/tokens")
    token_body = {
        "auth": {
            "identity": {
                "methods": ["token"],
                "token": {"id": unscoped_token}
            },
            "scope": {"project": {"id": os_project_id}}
        }
    }
    r = requests.post(url, headers={'content-type': 'application/json'},
                      data=json.dumps(token_body))
    return r.headers['X-Subject-Token']


def main():
    # read from environment
    checkin_url = os.environ.get('CHECKIN_URL', 'https://aai.egi.eu')
    client_id = os.environ.get('CHECKIN_CLIENT_ID', '')
    client_secret = os.environ.get('CHECKIN_CLIENT_SECRET', '')
    refresh_token = os.environ.get('CHECKIN_REFRESH_TOKEN', '')

    os_auth_url = os.environ.get('OS_AUTH_URL', '')
    os_project_id = os.environ.get('OS_PROJECT_ID', '')

    access_token = get_access_token(checkin_url, client_id, client_secret,
                                    refresh_token)
    token = get_scoped_token(os_auth_url, os_project_id,
                             get_unscoped_token(os_auth_url, access_token))
    print(token, end='')


if __name__ == '__main__':
    main()
