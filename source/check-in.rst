.. toctree::

.. _oidc-auth-using-check-in:

OIDC authentication using Check-in
==================================

Providers natively integrated with EGI Check-in support
`OpenID Connect <http://openid.net/connect/>`_ for authentication on Keystone 
with the `OS-FEDERATION extension of Keystone v3 API <https://developer.openstack.org/api-ref/identity/v3-ext/index.html#os-federation-api>`_.
The OS-FEDERATION has a set of API calls that allow getting an unscoped token
and Keystone assume the URLs for these calls to be protected by some
authentication mechanism (SAML, OpenID Connect, ...) that will make sure the
user is valid. Once the user is granted by the underlying authentication,
Keystone will perform the authorisation based on a mapping configured by the
provider. `Mappings <https://developer.openstack.org/api-ref/identity/v3-ext/index.html#mappings>`_
restrict the allowed users and maps them to local groups or specific local
accounts. If the mapping is successful, an unscoped token will be returned.
This is a regular OpenStack unscoped token that can be scoped to any of the
allowed projects as with any other authentication mechanism.

Obtaining an access token
^^^^^^^^^^^^^^^^^^^^^^^^^

Access tokens can obtained via several mechanisms, usually involving the use of
a web server and a browser. Command line clients/APIs without access to a
browser or interactive prompt for user authentication can use refresh tokens. A
refresh token is a special token that is used to generate additional access
tokens. This allows you to have short-lived access tokens without having to
collect credentials every single time one expires. You can request this token
alongside the access and/or ID tokens as part of a user’s initial
authentication flow.

In the case of EGI Check-in, we have created a special client meant to obtain
your personal refresh token and client credentials that will allow the
obtention of access tokens as needed. You can access the client at
https://aai.egi.eu/fedcloud/ and click on 'Authorise' to log in with your
Check-in credentials to obtain:

* a client id
* a client secret
* a refresh token

All of them can be used to obtain the needed access token, here using curl:

.. code-block:: console

   $ curl -X POST -u '<client id>':'<client secret>'  \
   l      -d 'client_id=<client id>&<client secret>&grant_type=refresh_token&refresh_token=<refresh token>&scope=openid%20email%20profile' \
          'https://aai.egi.eu/oidc/token' | python -m json.tool;
     % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
   100  2066    0  1743  100   323   2970    550 --:--:-- --:--:-- --:--:--  2974
   {
       "access_token": "<your access token>,
       "expires_in": 3599,
       "id_token": "<your id token>",
       "scope": "openid profile email",
       "token_type": "Bearer"
   }
