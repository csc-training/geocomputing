# Installation of geospatial tools to cPouta

Instructions here show how to install geospatial software to [cPouta](https://docs.csc.fi/cloud/pouta/), which is CSC public cloud service. 

Included installation examples are for following widely used open source tools:
* [GeoServer](https://geoserver.org/) - for providing OGC APIs, often running as a back-end of different web map appliations.
* [PostGIS](https://postgis.net/) - database solution for spatial data.
* [OpenDroneMap](https://www.opendronemap.org/) - for creating mosaics from drone images.

All tools are installed using [Docker containers](https://www.docker.com/). The used Docker containers are provided by the each project themselves. Installing other tools with Docker would have mainly similar steps.

Technically the examples use [Ansible scripts](https://www.ansible.com/) for creating the virtual machine to cPouta and installing the geospatial tools. These scripts are suitable for setting up the new virtual machine from Linux, Mac and Windows Subsystem for Linux, **they will not work on Windows.**

## Preparations for intallation

### cPouta usage rights
First, make sure you have CSC user account with a project with cPouta access enabled. More info about [CSC user accounts](https://docs.csc.fi/accounts/).

### Local installations
In order to run the Ansible scripts, you need to have Python with Ansible and [OpenstackSDK for Python](https://pypi.org/project/openstacksdk/) installed to your laptop or PC. 

1. Make sure you have Python(>= 3.6) and git installed.
1. Then, add Ansible and OpenStackSDK with pip:
   
   ```bash
   pip install ansible openstacksdk
   ```
2. You need to add the [openstack.cloud collection](https://docs.ansible.com/ansible/latest/collections/openstack/cloud/index.html) for Ansible:
   
   ```bash
   ansible-galaxy collection install openstack.cloud
   ```

### Required files 

Download to your local laptop/PC:
1. The OpenRC file of your CSC Project from [cPouta API access page](https://pouta.csc.fi/dashboard/project/api_access/). More information on [Pouta access through OpenStack APIs](https://docs.csc.fi/cloud/pouta/api-access/)

2. The Ansible scripts from [this Github repository](https://github.com/csc-training/geocomputing?tab=readme-ov-file#download). The included `ansible.cfg` file is needed for the playbooks to work as intended.

## Changing default settings

Changing the variables used for creating the virtual machine and security group rules can to be done with [the variable file](group_vars/all.yml) in the group_vars folder.

## The installation

In principle, all tools have the same general workflow of installation:
1. Create the virtual machine
2. Install Docker to the virtual machine
3. Install the selected software using Docker containers

Before running the playbooks, you need to source the OpenRC file:he 

```bash
source <project_name>-openrc.sh
```

Running the playbooks:

```bash
ansible-playbook install-geoserver.yml
ansible-playbook install-odm.yml
ansible-playbook install-postgis.yml
```


