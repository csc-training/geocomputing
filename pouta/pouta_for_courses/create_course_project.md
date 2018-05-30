
## Creating a cPouta project for a course
You will create a cPouta project that will be use to manage the resources that will be used during a course. The resources in the cPouta account for the infrastructure (virtual machines, firewalls...) that are used in the course.

### New user
You need to have a CSC account to be able to use cPouta or any CSC's resources in general. Not necessarily all the people involved in the course needs to have a CSC account, only the ones responsible for the course.

The following two roles are necessary and need to have a CSC's account:
- Course's main contact person (also called principal investigator, PI): responsible to create the cPouta project and administer the project.
- IT support person: has system administration skills. Manages the infrastructure and necessary software installation, set up and maintenance. This role can be done by the PI if having the necessary skills.

Other people working in the course can be added to the CSC's project but it is not necessary.

See [registering as CSC's customer](https://research.csc.fi/accounts-and-projects).

### Creating a new cPouta project
This is a necessary step for every course. You need to:
1- Create a new CSC project, see [Opening a new CSC Project](https://research.csc.fi/accounts-and-projects). The course's responsible person acts is the PI who requests the project.  You can add project member's (for ex the IT person) when creating the project. You should get an email confirming the project's creation in short time (within minutes). If you cannot find it, look in your spam folder and contact servicedesk@csc.fi.

2- Request cPouta service to your project, see [Adding computing services](https://research.csc.fi/accounts-and-projects). By default, new projects are created without any service so you need to request cPouta to be added via the SUI interface. You should also get an email confirming that the service is active.

Once you have a project with cPouta service activated you can log in at: https:://pouta.csc.fi

You can get started (specially the IT person, but it is good that the PI has some understanding of the platform) with the Pouta environment by following the [cPouta user guide](https://research.csc.fi/pouta-user-guide).


## Simple cPouta course environment setup
The basic structure of a cPouta course environment has two main components:
- the cPouta environment: a virtual machine (VM), often called instance, which has a specific OS and its network configuration (especially the firewall rules). Note that some of the access and network configuration must be also configured in the software installed to the VM (e.g. PostgreSQL database firewall rules).
- the software and setup that is necessary for the course. This is installed to the VM created in previous step. * 

Seting up the cPouta environment is a quite general step requiring some IT expertise, for guidance see the [cPouta user guide](https://research.csc.fi/pouta-user-guide). Some specific settings (e.g. what ports need to be open) depend on the software and the course requirements.

Setting up the software necessary for a course needs to be specified by the course's responsible person. It is possible that such instructions are ready for some specific cases, to see CSC's GIS related use cases go to the [CSC's training git-hub](https://github.com/csc-training/geocomputing/tree/master/pouta) pages.
As an example, you can follow the instructions on [how to set up a single VM GeoServer course environment](https://github.com/csc-training/geocomputing/tree/master/pouta/geoserver).

Please, contact servicedesk@csc.fi if you have any questions.

(*) Note that the software installation could be also packed as containers (e.g. Dockers), in that case several "course software environments" (containers) would likely be running inside a VM... making for a somewhat more complex use case.
