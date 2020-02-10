ECAS environment with EC3
-------------------------

The following guide is intended for researchers who want to use ECAS, a complete
environment enabling data analysis experiments, in the EGI cloud.

ECAS (ENES Climate Analytics Service) is part of the EOSC-hub service catalog
and aims to:

#. provide server-based computation,

#. avoid data transfer, and

#. improve reusability of data and workflows (FAIR approach).

It relies on `Ophidia <http://ophidia.cmcc.it/>`_, a data analytics framework
for eScience, which provides declarative, server-side, and parallel data
analysis, jointly with an internal storage model able to efficiently deal with
multidimensional data and a hierarchical data organization to manage large data
volumes (“datacubes”), and on JupyterHub, to give users access to ready-to-use
computational environments and resources.

Thanks to the Elastic Cloud Compute Cluster (EC3) platform, operated by the
`Polytechnic University of Valencia (UPV) <http://www.upv.es/index-en.html>`_,i
researchers will be able to rely on the EGI Cloud Compute service to scale up
to larger simulations without being worried about the complexity of the
underlying infrastructure.


Objectives
==========

This guide will show how to:

* deploy an ECAS elastic cluster of VMs in order to automatically install and
  configure the whole ECAS environment services, i.e. JupyterHub, PyOphidia,
  several Python libraries such as numpy, matplotlib and Basemap;

* perform data intensive analysis using the Ophidia HPDA framework;

* access the ECAS JupyterHub interface to create and share documents containing
  live code, equations, visualizations and explanatory text.


..
   enolfc: I think this is not relevant for this documentation
   EC3 architecture
   ================

   The Elastic Cloud Computing Cluster (EC3) is a framework to create elastic
   virtual clusters on top of Infrastructure as a Service (IaaS) providers is
   composed by the following components:

   * Infrastructure Manager (IM)

   * Resource and Application Description Language (RADL)

   * CLUES

   * EC3 as a Service (EC3aaS)

   For further details about the architecture of the EC3 service, please refer to
   the official documentation.

Deploy an ECAS cluster with EC3
===============================

In the latest release of the EC3 platform, tailored to support the EGI Applications on Demand (AoD) service, a new Ansible receipt is now available for researchers interested to deploy ECAS cluster on the EGI Infrastuctrure.
Additional details on how to configure and deploy an ECAS cluster on EGI resources are provided in the next sections.

ECAS in now available in the latest release of the EC3 platform supporting the
EGI Applications on Demand (AoD). The next sections provide details on how to
configure and deploy an ECAS cluster on EGI resources.

Configure and deploy the cluster
::::::::::::::::::::::::::::::::

To configure and deploy a Virtual Elastic Cluster using EC3aaS, access the
`EC3 platform front page <https://servproject.i3m.upv.es/ec3-ltos/index.php>`_
and click on the **"Deploy your cluster"** link as shown in the figure below:

.. image:: img/ecas-front.png
   :width: 800px
   :alt: EC3 front page.

A wizard will guide the user during the cluster configuration process.
Specifically, the general wizard steps include:

* **LRMS selection**: choose **ECAS** from the list of LRMSs (Local Resource
  Management System) that can be automatically installed and configured by EC3.

.. image:: img/ecas-lrms.png
   :width: 800px
   :alt: LRMS selection.


* **Endpoint**: the endpoints of the providers where to deploy the ECAS elastic
  cluster. The endpoints serving the ``vo.access.egi.eu`` VO are dynamically
  retrieved from the `EGI Application DataBase <https://appdb.egi.eu/>`_ using
  REST APIs.


.. image:: img/ecas-endpoint.png
   :width: 800px
   :alt: Endpoint selection.

* **Operating System**: choose EGI CentOS7 as cluster OS.

.. image:: img/ecas-os.png
   :width: 800px
   :alt: Operating System selection.

* **Instance details**, in terms of CPU and RAM to allocate for the front-endu
  and the working nodes.

.. image:: img/ecas-instance.png
   :width: 800px
   :alt: Instance details.

* **Cluster’s size and name**: the name of the cluster and the maximum number
  of nodes of the cluster, without including the front-end. This value indicates
  the maximum number of working nodes that the cluster can scale. Initially,
  the cluster is created with the front-end and only one working node: the
  other working nodes are powered on on-demand.

.. image:: img/ecas-size.png
   :width: 800px
   :alt: Cluster size and name.

* **Resume and Launch**: a summary of the chosen cluster configuration. To start
  the deployment process, click the Submit button.

.. image:: img/ecas-summary.png
   :width: 800px
   :alt: Resume and Launch.

When the front-end node of the cluster has been successfully deployed, the user
will be notified with the credentials to access via SSH.

.. image:: img/ecas-end.png
   :width: 800px
   :alt: ECAS cluster connection details.

The cluster details are available by clicking on the "Manage your deployed
clusters" link on the front page:

