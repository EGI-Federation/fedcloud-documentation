.. toctree::

Using FedCloud with OpenStack Native APIs
=========================================

Authentication
--------------

EGI Check-in
^^^^^^^^^^^^

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
"""""""""""""""""""""""""

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


Installing required dependencies
--------------------------------

Adding IGTF CA to python's CA store.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console
   cat /etc/grid-security/certificates/*.pem >> $(python -m requests.certs)

Installing requirements
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console
   pip install requests
   pip install openstackclient

* `jq` to easily manage JSON output

Discovering projects
--------------------

You may not know which projects are available to your user at a given provider,
but you can easily discover them using the Keystone API. The :doc:`../get-projects.py`
script will just do that for you (requires requests library). It expects these
variables to be defined in the environment:

The script expects your credentials to be available in the environment:

* CHECKIN_CLIENT_ID: Your Check-in client id (get it from https://aai.egi.eu/fedcloud)
* CHECKIN_CLIENT_SECRET: Your Check-in client secret (get it from https://aai.egi.eu/fedcloud)
* CHECKIN_REFRESH_TOKEN: Your Check-in refresh token (get it from https://aai.egi.eu/fedcloud)
* OS_AUTH_URL: Keystone URL (depends on the provider, you can get it in https://goc.egi.eu)

.. code-block:: console
   # Export OIDC env
   export CHECKIN_CLIENT_ID=<CLIENT_ID>
   export CHECKIN_CLIENT_SECRET=<CLIENT_SECRET>
   export CHECKIN_REFRESH_TOKEN=<REFRESH_TOKEN>
   # Select OpenStack endpoint
   export OS_AUTH_URL=<OPENSTACK_URL>
   # Retrieve project ID
   python get-projects.py

Using an access token to interact with OpenStack Native APIs
------------------------------------------------------------

Putting everything together it's possible to interact with OpenStack using the OIDC token.

.. code-block:: console
   # Export OIDC env
   export CHECKIN_CLIENT_ID=<CLIENT_ID>
   export CHECKIN_CLIENT_SECRET=<CLIENT_SECRET>
   export CHECKIN_REFRESH_TOKEN=<REFRESH_TOKEN>
   # Select OpenStack endpoint
   export OS_AUTH_URL=<OPENSTACK_URL>
   # Retrieve project ID
   python get-projects.py
   export OS_PROJECT_ID=<PROJECT_ID>
   # Retrieve access token
   export OS_ACCESS_TOKEN=$(curl -s -X POST -u "$CHECKIN_CLIENT_ID":"$CHECKIN_CLIENT_SECRET"  \
        -d "client_id=$CHECKIN_CLIENT_ID&$CHECKIN_CLIENT_SECRET&grant_type=refresh_token&refresh_token=$CHECKIN_REFRESH_TOKEN&scope=openid%20email%20profile" \
       'https://aai.egi.eu/oidc/token' | jq -r '.access_token')
   export OS_IDENTITY_PROVIDER=egi.eu
   export OS_AUTH_TYPE=v3oidcaccesstoken
   export OS_PROTOCOL=oidc
   openstack image list

Getting an OpenStack token with OIDC
------------------------------------

Most OpenStack client allow authentication with tokens, so you can easily use
them with EGI Cloud providers just doing a first step for obtaining the token.
With the OpenStack client you can use the following command to set the OS_TOKEN
variable with the needed token:

.. code-block:: console
   $ OS_TOKEN=$(openstack --os-auth-type v3oidcaccesstoken \
               --os-protocol oidc --os-identity-provider egi.eu \
               --os-auth-url <keystone  url> \
               --os-access-token <your access token> \
               --os-project-id <your project id> token issue -c id -f value)

You can refresh the access token and obtain an OpenStack token in a single
:doc:`../get-token.py` script expecting your credentials to be available in
the environment:

* CHECKIN_CLIENT_ID: Your Check-in client id (get it from https://aai.egi.eu/fedcloud)
* CHECKIN_CLIENT_SECRET: Your Check-in client secret (get it from https://aai.egi.eu/fedcloud)
* CHECKIN_REFRESH_TOKEN: Your Check-in refresh token (get it from https://aai.egi.eu/fedcloud)
* OS_AUTH_URL: Keystone URL (depends on the provider, you can get it in https://goc.egi.eu)
* OS_PROJECT_ID: OpenStack project to use (See script above for obtaining it)

Optionally set the CHECKIN_URL to the Check-in endpoint (https://aai-dev.eu.eu/
if testing on the devel environment).

.. code-block:: console
   # Export OIDC env
   export CHECKIN_CLIENT_ID=<CLIENT_ID>
   export CHECKIN_CLIENT_SECRET=<CLIENT_SECRET>
   export CHECKIN_REFRESH_TOKEN=<REFRESH_TOKEN>
   # Select OpenStack endpoint
   export OS_AUTH_URL=<OPENSTACK_URL>
   # Retrieve project ID
   python get-projects.py
   export OS_PROJECT_ID=<PROJECT_ID>
   # Retrieve OpenStack token
   export OS_TOKEN=$(python get-token.py)
   echo $OS_TOKEN

Registering an existing ssh key
-------------------------------

It's possible to register an ssh key that can later be used while creating
servers (Virtual Machines).
When selected using `--key-name` while creating a server, it will be
automatically added the ssh configuration.

.. code-block:: console
   openstack keypair create --public-key ~/.ssh/id_rsa.pub mykey

Creating a VM using OpenStack native API
----------------------------------------

.. code-block:: console
   openstack flavor list
   FLAVOR=<FLAVOR_NAME>
   openstack image list
   IMAGE_ID=<IMAGE_ID>
   openstack network list
   # Pick FedCloud network
   NETWORK_ID=<NETOWRK_ID>
   openstack security group list
   openstack server create --flavor $FLAVOR --image $IMAGE_ID \
     --nic net-id=$NETWORK_ID --security-group default \
     --key-name mykey oneprovider
   # Creating a floating IP
   openstack floating ip create <NETOWRK_NAME>
   # Assigning floating IP to server
   openstack server add floating ip <SERVER_ID> <IP>
   # Removing floating IP from server
   openstack server show <SERVER_ID>
   # Deleting server
   openstack server remove floating ip <SERVER_ID> <IP>
   openstack server delete <SERVER_ID>
   # Deleting floating IP
   openstack floating ip delete <IP>

* `OpenStack: launch an instance on the provicer network <https://docs.openstack.org/mitaka/install-guide-obs/launch-instance-provider.html>`_
* `OpenStack: Manging IP addresses <https://docs.openstack.org/ocata/user-guide/cli-manage-ip-addresses.html>`_


Using cloud-init with OpenStack
-------------------------------

.. code-block:: console
   openstack server create --flavor m3.medium \
     --image d0a89aa8-9644-408d-a023-4dcc1148ca01 \
     --user-data userdata.txt --key-name My_Key server01.example.com

* `OpenStack: providing user data (cloud-init) <https://docs.openstack.org/nova/queens/user/user-data.html>`_
* `cloudinit documentation <https://cloudinit.readthedocs.io/en/latest/index.html>`_

Shell script data as user data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell
   #!/bin/sh
   adduser --disabled-password --gecos "" clouduser

cloud-config data as user data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml
   #cloud-config
   hostname: mynode
   fqdn: mynode.example.com
   manage_etc_hosts: true

* `Official cloud-config examples <https://cloudinit.readthedocs.io/en/latest/topics/examples.html#yaml-examples>`_
* `Cloud-init example <https://www.zetta.io/en/help/articles-tutorials/customizing-instance-deployment-cloud-init/>`_

Other resources
---------------

* `EGI FedCloud OpenStack usage <https://wiki.egi.eu/wiki/Federated_Cloud_APIs_and_SDKs#OpenStack>`_
