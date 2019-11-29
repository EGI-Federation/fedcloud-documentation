.. toctree::

AppDB VMOps
===========

The `EGI Application Database (AppDB) <https://appdb.egi.eu/>`_ includes a web
GUI for management of Virtual Machines (VMs) on the federated infrastrcutrure.

This GUI is available for a set of `selected VOs <https://wiki.appdb.egi.eu/main:faq:which_vos_are_supported_by_the_vmops_dashboard>`_
If your VO is not listed and you are interested in getting support, please
contact us!

Main user features
------------------

* User identification with Check-in, with customised view of the VAs and
  resource providers based on the VO membership of the user.
   
* Management of VMs in *topologies*, containing one or more instances of a given
  VA.
 
* Attachment of additional block storage to the VM instances.

* Start/Stop VMs without destroying the VM (for all VMs of a topology or for
  individual instances within a topology)
 
* Single control of topologies across the whole federation.

Create (and deploy) a new VM Topology
-------------------------------------

To create (and deploy) a new VM topology, just click on the **New Topology**
button and configure the settings using the Topology Builder interface as
shown in the figure below.

The configuration of a new VM topology is done in four steps:

* Select the **EGI Virtual Appliance** (VA) to be included in the topology
* Select the **Virtual Organisation** (VO) where the topology will be deployed
* Identify the **Provider** where to deploy the topology
* Choose the **VM template** for the VA

.. FIXME: image1

In this example, the topology is composed by only one VA (e.g. EGI Ubuntu
14.04). This VA will be deployed in the CESNET-MetaCloud provider under the
fedcloud.egi.eu VO and using the ``small`` flavour as VM template.

.. FIXME: image2

Clicking on the **Launch** button the deployment process of the VM topology
will start. 

As soon as the topology has been deployed, the user can get the public IP
address of the running VM and download the SSH public key that can be used to
access.

.. FIXME: image3
