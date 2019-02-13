.. toctree::

Authentication
==============

.. _oidc-auth-using-check-in:

OpenID Connect using Check-in
-----------------------------

`OpenID Connect <http://openid.net/connect/>`_ is an authentication protocol
based on OAuth 2.0 and replacing the current VOMS-based authentication on the
EGI Cloud.

The providers natively integrated with EGI Check-in are able to authenticate
users with OAuth 2.0 tokens without using any certificates in the process by
relying on the OpenStack Keystone `OS-FEDERATION API <https://developer.openstack.org/api-ref/identity/v3-ext/index.html#os-federation-api>`_.

.. TODO(enolfc): discovery of providers with check-in support?

The process for authentication is as follows:

#. Obtain a valid access token from Check-in. Access tokens are short-lived
   credentials that can be obtained by recognised Check-in clients once a user
   has authenticated.

#. Interchange the Check-in access token for a valid unscoped Keystone token.

#. Discover available projects from Keystone using the unscoped token.

#. Use the unscoped Keystone token to get a scoped token for a valid project.
   Scoped tokens will allow the user to perform operations on the provider.

The sections below detail how to achieve this as a EGI Cloud user.

EGI Check-in FedCloud client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Note them down so you can use them for the next steps.

Discovering projects in Keystone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Your access token will provide you access to a cloud provider, but you may have
access to several different projects within that provider (a project can be
considered as equal to a VO allocation). In order to discover which projects
are available you can do that using the Keystone API.

The :download:`../get-projects.py` script will just do that for you (requires
``requests`` library). It expects these variables to be defined in the
environment:

