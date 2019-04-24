## Getting started with cPouta Command Line Interface (OpenStack)

Before you can use the Command Line Interface (CLI) tools, you need to get them installed. For this you will need a Linux environment.

Below is an example installation of the necessary tools in an Linux Ubuntu 16.04 machine. If you don't have a linux based computer, you can install one using for ex. VirtualBox or you could create a virtual machine in cPouta.

Note that using the CLI tools to manage cPouta projects does not require many resources, so in case that you are creating a virtual machine for this purpose (locally with VirtualBox or in cPouta), you will be fine with a small amount of resources allocated.

In the examples below a cPouta VM with 1 CPU and 1GB of RAM created from an Ubuntu 16.04 image is used. Of course, if you have a local Linux machine, you can use it as well (consider installing in a separate python environment).

Steps to get your CLI environment up and running:
- [Install openstack tools](#Install-openstack-tools)
- [Get your project API credentials](#Get-your-project-API-credentials)
- [Using CLI after installation](#Using-CLI-after-installation)

### Install openstack tools
If you have a Linux or MacOS computer you can simply use virtual environments as mentioned in [Pouta Command Line tools](https://research.csc.fi/pouta-install-client).

Once you have your machine (or virtual environment) ready, install **python-openstack** tools as indicated in [Pouta Command Line tools](https://research.csc.fi/pouta-install-client).

**Note** that in the isntructions above, if you are using a virtual python environment, you should do the python installations **without** `sudo`! (Otherwise you will get some installation errors).

You should now have an environment with the necessary **openstack** tools installed and ready to manage your Pouta projects.

## Get your project API credentials
To login and manage a cPouta project from the command line, you need to use your project's **API credentials**. You can **download them from the cPouta web interface**. Note that you will need to load these credential everytime you want to use the openstack tools.

Follow the instructions **3.4.1.3 Configure your terminal environment for OpenStack** at the end of [Pouta Command Line tools](https://research.csc.fi/pouta-install-client). If you are working on a cPouta VM, you can download the credentials to your computer and then transfer the file to the cPouta VM, where you load the environment variables.

**Note** that there are tow versions of the API file (v2.0 and v3). For recent projects, you should used the **v3** version.

Activate your credentials (with your password) by running the API file:
```
source <your-project-api-file>.sh
```

Test that you are connected to your project and the CLI tools work by for example listing all images available in your project:
```
# get a list of the images available in your cPouta project.
openstack image list
```

If you get an authentication error, it is possible that you did not entered your password correctly. Try to run your API file again.

## Using CLI after installation
After you have installed your *openstack* tools, whenever you want to use them to manage a project, login to your project by running the API file::
```
source <your-project-api-file>.sh
```

If you installed your tools in a python environment, load the CLI tools environment first with:
```
cd python_virtualenvs
source osclient/bin/activate
```

You can learn some basic commands from https://research.csc.fi/pouta-client-usage.
