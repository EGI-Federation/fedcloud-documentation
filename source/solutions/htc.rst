Deploying HTC clusters
======================

This document describes how to use the Elastic Cloud Computing Cluster (EC3)
platform to create elastic virtual clusters on the EGI Cloud.

Get EC3 CLI
-----------

EC3 has an official Docker container image available in Docker Hub that can be
used instead of installing the CLI. You can download it with


.. code-block:: console

   ]$ sudo docker pull grycap/ec3

That will allow you to exploit all the potential of EC3 from your computer.

List available EC3 templates
----------------------------

To list the available templates, use the command:

.. code-block:: console

   ]$ sudo docker run -v /var/.ec3/clusters:/root/.ec3/clusters grycap/ec3 templates

   name                    kind                                         summary
   ---------------------------------------------------------------------------------------------------
   blcr                component   Tool for checkpoint the applications.
   centos-ec2          images      CentOS 6.5 amd64 on EC2.
   ckptman             component   Tool to automatically checkpoint applications running on Spot instances.
   docker              component   An open-source tool to deploy applications inside software containers.
   gnuplot             component   A program to generate two- and three-dimensional plots.
   nfs                 component   Tool to configure shared directories inside a network.
   octave              component   A high-level programming language for numerical computations
   openvpn             component   Tool to create a VPN network.
   sge                 main        Install and configure a cluster SGE from distribution repositories.
   slurm               main        Install and configure a cluster SLURM 14.11 from source code.
   torque              main        Install and configure a cluster TORQUE from distribution repositories.
   ubuntu-azure        images      Ubuntu 12.04 amd64 on Azure.
   ubuntu-ec2          images      Ubuntu 14.04 amd64 on EC2.

List EC3 clusters
------------------

To list the available running clusters, use the command:

.. code-block:: console

   ]$ sudo docker run -v /var/.ec3/clusters:/root/.ec3/clusters grycap/ec3 list

       name        state           IP           nodes
   -------------------------------------------------------
    cluster      configured    212.189.145.XXX    0
    

Authorization file
^^^^^^^^^^^^^^^^^^

The authorization file stores in plain text the credentials to access the cloud
providers, the IM service and the VMRC service. Each line of the file is
composed by pairs of key and value separated by semicolon, and refers to a
single credential. The key and value should be separated by ``=``, that is
**an equal sign preceded and followed by one white space at least**.

Example of cloud provider with OIDC-based authentication:

.. code-block:: console

   $ cat /tmp/auth.dat
   id = PROVIDER_ID; type = OpenStack; host = KEYSTONE_ENDPOINT; username = egi.eu; tenant = openid; domain = DOMAIN_NAME; auth_version = 3.x_oidc_access_token; password = OIDC_ACCESS_TOKEN
   
   Where:
   * `id` is the id of the cloud provider (e.g.: in2p3ostegi)
   * `host` is the public IP address of the cloud provider Keystone service (e.g.: https://sbgcloud.in2p3.fr:5000/v3)
   * `domain` is the project tenant in the cloud provider (e.g.: EGI_access)
   * `password` is the access token

Get an access token
-------------------
Login the EGI AAI Check-In [EGI AAI Check-In](https://aai.egi.eu/fedcloud) service. 
Copy and paste in your terminal the CURL command to generate a valid access token valid for 1h.

Create an elastic EC3 cluster
-----------------------------

To launch a cluster, you can use the recipes that you have locally by mounting
the folder as a volume, or create your dedicated ones. Also, it is
recommendable to maintain the data of active clusters locally, by mounting a
volume. In the next example, we are going to deploy a new Torque/Maui cluster
on one cloud provider of the EGI Federation.

The cluster will be configured with the following templates:

.. code-block::

   #torque (default template),
   #configure_nfs (patched template),
   #centos7-OIDC-IN2P3-IRES_Torque (user's template),
   #cluster_configure (user's template)

User’s templates are stored in ``$HOME/ec3/templates``

.. code-block:: console

   docker run -v /home/centos/:/tmp/ \
              -v /home/centos/ec3/templates:/root/.ec3/templates \
              -v /var/.ec3/clusters:/root/.ec3/clusters grycap/ec3 launch cluster \
              torque centos7-OIDC-IN2P3-IRES_Torque cluster_configure refreshtoken configure_nfs \
              -a /tmp/auth.dat

   Creating infrastructure
   Infrastructure successfully created with ID: 529c62ec-343e-11e9-8b1d-300000000002
   Front-end state: launching
   Front-end state: pending
   Front-end state: running
   IP: 212.189.145.XXX
   Front-end configured with IP 212.189.145.XXX
   Transferring infrastructure
   Front-end ready!

Templates
^^^^^^^^^

This section contains the templates used to configure the cluster.

``ec3/templates/cluster_configure.radl``

.. code-block:: console

   configure front (
   @begin
   ---
     - vars:
        - USERS:
          - { name: user01, password: <PASSWORD> }
          - { name: user02, password: <PASSWORD> }
   [..]
       tasks:
       - user:
           name: "{{ item.name }}"
           password: "{{ item.password }}"
           shell: /bin/bash
           append: yes
           state: present
         with_items: "{{ USERS }}"
       - name: Install missing dependences in Debian system
         apt: pkg={{ item }} state=present
         with_items:
          - build-essential
          - mpich
          - gcc
          - g++
          - vim
         become: yes
         when: ansible_os_family == "Debian"
       - name: Install missing dependences in RedHat distribution
         yum: pkg={{ item }} state=present
         with_items:
          - "@Development Tools"
          - csh
          - tcsh
          - tcl-devel
          - openmpi
          - openmpi-devel
          - gcc-c++.x86_64
          - mlocate
          - vim
         become: yes
         when: ansible_os_family == "RedHat"
       - name: SSH without password
         include_role:
           name: grycap.ssh
         vars:
           ssh_type_of_node: front
           ssh_user: "{{ user.name }}"
         loop: '{{ USERS }}'
         loop_control:
           loop_var: user     
   @end
   )
   configure wn (
   @begin
   ---
     - vars:
        - USERS:
          - { name: user01, password: <PASSWORD> }
          - { name: user02, password: <PASSWORD> }
   [..]
       tasks:
       - user:
           name: "{{ item.name }}"
           password: "{{ item.password }}"
           shell: /bin/bash
           append: yes
           state: present
         with_items: "{{ USERS }}"
       - name: Install missing dependences in Debian system
         apt: pkg={{ item }} state=present
         with_items:
          - build-essential
          - mpich
          - gcc
          - g++
          - vim
         become: yes
         when: ansible_os_family == "Debian"
       - name: Install missing dependences in RedHat distribution
         yum: pkg={{ item }} state=present
         with_items:
          - "@Development Tools"
          - csh
          - tcsh
          - tcl-devel
          - openmpi
          - openmpi-devel
          - gcc-c++.x86_64
          - mlocate
          - vim
         become: yes
         when: ansible_os_family == "RedHat"         
       - name: SSH without password
         include_role:
           name: grycap.ssh
         vars:
           ssh_type_of_node: wn
           ssh_user: "{{ user.name }}"
         loop: '{{ USERS }}'
         loop_control:
           loop_var: user
   @end
   )

``centos7-OIDC-IN2P3-IRES_Torque.radl``

.. code-block:: console

   description ubuntu-1604-occi-INFN-CATANIA-STACK (
       kind = 'images' and
       short = 'CentOS7' and
       content = 'FEDCLOUD Image for CentOS7'
   )
   network public (
       provider_id = 'ext-net' and
       outports contains '22/tcp' and
   )
   system front (
       cpu.arch = 'x86_64' and
       cpu.count >= 2 and
       memory.size >= 4096m and
       disk.0.os.name = 'linux' and
       # vo.access.egi.eu tenant
       disk.0.image.url = 'ost://sbgcloud.in2p3.fr/20de522d-1242-4211-be13-bcef51058a5e' and
       disk.0.os.credentials.username = 'centos'
   )
   system wn (
       cpu.arch = 'x86_64' and
       cpu.count >= 2 and
       memory.size >= 2048m and
       ec3_max_instances = 10 and # maximum number of working nodes in the cluster
       instance_type = 'http://schemas.openstack.org/template/resource#98f6ac88-e773-48b8-85bf-86415b421996' and
       disk.0.os.name = 'linux' and
       # vo.access.egi.eu tenant
       disk.0.image.url = 'ost://sbgcloud.in2p3.fr/20de522d-1242-4211-be13-bcef51058a5e' and
       disk.0.os.credentials.username = 'centos'
   )

``configure_nfs.radl``

.. code-block:: console

   # http://www.server-world.info/en/note?os=CentOS_6&p=nfs&f=1
   # http://www.server-world.info/en/note?os=CentOS_7&p=nfs
   description nfs (
       kind = 'component' and
       short = 'Tool to configure shared directories inside a network.' And
       content = 'Network File System (NFS) client allows you to access shared directories from Linux client.
       This recipe installs nfs from the repository and shares the /home/ubuntu directory with all the nodes
       that compose the cluster.
   Webpage: http://www.grycap.upv.es/clues/'
   )
   network public (
       outports contains '111/tcp' and
       outports contains '111/udp' and
       outports contains '2046/tcp' and
       outports contains '2046/udp' and
       outports contains '2047/tcp' and
       outports contains '2047/udp' and
       outports contains '2048/tcp' and
       outports contains '2048/udp' and
       outports contains '2049/tcp' and
       outports contains '2049/udp' and
       outports contains '892/tcp' and
       outports contains '892/udp' and
       outports contains '32803/tcp' and
       outports contains '32769/udp'
   )
   system front (
       ec3_templates contains 'nfs' and
       disk.0.applications contains (name = 'ansible.modules.grycap.nfs')
   )
   configure front (
   @begin
     - roles:
       - { role: 'grycap.nfs', nfs_mode: 'front', nfs_exports: [{path: "/home", export: wn*.localdomain(rw,async,no_root_squash,no_subtree_check,insecure)"}] }
   @end
   )
   system wn ( ec3_templates contains 'nfs' )
   configure wn (
   @begin
     - roles:
       - { role: 'grycap.nfs', nfs_mode: 'wn', nfs_client_imports: [{ local: "/home", remote: "/home", server_host: '{{ hostvars[groups["front"][0]]["IM_NODE_PRIVATE_IP"] }}' }] }
   @end
   )
   include nfs_misc (
     template = 'openports'
   )

Access the EC3 cluster
----------------------

To access the cluster, use the command:

.. code-block:: console

   ]$ sudo docker run -ti -v /var/.ec3/clusters:/root/.ec3/clusters grycap/ec3 ssh cluster

   Warning: Permanently added '134.158.151.205' (ECDSA) to the list of known hosts.
   Last login: Tue Jul 21 14:47:29 2020 from torito.i3m.upv.es

Configuration of the cluster
----------------------------

Enable Password-based authentication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Change settings in ``/etc/ssh/sshd_config``

.. code-block:: console

   # Change to no to disable tunnelled clear text passwords
   PasswordAuthentication yes

and restart the ssh daemon:

.. code-block:: console

   sudo service sshd restart

Configure the number of processors of the cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   ]$ cat /var/spool/torque/server_priv/nodes
   wn1 np=XX
   wn2 np=XX
   [...]

To obtain the number of CPU/cores (np) in Linux, use the command:

.. code-block:: console

   ]$ lscpu | grep -i CPU
   CPU op-mode(s):         32-bit, 64-bit
   CPU(s):                 16
   On-line CPU(s) list:    0-15
   CPU family:             6
   Model name:             Intel(R) Xeon(R) CPU E5520  @ 2.27GHz
   CPU MHz:                2266.858
   NUMA node0 CPU(s):      0-3,8-11
   NUMA node1 CPU(s):      4-7,12-15

Test the cluster
^^^^^^^^^^^^^^^^

Create a simple test script:

.. code-block:: console

   ]$ cat test.sh
   #!/bin/bash
   #PBS -N job
   #PBS -q batch

   #cd $PBS_O_WORKDIR/
   hostname -f
   sleep 5

Submit to the batch queue:

.. code-block:: console

   ]$ qsub -l nodes=2 test.sh

Destroy the cluster
-------------------

To destroy the running cluster, use the command:

.. code-block:: console

   ]$ sudo docker run -ti -v /var/.ec3/clusters:/root/.ec3/clusters grycap/ec3 destroy cluster
   WARNING: you are going to delete the infrastructure (including frontend and nodes).
   Continue [y/N]? y
   Success deleting the cluster!
