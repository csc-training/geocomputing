# Using cPouta from command line
Make sure you have the correct tools installed and your API credentials are loaded (see [Getting started with cPouta Command Line Interface](cli_getting_started.md))

### Basic tools
For every topic to be managed in cPouta, there is a specific `openstack` tool.

```shell
# to get a list of images in your project
openstack image list

# to get a list of VMs in your project
openstack server list

# to get a list of keypairs in your project
openstack keypair list

# to get a list of VM flavors in your project
openstack flavor list

# to get a list of floating ips in your project
openstack floating ip list

# to get a list of security groups in your project
openstack security group list

# to get a list of volumes in your project
openstack volume list
```

To see the available commands for every tool use the `openstack help <tool_name>`. For example:
```shell
# a list of commands for the server tool
openstack help server
```

### Some basic operations

Get information about an existing cPouta image:
```shell
# list images
openstack image list
# show image for "Ubuntu-16.04" image
openstack image show Ubuntu-16.04
# in this case the image in cPouta was in format QCOW2
```

Download a cPouta image to your machine
```shell
# Downloading an image from openstack
openstack image save --file ~/Downloads/Ubuntu-16.04.qcow2 Ubuntu-16.04
# when downloading an image, check the format of the file in cPouta or with "openstack image show" command
```

### Managing VMs (servers)
When working in with openstack, you can access existing VM's information or manage them with the **server** tools:
```shell
# A list of existing VMs
openstack server list
```

To create a VM (server):
```shell
openstack server create --flavor <cpouta_flavor_name> --image <image_name> --security-group default --security-group 'your own security group' --key-name <your_keypair> <name_of_vm>
```
