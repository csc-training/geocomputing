> [!NOTE]  
> The instructions here are from 2018 and **are partly outdated**. Partly they still could be still useful. After 2018t ESRI has realeased [ArcPy also as conda package](https://enterprise.arcgis.com/en/server/latest/develop/linux/linux-python.htm). Using the conda installation is likely easier, but installing the ArcGIS Server is still also needed to get the license.
> If possible, **consider using opensource Python libraries instead**, see for example [Puhti geoconda](https://docs.csc.fi/apps/geoconda/) libraries.

# Setting up and using ArcPy in cPouta
If you need to run [ArcPy scripts](http://desktop.arcgis.com/en/arcmap/latest/analyze/arcpy/what-is-arcpy-.htm) in CSC's cPouta environment, the following instructions will help you set up a remote virtual machine with the necessary software.

On a Windows PC/laptop ArcPy is usually installed as part of ArcGIS Pro or ArcGIS desktop. In cPouta, virtual machines have Linux operating systems. ArcGIS Pro and Desktop do not have a Linux version, but ArcPy can be installed as part of ArcGIS Server. 

Please notice:

* ArcGIS is a **licensed software**. You must have an ArcGIS Server license provisioning file and the corresponding installation package. Universities with ArcGIS campus license (inc. ArcGIS Server licenses) are listed [here](https://docs.csc.fi/apps/arcgis/).

## Prerequisites
In order to follow these instructions you will need to have a cPouta account and a project. You should also have some basic skills in managing cPouta, see the [Pouta User Guide](https://docs.csc.fi/cloud/pouta/).


## Manual installation
These instructions explain the necessary steps to create a cPouta virtual machine with an ArcGIS Server installation and how to test it with a simple ArcPy script.

The [`ArcGIS_Server_manual_installation.sh`](ArcGIS_Server_manual_installation.sh) script includes minimum settings to install ArcGIS Server to an existing CentOS virtual machine in cPouta.

Modify the script to your own use case as necessary.

Create a virtual machine in cPouta, log into it and run the script.


## Automating ArcPy computation using Ansible playbooks
### Prerequisites
**Important**: Using Ansible scripts is an advanced topic where skills in system adminstration and remote connections are required. In addition you should understand the Ansible language itself.

The first thing you need is to make sure that you have the necessary tools and settings to work with Ansible. Review the information about [how to set up your terminal environment to work with Ansible scripts](ansible_preparations.md).

Before running the Ansible playbooks, you will need to make some adjustments to the ansible scripts such as names for keypairs and security groups corresponding to your cPouta project. See comments in the scripts.

To run Ansible playbooks:
````bash
ansible-playbook ansible-playbook.yml
````

### The ArcPy Ansible playbooks
These scripts demonstrate the use of Ansible playbooks to automate the management of virtual machines in cPouta, in this case to install an ArcGIS Server machine and reuse it to run ArcPy scripts.

The following two Ansible playbooks repeat many of the steps shown in the manual installation above. The main difference being that these scripts are meant to be used in a fully automatic way so that the virtual machine is only running while some operation is being executed.

The process is split in two scripts:

1. [`ansible_install_arcpy.yml`](ansible_install_arcpy.yml) creates a volume from an existing image with CentOS operating system and installs ArcGIS Server to it. The cPouta virtual machine is created using a permanent volume which allows to destroy the virtual machine and recreate it whenever needed again.

2. [`ansible_run_arcpy.yml`](ansible_run_arcpy.yml) boots a new virtual machine from the volume created with the first script and runs an ArcPy script on it. Afterwards the machine gets deleted but volume is stored for further use. Note that the results of the example ArcPy script are stored to that volume and to access it you would need to edit this ansible script so that the virtual machine does not get deleted (see comments in the script) or you could send the results to an existig NFS disk.
