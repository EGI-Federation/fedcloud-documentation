.. toctree::

.. _`FedCloud Check-in client`: https://aai.egi.eu/fedcloud

Using OpenStack providers
=========================

`OpenStack <https://openstack.org>`_ providers of the EGI Cloud Compute service
offer native OpenStack features via native APIs integrated with EGI Check-in
accounts.

The extensive `OpenStack user documentation <https://docs.openstack.org/user/>`_
includes details on every OpenStack project, most providers offer access to:

* keystone, for identity

* nova, for VM management

* glance, for VM image management

* cinder, for block storage

* neutron, for network management

* horizon, as a web dashboard

.. TODO(enolfc): horizon? how to know if available

Web-dashboard of the integrated providers can be accessed using your EGI
Check-in credentials directly: select *OpenID Connect* or *EGI Check-in*
in the **Authenticate using** drop-down menu of the login screen. You can
explore `Horizon dashboard documentation <https://docs.openstack.org/horizon/rocky/user/>`_
for more information on how to manage your resources from the browser. The rest
of this guide will focus on CLI/API access.


Installation
------------

.. TODO(enolfc): this should be moved to a global installation section,
   probably once we have some basic client around


**TBC**

.. code-block:: console

   pip install requests
   pip install openstackclient

* `jq` to easily manage JSON output


Add IGTF CA to python's CA store:

.. code-block:: console

   cat /etc/grid-security/certificates/*.pem >> $(python -m requests.certs)

Authentication
--------------

Check the documentation at :ref:`oidc-auth-using-check-in` on how to get the
right crendentials for accessing the providers.

OpenStack token for other clients
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Most OpenStack clients allow authentication with tokens, so you can easily use
them with EGI Cloud providers just doing a first step for obtaining the token.
With the OpenStack client you can use the following command to set the OS_TOKEN
variable with the needed token:

.. code-block:: console

   $ OS_TOKEN=$(openstack --os-auth-type v3oidcaccesstoken \
               --os-protocol openid --os-identity-provider egi.eu \
               --os-auth-url <keystone  url> \
               --os-access-token <your access token> \
               --os-project-id <your project id> token issue -c id -f value)

You can refresh the access token and obtain an OpenStack token in a single
:download:`../get-token.py` script expecting your credentials to be available in
the environment:

* ``CHECKIN_CLIENT_ID``: Your Check-in client id (get it from
  `FedCloud Check-in client`_)
* ``CHECKIN_CLIENT_SECRET``: Your Check-in client secret (get it from
  `FedCloud Check-in client`_)
* ``CHECKIN_REFRESH_TOKEN``: Your Check-in refresh token (get it from
  `FedCloud Check-in client`_)
* ``OS_AUTH_URL``: Keystone URL (depends on the provider, you can get it in
  `GOCDB <https://goc.egi.eu>`_)
* ``OS_PROJECT_ID``: OpenStack project to use (See script above for
  obtaining it)

Optionally set the ``CHECKIN_URL`` to the Check-in endpoint
(https://aai-dev.eu.eu/ if testing on the devel environment).

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

Useful commands with OpenStack CLI
----------------------------------

Please refer to the `nova documentation <https://docs.openstack.org/nova/rocky/user/>`_
for a complete guide on the VM management features of OpenStack. We list in the
sections below some useful commands for the EGI Cloud.

Registering an existing ssh key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It's possible to register an ssh key that can later be used as the default ssh
key for the default user of the VM (via the ``--key-name`` argument to
`openstack server create``):

.. code-block:: console

   openstack keypair create --public-key ~/.ssh/id_rsa.pub mykey

Creating a VM
^^^^^^^^^^^^^

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

* `OpenStack: launch an instance on the provider network <https://docs.openstack.org/mitaka/install-guide-obs/launch-instance-provider.html>`_
* `OpenStack: Manging IP addresses <https://docs.openstack.org/ocata/user-guide/cli-manage-ip-addresses.html>`_

Using cloud-init
^^^^^^^^^^^^^^^^

.. code-block:: console

   openstack server create --flavor m3.medium \
     --image d0a89aa8-9644-408d-a023-4dcc1148ca01 \
     --user-data userdata.txt --key-name My_Key server01.example.com

* `OpenStack: providing user data (cloud-init) <https://docs.openstack.org/nova/queens/user/user-data.html>`_
* `cloudinit documentation <https://cloudinit.readthedocs.io/en/latest/index.html>`_

Shell script data as user data
::::::::::::::::::::::::::::::

.. code-block:: shell

   #!/bin/sh
   adduser --disabled-password --gecos "" clouduser

cloud-config data as user data
::::::::::::::::::::::::::::::

.. code-block:: yaml

   #cloud-config
   hostname: mynode
   fqdn: mynode.example.com
   manage_etc_hosts: true

* `Official cloud-config examples <https://cloudinit.readthedocs.io/en/latest/topics/examples.html#yaml-examples>`_
* `Cloud-init example <https://www.zetta.io/en/help/articles-tutorials/customizing-instance-deployment-cloud-init/>`_


Creating a snapshot image from running VM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can create a new image from a snapshot of an existing VM that will allow
you to easily recover a previous version of your VM.

.. code-block:: console

   openstack server image create <your VM> --name <name of the snapshot>

Once the snapshot is ready (``openstack image show <name of the snapshot>`` will
give your the details you can use it as any other image at the provider:

.. code-block:: console

   openstack server create --flavor <flavor> \
     --image <name of the snapshot> \
     <name of the new VM>

You can override files in the snapshot if needed, e.g. changing the SSH keys:

.. code-block:: console

   openstack server create --flavor <flavor> \
     --image <name of the snapshot> \
     --file /home/ubuntu/.ssh/authorized_keys=my_new_keys \
     <name of the new VM>

Terraform
---------

`Terraform <https://terraform.io>`_ supports EGI Cloud OpenStack providers by
using valid access tokens for Keystone. For using this, just configure your
provider as usual in Terraform, but do not include user/password informaton:

.. code-block:: terraform

  # Configure the OpenStack Provider
  provider "openstack" {
    project_id = "<your project id>"
    auth_url    = "http://<your keystone url>/v3"
  }

  # Create a server
  resource "openstack_compute_instance_v2" "test-server" {
    # ...
  }

when launching Terraform, set the ``OS_TOKEN`` environment variable to a valid
token as shown in :ref:OpenStack token for other clients. You may also
set the Keystone URL and project id in the ``OS_AUTH_URL`` and ``OS_PROJECT_ID``
environment variables:

.. code-block:: terraform

   provider "openstack" {
   }

   data "openstack_images_image_v2" "ubuntu16" {
     most_recent = true

     properties {
       APPLIANCE_MPURI = "https://appdb.egi.eu/store/vo/image/8df7ba00-8467-57aa-bf1e-05754a2a73bf:6428/"
     }
   }

   data "openstack_compute_flavor_v2" "small" {
     vcpus = 1
     ram   = 2048
     disk  = 20
   }

   resource "openstack_compute_instance_v2" "vm" {
     name = "testvm"
     image_id = "${data.openstack_images_image_v2.ubuntu16.id}"
     flavor_id = "${data.openstack_compute_flavor_v2.small.id}"
     security_groups = ["default"]
   }


.. code-block:: console

   $ export CHECKIN_CLIENT_ID=<CLIENT_ID>
   $ export CHECKIN_CLIENT_SECRET=<CLIENT_SECRET>
   $ export CHECKIN_REFRESH_TOKEN=<REFRESH_TOKEN>
   $ export OS_AUTH_URL=<OPENSTACK_URL>
   $ export OS_PROJECT_ID=<PROJECT_ID>
   $ export OS_TOKEN=$(python get-token.py)
   $ terraform plan
   Refreshing Terraform state in-memory prior to plan...
   The refreshed state will be used to calculate this plan, but will not be
   persisted to local or remote state storage.

   data.openstack_compute_flavor_v2.small: Refreshing state...
   data.openstack_images_image_v2.ubuntu16: Refreshing state...

   ------------------------------------------------------------------------

   An execution plan has been generated and is shown below.
   Resource actions are indicated with the following symbols:
     + create

   Terraform will perform the following actions:

     + openstack_compute_instance_v2.vm
         id:                         <computed>
         access_ip_v4:               <computed>
         access_ip_v6:               <computed>
         all_metadata.%:             <computed>
         availability_zone:          <computed>
         flavor_id:                  "2"
         flavor_name:                <computed>
         force_delete:               "false"
         image_id:                   "ceb0434d-37af-4d1f-9efe-13f6f9937df2"
         image_name:                 <computed>
         name:                       "testvm"
         network.#:                  <computed>
         power_state:                "active"
         region:                     <computed>
         security_groups.#:          "1"
         security_groups.3814588639: "default"
         stop_before_destroy:        "false"


   Plan: 1 to add, 0 to change, 0 to destroy.

   ------------------------------------------------------------------------

   Note: You didn't specify an "-out" parameter to save this plan, so Terraform
   can't guarantee that exactly these actions will be performed if
   "terraform apply" is subsequently run.

Note that as in the example above you can get images using information from
AppDB if needed.

libcloud
--------

`Apache libcloud <https://libcloud.apache.org/index.html>`_ support OpenStack
and EGI authentication mechanisms by setting the ``ex_force_auth_version`` to
``3.x_oidc_access_token`` or ``2.0_voms`` respectivelt. Check the `libcloud
docs on connecting to OpenStack <https://libcloud.readthedocs.io/en/latest/compute/drivers/openstack.html#connecting-to-the-openstack-installation>`_
for details. See below two code samples for using them

OpenID Connect
^^^^^^^^^^^^^^

.. code-block:: python

   import requests

   from libcloud.compute.types import Provider
   from libcloud.compute.providers import get_driver

   refresh_data = {
       'client_id': '<your client_id>',
       'client_secret': '<your client_secret>',
       'grant_type': 'refresh_token',
       'refresh_token': '<your refresh_token>',
       'scope': 'openid email profile',
   }

   r = requests.post("https://aai.egi.eu/oidc/token",
                     auth=(client_id, client_secret),
                     data=refresh_data)

   access_token = r.json()['access_token']

   OpenStack = get_driver(Provider.OPENSTACK)
   # first parameter is the identity provider: "egi.eu"
   # Second parameter is the access_token
   # The protocol 'openid' is specified in ex_tenant_name, and tenant/project cannot be selected :(
   driver = OpenStack('egi.eu', access_token, ex_tenant_name='openid',
                      ex_force_auth_url='https://keystone_url:5000',
                      ex_force_auth_version='3.x_oidc_access_token')

VOMS
^^^^

.. code-block:: python

   from libcloud.compute.types import Provider
   from libcloud.compute.providers import get_driver

   OpenStack = get_driver(Provider.OPENSTACK)
   # assume your proxy is available at /tmp/x509up_u1000
   # you can obtain a proxy with the voms-proxy-init command
   # no need for username
   driver = OpenStack(None, '/tmp/x509up_u1000', ex_tenant_name='EGI_FCTF',
                      ex_force_auth_url='https://sbgcloud.in2p3.fr:5000',
                      ex_force_auth_version='2.0_voms')