* ``CHECKIN_CLIENT_ID``: Your Check-in client id (get it from https://aai.egi.eu/fedcloud)
* ``CHECKIN_CLIENT_SECRET``: Your Check-in client secret (get it from https://aai.egi.eu/fedcloud)
* ``CHECKIN_REFRESH_TOKEN``: Your Check-in refresh token (get it from https://aai.egi.eu/fedcloud)
* ``OS_AUTH_URL``: Keystone URL (depends on the provider, you can get it in https://goc.egi.eu)

.. TODO(enolfc): discovery of Keystone URL?

.. code-block:: console

   # Export OIDC env
   export CHECKIN_CLIENT_ID=<CLIENT_ID>
   export CHECKIN_CLIENT_SECRET=<CLIENT_SECRET>
   export CHECKIN_REFRESH_TOKEN=<REFRESH_TOKEN>
   # Select OpenStack endpoint
   export OS_AUTH_URL=<OPENSTACK_URL>
   # Retrieve project ID
   python get-projects.py

.. warning::

   **Use of IGTF CAs**

   If you get certificate validation errors, you may need to install the IGTF
   CAs and configure the request libraries to use them. If you don't have the
   CA certificates installed in your machine, you can get them from the `UMD
   EGI core Trst Anchor Distribution <http://repository.egi.eu/?category_name=cas>`_.

   Once installed, get the location of the requests CA bundle with:

   .. code-block:: console

     python -m requests.certs

   If the output of that command is ``/etc/ssl/certs/ca-certificates.crt``,
   you can add IGTF CAs by executing:

   .. code-block:: console

     cd /usr/local/share/ca-certificates
     for f in /etc/grid-security/certificates/*.pem ; do ln -s $f $(basename $f .pem).crt; done
     update-ca-certificates


   If the output is ``/etc/pki/tls/certs/ca-bundle.crt`` add the IGTF CAs with:

   .. code-block:: console

     cd /etc/pki/ca-trust/source/anchors
     ln -s /etc/grid-security/certificates/*.pem .
     update-ca-trust extract

   Otherwise, you are using internal requests bundle, which can be augmented
   with the IGTF CAs with:

   .. code-block:: console

     cat /etc/grid-security/certificates/*.pem >> $(python -m requests.certs)


Access the provider
^^^^^^^^^^^^^^^^^^^

Once you know which project to use, you can use your regular openstack cli
commands for performing actual operations in the provider:

.. code-block:: console

   # Export OIDC env
   export CHECKIN_CLIENT_ID=<CLIENT_ID>
   export CHECKIN_CLIENT_SECRET=<CLIENT_SECRET>
   export CHECKIN_REFRESH_TOKEN=<REFRESH_TOKEN>
   # Select OpenStack endpoint
   export OS_AUTH_URL=<OPENSTACK_URL>
   # Use the previously discovered ID
   export OS_PROJECT_ID=<PROJECT_ID>
   export OS_IDENTITY_PROVIDER=egi.eu
   export OS_AUTH_TYPE=v3oidcaccesstoken
   export OS_PROTOCOL=openid
   # Retrieve access token
   export OS_ACCESS_TOKEN=$(curl -s -X POST -u "$CHECKIN_CLIENT_ID":"$CHECKIN_CLIENT_SECRET"  \
        -d "client_id=$CHECKIN_CLIENT_ID&$CHECKIN_CLIENT_SECRET&grant_type=refresh_token&refresh_token=$CHECKIN_REFRESH_TOKEN&scope=openid%20email%20profile" \
       'https://aai.egi.eu/oidc/token' | jq -r '.access_token')
   openstack image list

.. note::

   For 3rd party tools that can use token based authentication in OpenStack,
   use the following command (after setting the environment as shown above):


   .. code-block:: console

     export OS_ACCESS_TOKEN=$(curl -s -X POST -u "$CHECKIN_CLIENT_ID":"$CHECKIN_CLIENT_SECRET"  \
        -d "client_id=$CHECKIN_CLIENT_ID&$CHECKIN_CLIENT_SECRET&grant_type=refresh_token&refresh_token=$CHECKIN_REFRESH_TOKEN&scope=openid%20email%20profile" \
       'https://aai.egi.eu/oidc/token' | jq -r '.access_token')
     export OS_TOKEN=$(openstack token issue -c id -f value)


VOMS (to be deprecated)
-----------------------

`VOMS <https://italiangrid.github.io/voms/index.html>`_ uses X.509 proxies
extended with VO information for authentication and authorisation on the
providers.

VOMS configuration
^^^^^^^^^^^^^^^^^^

Every VO needs two different pieces of information:

* the ``vomses`` configuration files, where the details of the VO are stored
  (e.g. name, server, ports). These are stored by default at ``/etc/vomses``
  and are normally named following this convention: ``<vo name>.<server name>``
  (e.g. for fedcloud.egi.eu VO, you would have ``fedcloud.egi.eu.voms1.grid.cesnet.cz``
  and ``fedcloud.egi.eu.voms2.grid.cesnet.cz``.


* the ``.lsc`` files that describe the trust chain of the VOMS server. These are
  stored at ``/etc/grid-security/vomsdir/<vo name>`` and there should be one
  file for each of the VOMS server of the VO.

You can check specific configuration for your VO at the `Operations portal <https://operations-portal.egi.eu/vo>`_.
Normally each VOMS server has a *Configuration Info* link where the exact
information to include in the `vomses` and `.lsc` files.

Valid configuration for ``fedcloud.egi.eu`` is available on the `FedCloud
client VM <https://appdb.egi.eu/store/vappliance/egi.fedcloud.clients>`_ as
generated by the `fedcloud-ui installation script <https://raw.githubusercontent.com/EGI-FCTF/fedcloud-userinterface/master/fedcloud-ui.sh>`_.

VOMS client expects your certificate and private key to be available at
``$HOME/.globus/usercert.pem`` and ``$HOME/.globus/userkey.pem`` respectively.

Creating a proxy
^^^^^^^^^^^^^^^^

Once you have the VO information configured (``vomses`` and ``.lsc``) and your
certificate available in your ``$HOME/.globus`` directory you can create a
VOMS proxy to be used with clients with:

.. code-block:: console

   voms-proxy-init --voms <name of the vo> --rfc

For fedcloud.egi.eu VO:

.. code-block:: console

   voms-proxy-init --voms fedcloud.egi.eu --rfc
   Enter GRID pass phrase:
   Your identity: /DC=org/DC=terena/DC=tcs/C=NL/O=EGI/OU=UCST/CN=Enol Fernandez
   Creating temporary proxy ......................................................... Done
   Contacting  voms1.grid.cesnet.cz:15002 [/DC=cz/DC=cesnet-ca/O=CESNET/CN=voms1.grid.cesnet.cz] "fedcloud.egi.eu" Done
   Creating proxy ................................................................... Done

   Your proxy is valid until Mon Feb  4 23:37:21 2019


Access the providers
^^^^^^^^^^^^^^^^^^^^

VOMS authentication differs from one provider to another depending on the
technology used. There are 3 different cases handled automatically by the
``rOCCI-cli``. For accessing native OpenStack sites there are two different
plugins available for Keystone that are installed with a single library:

.. code-block:: console

  pip install openstack-voms-auth-type


For Keystone-VOMS based installations (Keystone URL ending on ``/v2.0``), just
define the location of your proxy and ``v2voms`` as authorisation plugin:

.. code-block:: console

  openstack --os-auth-url https://<keystone-url>/v2.0 \
            --os-auth-type v2voms --os-x509-user-proxy /tmp/x509up_u1000 \
            token issue
  +---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Field   | Value                                                                                                                                                              |
  +---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | expires | 2019-02-04T12:41:25+0000                                                                                                                                           |
  | id      | gAAAAABcWCTlMoz6Jx9IHF5hj-ZOn-CI17CfX81FTn7yy0ZJ54jkza7QNoQTRU5-KRJkphmes55bcoSaaBRnE3g2clFgY-MR2GVUJZRkCmj9TXsLZ-hVBWXQNENiX9XxUwnavj7KqDn4b9B1K22ijTrjdDVkcdpvMw |
  | user_id | 9310054c2b6f4fd28789ee08c2351221                                                                                                                                   |
  +---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+

For those Keystone installations supporting only ``v3``, specify ``v3voms`` as
authorisation plugin, ``egi.eu`` as identity provider, ``mapped`` as protocol,
and the location of your proxy:

.. code-block:: console

  openstack --os-auth-url https://<keystone url>/v3 \
            --os-auth-type v3voms --os-x509-user-proxy /tmp/x509up_u1000 \
            --os-identity-provider egi.eu --os-protocol mapped \
            token issue
  +---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Field   | Value                                                                                                                                                                                                        |
  +---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | expires | 2019-02-04T12:45:32+0000                                                                                                                                                                                     |
  | id      | gAAAAABcWCXcXGUDpHUYnI1IDLW3MnEpDzivw_OPaau8DQDYxA7gK9XsmOqZh1pL5Uqqs8aM-tHowdJQnJURww2-UhmQVqk5PxbjdnvLeqtXPYURCLaSsbmhkQg6kB311c_ZA1jfgdT-pG6fZz3toeH66SEFX-H0bThSUy0KFLhcZVkrZIbYgTsAOIzFkTfLjOgTw_tNChS8 |
  | user_id | 50fa8516b2554daeae652619ba9ebf96                                                                                                                                                                             |
  +---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
