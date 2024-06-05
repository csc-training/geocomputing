# Ansible Docker installations of GeoServer, OpenDroneMap, and PostGIS on Pouta

A collection of Ansible playbooks to set up a virtual machine on Pouta and then install geocomputing software.

## Requirements

In order to run this code you need to first install some tools into your computer.

1. First, you need Ansible to be installed. There are several methods to install Ansible, one of them being pip:
  **  Make sure you have Python (>= 3.6). 
  `pip install ansible`
2. You need the [openstack.cloud collection](https://docs.ansible.com/ansible/latest/collections/openstack/cloud/index.html) for Ansible:
  `ansible-galaxy collection install openstack.cloud`
3. You need the [openstacksdk for Python](https://pypi.org/project/openstacksdk/):
  `pip install openstacksdk`
4. Lastly, you need the OpenRC file corresponding to the CSC Project. This can be downloaded from [API access](https://pouta.csc.fi/dashboard/project/api_access/) page from CSC Pouta. More information on [Pouta access through OpenStack APIs](https://docs.csc.fi/cloud/pouta/api-access/)


Please include the ansible.cfg file for the playbooks to work as intended.
