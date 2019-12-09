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

Quick start
-----------

#. Log into the `VMOps dashboard <https://dashboard.appdb.egi.eu/vmops>`_ using
   EGI Check-in.

#. Click on "Create a new VM Topology" to start the topology builder, this will
   guide you through a set of steps:

   #. Select the Virtual Appliance you want to start, these are the same shown
      in the `AppDB Cloud Marketplace <https://appdb.egi.eu/browse/cloud>`_,
      you can use the search field to find your VA;

      .. image:: img/vmops_va_select.png
         :width: 900px
         :alt: Select the VA

   #. select the VO to use when instantiating the VA;

   #. select the provider where to instantiate the VA; and finally

   #. select the template (VM instance type) of the instance that will
      determine the number of cores, memory and disk space used in your VM.

#. Now you will be presented with a summary page where you can further customise
   your VM by:

   * Adding more VMs to the topology

   * Adding block storage devices to the VMs

   * Define contextualisation parameters (e.g. add new users, execute some
     script)

   .. image:: img/vmops_settings.png
      :width: 900px
      :alt: Topology settings

#. Click on "Launch" and your deployment will be submitted to the infrastructure.

The topology you just created will appear on your "Topologies" with all the
details about it, clicking on a VM of a topology will give you details about
its status and IP. VMOps will create a default ``cloudadm`` user for you and
create ssh-key pair for login (you can create as many users as needed with
the contextualisation options of the wizard described above).

.. image:: img/vmops_vm.png
   :width: 900px
   :alt: VM details
