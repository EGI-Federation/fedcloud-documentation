.. toctree::

Introduction
============

EGI Cloud Compute gives you the ability to deploy and scale virtual machines
on-demand. It offers computational resources in a secure and isolated
environment contolled via APIs without the overhead of managing physical
servers.

Cloud Compute service is provided through a federation of IaaS cloud sites that
offer:

.. TODO: do we have nice link for resource discovery?

* Single Sign-On via `EGI Check-in <https://www.egi.eu/services/check-in/>`_,
  users can login into every provider with their institutional credentials and
  using modern industry standards like `OpenID Connect <https://openid.net/connect/>`_.

* Global VM image catalogue at `AppDB <https://appdb.egi.eu>`_ with pre-configured
  Virtual Machine images that are automatically replicated to every provider
  based on your community needs.

* Resource discovery features to easily understand which providers are support
  your community and what are their capabilities.

* `Global accounting <https://accounting.egi.eu/cloud/>`_ that aggregates and
  allows visualisation of usage information across the whole federation.

* `Monitoring of Availability and Reliability of the providers <http://argo.egi.eu/status-fedcloud>`_
  to ensure SLAs are met.

The flexibility of the Infrastructure as a Service can benefit various use
cases and usage models. Besides serving compute/data intensive analysis
workflows, Web services and interactive applications can be also integrated
with and hosted on this infrastructure. Contextualisation and other deployment
features can help application operators fine tune services in the cloud,
meeting software (OS and software packages), hardware (number of cores,
amount of RAM, etc.) and other types of needs (e.g. orchestration, scalability).

Since the opening of the EGI Federated Cloud, the following usage models have
emerged:

* **Service hosting**: the EGI Federated Cloud can be used to host any IT
  service as web servers, databases, etc. Cloud features, as elasticity, can
  help users to provide better performance and reliable services.

  * Example: `NBIS Web Services <https://www.egi.eu/use-cases/scientific-applications-tools/nbis-toolkit/>`_,
    `Peachnote analysis platform <https://www.egi.eu/news/peachnote-in-unison-with-egi/>`_.

* **Compute and data intensive**: applications needing considerable amount of
  resources in term of computation and/or memory and/or intensive I/O. Ad-hoc
  computing environments can be created in the EGI cloud providers to satisfy
  very hard HW resource requirements.

  * Example: `VERCE platform <https://www.egi.eu/news/new-egi-use-case-a-close-look-at-the-amatrice-earthquake/>`_,
    `The Genetics of Salmonella Infections <https://www.egi.eu/use-cases/research-stories/the-genetics-of-salmonella-infections/>`_,
    `The Chipster Platform <https://www.egi.eu/use-cases/research-stories/new-viruses-implicated-in-fatal-snake-disease/>`_.

* **Datasets repository**: the EGI Cloud can be used to store and manage large
  datasets exploiting the big amount of disk storage available in the Federation.

* **Disposable and testing environments**: environments for training or testing
  new developments.

  * Example: `Training infrastructure <https://wiki.egi.eu/wiki/Training_infrastructure>`_.


Getting access
--------------


Cloud Compute service is accessed through **Virtual Organisations (VOs)**. A VO
is a grouping of IaaS cloud providers from the federation, who allocate capacity
for a specific user group. Users with similar interest/requirements can join or
form a VO to gather resources from EGI cloud providers - typically for a given
project, experiment or use case. There are generic VOs too, for example the
fedcloud.egi.eu VO, which is open for any user who wants to experiment with the
service. **You have to join a VO before you can interact with the cloud
resources**, while higher level services (PaaS, SaaS) do not always require
VO membership.

Most of the existing VOs in EGI rely on X.509 certificates for user
authentication. While we are transitioning to a certificate-less experience for
using the service, membership to the VO still require users to obtain a personal
certificate from a recognised Certification Authoriy (unless you have one
already)

Obtaining a certificate
^^^^^^^^^^^^^^^^^^^^^^^

The easiest option is to get an 'eScience Personal' certificate online from the
Terena Certificate Service CA. Check here the countries where this is available,
and follow the link to the respective CA page at the `TCS participants <https://www.terena.org/activities/tcs/participants.html>`_
list (See FAQs for details.)

If eScience Personal certificate is not available in your country, then obtain
a certificate from a regular `https://www.eugridpma.org/members/worldmap/ <IGTF CA>`_
(this requires personal visit at the CA).

Join pilot VO
^^^^^^^^^^^^^

The `fedcloud.egi.eu Virtual Organisation <https://operations-portal.egi.eu/vo/view/voname/fedcloud.egi.eu>`_
serves as a test ground for users to try the Cloud Compute service and to
prototype and validate applications. It can be used for up to 6 month by any
new user.

.. warning::

  * After the 6-month long membership in the fedcloud.egi.eu VO, you will need
    to move to a production VO, or establish a new VO.

  * The resources are not guaranteed and may be removed without notice by
    providers. **Back-up frequently to avoid loosing your work!**


Other VOs
^^^^^^^^^

Pre-existing VOs of EGI can be also used on IaaS cloud providers. Consult with
your VO manager.  If none of the existing VOs matches your use case, then a
new VO can be created. Place an order in `EGI Marketplace <https://marketplace.egi.eu/31-cloud-compute>`_
and we will invite providers from the infrastructure to support your needs.

You can browse existing VOs at the `EGI Operations Portal <https://operations-portal.egi.eu/vo/search>`_
(filter for cloud in the middleware column).