.. image:: img/ecas-manage.png
   :width: 800px
   :alt: Manage your clusters.

.. note::

   The configuration of the cluster may take some time. Please wait for its
   completion before starting to start using the cluster.

Accessing the cluster
:::::::::::::::::::::

To access the front-end of the elastics cluster:

* download the SSH private key provided by the EC3 portal;
* change its permissions to ``600``;
* access via SSH providing the key as identity file for public key authentication.

.. code-block:: console

   [fabrizio@MBP EC3]$ ssh -i key.pem cloudadm@134.158.151.218
   Last login: Mon Nov 18 11:37:29 2019 from torito.i3m.upv.es
   [cloudadm@oph-server ~]$ sudo su -
   [root@oph-server ~]#

Both the front-end and the working node are configured by Ansible. This process
usually takes some time. User can monitor the status of the cluster
configuration using the ``is_cluster_ready`` command-line tool:

.. code-block:: console

   [root@oph-server ~]# is_cluster_ready
   Cluster is still configuring.

The cluster is successfully configured when the command returns the following
message:

.. code-block:: console

   [root@oph-server ~]# is_cluster_ready
   Cluster configured!

As SLURM is used as workload manager, it is possible to check the status of the
working nodes by using the sinfo command, which provides information about
Slurm nodes and partitions.

.. code-block:: console

   [root@oph-server ~]# sinfo
   PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
   debug*       up   infinite  	1  down* oph-io2
   debug*       up   infinite  	1   idle oph-io1


Accessing the scientific eco-system
:::::::::::::::::::::::::::::::::::

ECASLab provides two different ways to get access to its scientific eco-system:
Ophidia client (``oph_term``) and JupyterHub.

Perform some basic operations with Ophidia
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run the Ophidia terminal as ``ophuser`` user.


.. image:: img/ecas-oph_term.png
   :width: 800px
   :alt: Ophidia terminal.

The default parameters are already defined as environmental variables inside
the ``.bashrc`` file:

.. code-block:: console

   export OPH_SERVER_HOST="127.0.0.1"
   export OPH_SERVER_PORT="11732"
   export OPH_PASSWD="abcd"
   export OPH_USER="oph-test"

Create an empty container and a new datacube with random data and dimensions.

.. image:: img/ecas-container-1.png
   :width: 800px
   :alt: Create container (1).

.. image:: img/ecas-container-2.png
   :width: 800px
   :alt: Create container (2).

Now, you can submit your first operation of data transformation: let’s reduce
the whole datacube in a single value for grid point using the average along the
time:

.. image:: img/ecas-reduce.png
   :width: 800px
   :alt: Reduce datacube.

Let’s have a look at the environment by listing the datacubes and containers in
the session:

.. image:: img/ecas-list.png
   :width: 800px
   :alt: List objects in session.

By default, the Ophidia terminal will use the last output datacube PID. So, you
can use the ``oph_explorecube`` operator to visualize the first 100 values.

.. image:: img/ecas-explore.png
   :width: 800px
   :alt: Explorecube operator.

For further details about the Ophidia operators, please refer to the official
`documentation <http://ophidia.cmcc.it/>`_.


Accessing the Jupyter interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To access the Jupyter interface, open the browser at
``https://<YOUR_CLUSTER_IP>:443/jupyter`` and log in to the system using the
username and password specified in the ``jupyterhub_config.pyp`` configuration
file (see the ``c.Authenticator.whitelist`` and ``c.DummyAuthenticator.password``
lines) located at the ``/root`` folder.

.. image:: img/ecas-jupyterhub.png
   :width: 800px
   :alt: JupyterHub login.

From JupyterHub in ECASLab you can do several things such as:

* create and run a Jupyter Notebook exploiting PyOphidia and Python libraries
  for visualization and plotting (e.g. matplotlib, basemap, NumPy);

* browse the directories, download and update the files in the home folder;

* execute operators and workflows directly from the Ophidia Terminal.

To get started with the ECASLab environment capabilities, open the
``ECAS_Basics.ipynb`` notebook available under the ``notebooks/`` folder in the
home directory.

.. image:: img/ecas-jupyter.png
   :width: 800px
   :alt: Jupyter.

..
   enolfc: This seems again not relevant for the EGI Cloud docs

   How to deploy a virtual cluster with the ECAS environment in EGI
   ================================================================

   * Access the EOSC Marketplace.
   * Select the Elastic Cloud Compute Cluster (EC3) from the list of available
     services.
   * Place an order requesting access to the service.
   * When the service request is approved you will be notified by email.
   * Service orders are usually processed by operators in three working days.

References
==========

* https://ecaslab.cmcc.it/web/home.html

* https://ecaslab.dkrz.de/home.html

* http://ophidia.cmcc.it/

* https://github.com/ECAS-Lab

* https://github.com/OphidiaBigData/ansible-role-ophidia-cluster

* http://www.grycap.upv.es/ec3

* http://www.github.com/grycap/ec3

