.. toctree::

Introduction
============

EGI Cloud Compute gives you the ability to deploy and scale virtual machines
on-demand. It offers computational resources in a secure and isolated
environment controlled via APIs without the overhead of managing physical
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
  datasets exploiting the large amount of disk storage available in the Federation.

* **Disposable and testing environments**: environments for training or testing
  new developments.

  * Example: `Training infrastructure <https://www.egi.eu/services/training-infrastructure/>`_


EGI Federated Cloud task force
------------------------------

The EGI Federated Cloud task force gathers together scientific communities,
R&D projects, and technology and resource providers so they can design the
tools and services that support the federation of providers, can share best
practices, and can offer user support and training in a collaborative fashion.
This enables community cloud solutions to develop faster, with a lower cost and
with a more sustainable future. The task force members:

* Capture requirements from user communities needing federated cloud services.

* Identify, integrate and enhance open source tools and services that enable
  cloud federations for research and education.

* Develop and maintain tools and services to fill gaps in third party solutions
  to reach production quality cloud federations.

* Provide consultancy and training for communities on how to build a federated
  cloud to meet custom community demands under certain constraints.

* Provide training and support for existing and potential users of cloud
  federations about topics, such as how to port or develop cloud-native
  applications; how to operate services in the cloud; or how to join a cloud
  federation as a provider.

* Facilitate the reuse of cloud federation tools and services across
  participating cloud federations to lower total cost of development and to
  improve cloud sustainability.

* Promote Platform as a Service (PaaS) and Software as a Service (SaaS)
  environments that are proven to be robust and reusable across communities to
  interact with federated IaaS.

* Provide service management and security oversight for participating clouds
  and cloud federations.

* Act as a discussion forum where cloud federations can be discussed and
  specific questions can be analysed with top-world experts.

* Organise dissemination and marketing events, workshops and conferences
  relating to the topics of the collaboration.

.. note::

   If you are interested in joining the EGI FedCloud Task Force, please send an
   email to ``fedcloud-tf _at_ mailman.egi.eu`` introducing yourself.

   We hold meetings regularly Tuesdays at 11.00 CE(S)T every two weeks. Check
   our `indico category <https://indico.egi.eu/indico/categoryDisplay.py?categId=159>`_
   for minutes and upcoming events.
