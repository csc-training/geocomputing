# Installation of geospatial tools to cPouta

Instructions here show how to install geospatial software to [cPouta](https://docs.csc.fi/cloud/pouta/), which is CSC public cloud service. 

Included installation examples are for following widely used open source tools:
* [GeoServer](https://geoserver.org/) - for providing OGC APIs, often running as a back-end of different web map appliations.
* [PostGIS](https://postgis.net/) - database solution for spatial data.
* [OpenDroneMap](https://www.opendronemap.org/) - for creating mosaics from drone images.

All tools are installed using [Docker containers](https://www.docker.com/). The used Docker containers are provided by the each project themselves. Installing other tools with Docker would have mainly similar steps.

Technically the examples use [Ansible scripts](https://www.ansible.com/) for creating the virtual machine to cPouta and installing the geospatial tools. These scripts are suitable for setting up the new virtual machine from Linux, Mac and Windows Subsystem for Linux, **they will not work on native Windows.**

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
* `os_image` - The [base Linux image](https://docs.csc.fi/cloud/pouta/images/), no need to change, but good to be aware.

  
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
   * [More info](https://docs.csc.fi/cloud/pouta/connecting-to-vm/)
     
```
ssh ubuntu@<public_ip> 
# OR if you had custom private key path
ssh ubuntu@<public_ip> -i <path_to_key>/<key_name>.pem
```
## GeoServer
* The script prints out the URL of GeoServer admin page and how to connect to the virtual machine.
* The default username (admin) and password (geoserver) are used, change password from Admin front page.
* If GeoServer is used for courses, do not let students use the main admin credetials, but [create new user account(s)](https://docs.geoserver.org/latest/en/user/security/webadmin/ugr.html#add-user).
* The scripts install the official [GeoServer Docker image](https://docs.geoserver.org/latest/en/user/installation/docker.html). 
* GeoServer version and data directory location are defined in: [install-geoserver.yml](install-geoserver.yml)
* For adding your own data, add it to data directory, which is mounted to Docker and visible for GeoServer.
* Customization:
   * See [GeoServer Docker readme](https://github.com/geoserver/docker/blob/master/README.md) for additional options.
   * The changes should be done to [roles/geoserver/tasks/main.yml](roles/geoserver/tasks/main.yml) `Start GeoServer` task.
   * The example shows how to bind data directory from outside of the Docker and how to install `ysld` extension.

## PostGIS
* The script prints out the IP, port, database and credentials of PostGIS and how to connect to the virtual machine.
* If PostGIS is used for courses, do not let students use the main admin credetials, but [create new user account(s)](https://www.postgresql.org/docs/16/sql-createuser.html).
* The scripts install the community [PostGIS Docker image](https://postgis.net/documentation/getting_started/install_docker/) 
* PostGIS version, host port and credentials are defined in: [install-postgis.yml](install-postgis.yml), change at least the password.
* Customization:
   * See [PostGIS Docker readme](https://hub.docker.com/r/postgis/postgis/) for additional options.
   * The changes should be done to [roles/postgis/tasks/main.yml](roles/postgis/tasks/main.yml) `Start PostGIS` task.

## OpenDroneMap
* The script prints out how to connect to the virtual machine.
* The scripts install the official [OpenDroneMap Docker image](https://hub.docker.com/r/opendronemap/odm) 
* ODM image folder is defined in: [install-odm.yml](install-odm.yml).
* Customization:
   * See [OpenDroneMap Docker readme](https://hub.docker.com/r/opendronemap/odm) for additional options.
   * The changes should be done in the code below.
   * To run OpenDronemap, connect to the virtual machine and move your images to /data/images folder
```
# Move to the data folder
cd /data/

# Use the **screen** command to start a detachable terminal (= you can close the terminal and the process keeps running)
screen –S odm

# Run the opendronemap command (use the **time** command to get info on how long it run):
time sudo docker run -it --rm \
    -v "$(pwd)/images:/code/images" \
    -v "$(pwd)/odm_orthophoto:/code/odm_orthophoto" \
    -v "$(pwd)/odm_georeferencing:/code/odm_georeferencing" \
    opendronemap/opendronemap \
    --mesh-size 100000
```

Other options: 
* The basic OpenDroneMap is also available in [Puhti](https://docs.csc.fi/apps/opendronemap/), but OpenDroneMap Web requires cPouta. 
* UEF drone lab has very detailed instructions for OpenDroneMap and OpenDroneMap Web in [GeoPortti](https://www.geoportti.fi/tools/instruments/) (see the end of the page).

**
Credentials can also be set using Ansible Vault variables https://docs.ansible.com/ansible/latest/vault_guide/index.html
