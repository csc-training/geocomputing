# Ansible preparations
Setting up a working Ansible environment may not be trivial, especially if you are not an experienced Linux user.

Below you will find some information and hint on how to preapre a working environment for Ansible.

## cPouta account
These are the minimum requirements before you can start using example Ansible playbooks:

- You need to have set up a pouta project with key-pairs and security groups to make connecting from your local machine possible. Instructions: https://research.csc.fi/pouta-getting-started

- You will need to download and source your cPouta project's API access file (see section 3.4.1.3 in [Configure your terminal environment for OpenStack](https://research.csc.fi/pouta-install-client)).

## Ansible tools

You need to have an environment with the necessary tools to run an ansible script (python, openstack-client, ansible and shade). Instructions how to install these: https://research.csc.fi/pouta-install-client.


## Setting up automatic access to keypairs and servers

In order for the ansible scripts to run smoothly, you will need to make sure that
the processes don't need interaction from the user and that the necessary keypairs
are readly loaded.

Some hints that may help:
- make sure that the key pair Ansible is using to contact the remote server is
available. For example with:
````bash
eval $(ssh-agent -s)
ssh-add ~/.ssh/your_private_key.pem
# this private key is the one corresponding to the key pair name specified in
# the Ansible script.
````
- to avoid the servers' fingerprint interactive check:
````bash
export ANSIBLE_HOST_KEY_CHECKING=False
````
