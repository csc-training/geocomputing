# GeoServer with (OpenStack tools) and Ansible

For easily repeatable set up of GeoServer OpenStack commandline tools and Ansible can be used. 
OpenStack tools are used for setting up cPouta virtual machine and Ansible for installing GeoServer.
Ansible provides automated way to install any software. These steps enable installing GeoServer installation with Ansible.


## Set up cPouta machine

You can either use the [cPouta web interface](https://docs.csc.fi/cloud/pouta/launch-vm-from-web-gui/) OR [OpenStack tools](https://docs.csc.fi/cloud/pouta/command-line-tools/). 

The virtual machine could be with:
   * For example standard.medium flavour and Centos7 image. 
   * Public IP
   * Security group settings with access from your local computer port 22 for SSH and public access to 80 and 8080 ports.
 
OpenStact tools commands for setting up the virtual machine:

```
# Set up openstack tool with your project
source project_2000XXXX-openrc.sh
# Create VM
openstack server create --flavor standard.medium --image CentOS-7 --key-name <key_name> <server_name>

# Add public IP
openstack floating ip create public
openstack server add floating ip <server_name> <public_ip_created_in_with_previous_command>

# Set up security group
openstack security group create <security_group_name>
openstack security group rule create --proto tcp --remote-ip xxx.xxx.xxx.x/24 --dst-port 22 <security_group_name> #local IP, SSH
openstack security group rule create --proto tcp --remote-ip 0.0.0.0/0 --dst-port 8080 <security_group_name> #Public
openstack security group rule create --proto tcp --remote-ip 0.0.0.0/0 --dst-port 80 <security_group_name> #Public
openstack server add security group <server_name> <security_group_name>
```

## Install GeoServer with Ansible 
* [Install Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) to your local computer. 
* Create Ansible hosts file to your local computer.

```
[geoserver]
geoserver ansible_host=<PUBLIC-IP> ansible_user=cloud-user ansible_ssh_private_key_file=
```
  
* Copy the example scripts from [ansible](https://github.com/csc-training/geocomputing/tree/master/pouta/geoserver/ansible) folder to the local computer.
* Run the Ansible play-book on local computer.  

```
ansible-playbook -i hosts -l geoserver geoserver.yml --extra-vars "ansible_ssh_private_key_file=<key_name>"
```

### Ansible cPouta webinars:
* [Creating a virtual machine in cPouta](https://www.youtube.com/watch?v=CIO8KRbgDoI)
* [First steps into automating cPouta deployments with Ansible](https://www.youtube.com/watch?v=Qvd0-zI4yvw)
