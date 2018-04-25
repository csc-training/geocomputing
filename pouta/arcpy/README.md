# Setting up and using ArcPy in cPouta

## Manual installation
The .sh script includes minimum settings to install ArcGIS Server to an existing Ubuntu virtual machine in cPouta.

Modify the script to your own use case as necessary.

Create a virtual machine in cPouta, log in to it and run the script.

## Automating ArcPy computation using Ansible playbooks
These scripts demonstrate the use of Ansible playbooks to automate the management of virtual machines in cPouta and how to remotely run processes in server machines.

Using Ansible scripts is an advanced topic where skills in system adminstration and remote connections are required. In addition you should understand the Ansible language itself.


There are two Ansible playbooks in this example:

1. Creates a volume and installs operating system and ArcGIS Server to it

2. Boots a new machine from volume created in step 1 and runs an arcpy script on it. Afterwards the machine gets deleted but volume is stored for further use.

Before running the playbooks you need to have following things in order:

1. You need to have access to linux machine on which you have installed python, openstack-client, ansible and shade. Instructions how to install these: https://research.csc.fi/pouta-install-client

2. You need to have set up a pouta project with key-pairs and security groups to make connecting from your local machine possible. Instructions: https://research.csc.fi/pouta-getting-started

3. You need to have sourced the OpenStack RC file during your current  (section 3.4.1.3 Configure your terminal environment for OpenStack in https://research.csc.fi/pouta-install-client)

4. To install ArcGISServer you will need a provisioning file. Contact your University's contact person or giscoord@csc.fi

5. You will need to make some adjustments to playbooks such as names for keys and security groups you created and name of the arcpy script you want to run.

Running playbooks:
ansible-playbook paybook.yml
