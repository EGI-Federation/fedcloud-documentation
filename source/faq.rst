.. toctree::

FAQ
===

Basics
------

How can I get access to the EGI.eu Federated Cloud?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a VO available for 6 months piloting activities that any researcher in
Europe can join. Just place an order into the `EGI Marketplace <https://marketplace.egi.eu/31-cloud-compute>`_.

How can I get an OAuth2.0 token?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Authentication via CLI or API requires a valid Check-in token. The
FedCloud Check-in client allows you to get one as needed. Check the
authentication guide for more information.

How can I get the list of the EGI Cloud providers?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The list of certified providers is available in `GOCDB <https://goc.egi.eu>`_.
The ``egicli endpoint list`` command can help you to get that list:

.. code-block:: console

   $ egicli endpoint list
   Site                type                URL
   ------------------  ------------------  ------------------------------------------------
   IFCA-LCG2           org.openstack.nova  https://api.cloud.ifca.es:5000/v3/
   IN2P3-IRES          org.openstack.nova  https://sbgcloud.in2p3.fr:5000/v3
   UA-BITP             org.openstack.nova  https://openstack.bitp.kiev.ua:5000/v3
   RECAS-BARI          org.openstack.nova  https://cloud.recas.ba.infn.it:5000/v3
   NCG-INGRID-PT       org.openstack.nova  https://nimbus.ncg.ingrid.pt:5000/v3
   CLOUDIFIN           org.openstack.nova  https://cloud-ctrl.nipne.ro:443/v3
   IISAS-GPUCloud      org.openstack.nova  https://keystone3.ui.savba.sk:5000/v3/
   IISAS-FedCloud      org.openstack.nova  https://nova.ui.savba.sk:5000/v3/
   UNIV-LILLE          org.openstack.nova  https://thor.univ-lille.fr:5000/v3
   INFN-PADOVA-STACK   org.openstack.nova  https://egi-cloud.pd.infn.it:443/v3
   CYFRONET-CLOUD      org.openstack.nova  https://api.cloud.cyfronet.pl:5000/v3/
   SCAI                org.openstack.nova  https://fc.scai.fraunhofer.de:5000/v3
   CESNET-MCC          org.openstack.nova  https://identity.cloud.muni.cz/v3
   INFN-CATANIA-STACK  org.openstack.nova  https://stack-server.ct.infn.it:35357/v3
   CESGA               org.openstack.nova  https://fedcloud-osservices.egi.cesga.es:5000/v3
   100IT               org.openstack.nova  https://cloud-egi.100percentit.com:5000/v3/

The providers also generate dynamic information about their characteristics via
the Argo Messaging System.

Managing VMs
------------

How can I assign a public IP to my VM?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some providers do not automatically assign a public IP address to a VM during
the creation phase. In this case, you can attach a public IP by first
allocating a new public IP and then assigning it to the VM.

How can I assign a DNS name to my VM?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you need a domain name for your VMs, we offer a Dynamic DNS service that
allows any EGI user to create names for VMs under the `fedcloud.eu` domain.

Just go to `EGI Cloud nsupdate <https://nsupdate.fedcloud.eu>`_ and logint with
your Check-in account. Once in, you can click on "Add host" to register a new
hostname in an available domain.

.. How can I log into a VM?
   ^^^^^^^^^^^^^^^^^^^^^^^^

.. How can I install software?
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^

What is contextualisation?
^^^^^^^^^^^^^^^^^^^^^^^^^^

The contextualisation of is the process of installing, configuring and
preparing software upon boot time on a pre-defined virtual machine image.
This way, the pre-defined images can be stored as generic and small as possible,
since customisations will take place on boot time.

Contextualisation is particularly useful for:

* Configuration not known until instantiation (e.g. data location).

* Private Information (e.g. host certs)

* Software that changes frequently or under development.

The contextualisation requires passing some data to the VMs on instantiation
(the context) and handling that context in the VM.

How can I inject my public SSH key into the machine?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The best way to login into the virtual server is to use SSH keys. If you don't
have one, you need to generate it with the ``ssh-keygen`` command:

.. code-block:: console

   ssh-keygen -f fedcloud

This will generate two files:

* ``fedcloud``, the private key. This file should never be shared

* ``fedcloud.pub``, the public key. That will be sent to your VM.

To inject the public SSH key into the VM you can use the `key-name` option
when creating the VM in OpenStack. Check `keypair management <https://docs.openstack.org/python-openstackclient/pike/cli/command-objects/keypair.html>`_
option in OpenStack documentation. This key will be available for the default
configured user of the VM (e.g. ``ubuntu`` for Ubuntu, ``centos`` for CentOS).

You can also create users with keys with a contextualisation file:

.. code-block:: yaml

   #cloud-config
   users:
     - name: cloudadm
       sudo: ALL=(ALL) NOPASSWD:ALL
       lock-passwd: true
       ssh-import-id: cloudadm
       ssh-authorized-keys:
         - <paste here the contents of your SSH key pub file>

.. warning::

   YAML format requires that the spaces at the beginning of each line is
   respected in order to be correctly parsed by ``cloud-init``.


How can I use a contextualisation file?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have a contextualisation file, you can use it with the ``--user-data``
option to ``server create`` in OpenStack.

.. code-block:: shell

   $ openstack server create --flavor <your-flavor> --image <your image> \
               --user-data <your contextualisation file> \
               <server name>

.. note::

   We recommend using ``cloud-init`` for contextualisation. EGI images in AppDB
   do support ``cloud-init``. Check the `documentation <http://cloudinit.readthedocs.org/ cloud-init>`_
   for more information.

How can I pass secrets to my VMs?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

EGI Cloud endpoints use https so information passed to contextualise the VMs
can be assumed to be safe and only readable within your VM. However, take into
account that anyone with access to the VM may be able to access also the
contextualisation information.

The disk on my VM is full, how can I get more space?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are several ways to increase the disk space available at the VM. The
fastest and easiest one is to use block storage, creating a new storage disk
device and attaching it to the VM.


How can I keep my data after the VM is stopped?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After a VM is stopped and unless backed up in a block storage volume, all data
in the VM is destroyed and cannot be recovered. To ensure your data will be
available after the VM is deleted, you need to use some form of persistent
storage.
