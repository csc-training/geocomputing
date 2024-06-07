# Ansible Docker installations of GeoServer, OpenDroneMap, and PostGIS on Pouta

A collection of Ansible playbooks to set up a virtual machine on Pouta and install geocomputing software.

Please include the ansible.cfg file for the playbooks to work as intended.

## Requirements

In order to run this code you need to first install some tools into your computer. Make sure you have Python(>= 3.6) installed.

1. First, you need Ansible to be installed. There are several methods to install Ansible, one of them being pip:
   
   ```bash
   pip install ansible
   ```
2. You need to add the [openstack.cloud collection](https://docs.ansible.com/ansible/latest/collections/openstack/cloud/index.html) for Ansible:
   
   ```bash
   ansible-galaxy collection install openstack.cloud
   ```
3. You need to install the [openstacksdk for Python](https://pypi.org/project/openstacksdk/):
   
   ```bash
   pip install openstacksdk
   ```
4. Lastly, you need the OpenRC file corresponding to the CSC Project. This can be downloaded from [API access](https://pouta.csc.fi/dashboard/project/api_access/) page from CSC Pouta. More information on [Pouta access through OpenStack APIs](https://docs.csc.fi/cloud/pouta/api-access/)

## Variables

Changing the variables used for creating the virtual machine and security group rules can to be done with [the variable file](group_vars/all.yml) in the group_vars folder.

## Running the playbooks

Before running the playbooks, you need to source the OpenRC file:

   ```bash
   source <project_name>-openrc.sh
   ```

Running the playbook:

   ```bash
   ansible-playbook install-geoserver.yml
   ansible-playbook install-odm.yml
   ansible-playbook install-postgis.yml
   ```

## The playbooks' workflow

1. Create the virtual machine
2. Install Docker on the virtual machine
3. Install the selected software on the virtual machine using Docker containers
