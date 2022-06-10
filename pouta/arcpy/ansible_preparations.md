# Ansible preparations
Setting up a working Ansible environment may not be trivial, especially if you are not an experienced Linux user.

Below you will find some information and hints on how to preapre a working environment for Ansible.

## cPouta account
These are the minimum requirements before you can start using example Ansible playbooks:

- A pouta project with key-pairs and security groups to make connecting from your local machine possible. Instructions: https://docs.csc.fi/cloud/pouta/launch-vm-from-web-gui/

- cPouta project's API access file, see [Configure your terminal environment for OpenStack](https://docs.csc.fi/cloud/pouta/install-client/#configure-your-terminal-environment-for-openstack)

## Computer environment

It is recommended to use a computer with a Linux operating system. Most of the instructions you will find here assume that you are working with a Linux computer. Note, that you can create a Linux virtual machine in cPouta and install the necessary tools and settings into it as necessary OR use Windows Linux Subsystem.

### Ansible tools

You need to have an environment with the necessary tools to run an ansible script: python, [openstack-client](https://docs.csc.fi/cloud/pouta/install-client), ansible and shade. 


### Setting up automatic access to keypairs and servers

In order for the ansible scripts to run smoothly, you will need to make sure that
the processes don't need interaction from the user and that the necessary keypairs
are loaded.

Some hints that may help:
- make sure that the key pair Ansible is using to contact the remote server is
available. For example with:
````bash
# Start a ssh agent to automatically manage your keypairs
eval $(ssh-agent -s)
# Add your keypair to the ssh agent
ssh-add ~/.ssh/your_private_key.pem
# this private key is the one corresponding to the key pair name specified in
# the Ansible script.
````
- by default, new remote connections have to be confirmed manually, which would interrupt the workflow of an Ansible script. To avoid new servers' fingerprint interactive checks, set the following environment variable:
````bash
export ANSIBLE_HOST_KEY_CHECKING=False
````
