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

### SSH key 
Set up [SSH key pair for cPouta](https://docs.csc.fi/cloud/pouta/launch-vm-from-web-gui/#setting-up-ssh-keys). If you create new key pair, save the private key to your laptop or PC.

### Local installations
In order to run the Ansible scripts, you need to have Python(>= 3.6) with Ansible (>= 4.0)  and [OpenstackSDK for Python](https://pypi.org/project/openstacksdk/) installed to your laptop or PC. 

1. Make sure you have Python and pip installed.
1. Then, add Ansible and OpenStackSDK with pip:
   
   ```bash
   pip install ansible openstacksdk
   ```
2. You need to add the [openstack.cloud](https://docs.ansible.com/ansible/latest/collections/openstack/cloud/index.html) and [docker](https://docs.ansible.com/ansible/latest/collections/community/docker/index.html) collections for Ansible:
   
   ```bash
   ansible-galaxy collection install openstack.cloud
   ansible-galaxy collection install community.docker
   ```
   or
   ```bash
   ansible-galaxy install -r requirements.yml
   ```
   
### Download required files 

Download to your local laptop/PC:
1. The Ansible scripts from [this Github repository](https://github.com/csc-training/geocomputing?tab=readme-ov-file#download). The included `ansible.cfg` file is needed for the playbooks to work as intended.
2. The OpenRC file of your CSC Project from [cPouta API access page](https://pouta.csc.fi/dashboard/project/api_access/). More information on [Pouta access through OpenStack APIs](https://docs.csc.fi/cloud/pouta/api-access/)


#### Define own settings

Some settings must be changed and some others are good to review, before doing the installation.

[group_vars/all.yml variable file](group_vars/all.yml) includes the common variables used for creating the virtual machine and security group rules can to be done with

* `key_name` - Name of your SSH key pair added to cPouta. Must be changed.
* `internal_ips` - To which IPs the admin ports of virtual machine should be open. Please change this to your own, you can use https://apps.csc.fi/myip to check your IP or ask jour local IT-support which IPs to use. Leaving this to default (open to everywhere) is tehcnically possible, but decreases the security of your virtual machine.
* `instance_flavor` - The [cPouta flavour](https://docs.csc.fi/cloud/pouta/vm-flavors-and-billing/#cpouta-flavors) to be used, this will affect your billing, select one suitable for you.

  
## The installation

In principle, all tools have the same general workflow of installation:
1. Create the virtual machine
2. Install Docker to the virtual machine
3. Install the selected software using Docker containers

For each of these steps there is an Ansible role.

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

If do not have the private key in ~/.ssh folder, you can add its path to the commands like this:
```bash
ansible-playbook install-geoserver.yml --extra-vars "ansible_ssh_private_key_file=<path_to_key>/<key_name>.pem"
```
Ansible prints out the steps of the scripts and shows the status.

### Virtual machines
You can check that the virtual machine was created and is running from [cPouta web interface](https://pouta.csc.fi/):
   * The `Instances` page shows main info about the virtual machines
   * The `Floating IPs` page shows the IP address of the virtual machine, that can be used for connecting to it.
   * The `Security groups` page shows the settings for different ports.
     
```
ssh ubuntu@<public_ip> 
# OR if you had custom private key path
ssh ubuntu@<public_ip> -i <path_to_key>/<key_name>.pem
```

# OpenDroneMap

Other options: 
* The basic OpenDroneMap is also available in [Puhti](https://docs.csc.fi/apps/opendronemap/), but OpenDroneMap Web requires cPouta. 
* UEF drone lab has very detailed instructions for OpenDroneMap and OpenDroneMap Web in [GeoPortti](https://www.geoportti.fi/tools/instruments/) (see the end of the page).
