## Installing Docker in a cPouta VM
A good alternative to having docker installed locally is to create a cloud VM to create and manage your docker images creation and containers testing. Docker can easily fill up your machine and creating images can take long times. In a cloud environment both managing disk space and leaving processes to the background can be easily done. Besides, in many cases you will want to test access to the containers via internet rather than locally, which is easily done in a remote VM. Nonetheless, the same instructions could be used to install in your Linux local machine.

The following instructions are meant for a Linux set up. If you want to install your environment in Windows see the [official installation documentation](https://docs.docker.com/docker-for-windows/install/).

Make sure that you have created a virtual machine in Pouta whith the approriate security settings and with docker installation (see the [Pouta general instructions](./pouta/pouta-general-instructions)).

### About Docker
Docker is a platform for developers and sysadmins to develop, deploy, and run applications with containers.

Containerization is increasingly popular because containers are:
- **Flexible** : Even the most complex applications can be containerized.
- **Lightweight** : Containers leverage and share the host kernel.
- **Interchangeable** : You can deploy updates and upgrades on-the-fly.
- **Portable** : You can build locally, deploy to the cloud, and run anywhere.
- **Scalable** : You can increase and automatically distribute container replicas.
- **Stackable** : You can stack services vertically and on-the-fly.

### installation steps
Installing Docker to an Ubuntu machine (the virtual machine we are using has that operating system) is relatively simple. You would find the best instructions on how to install it from:
- in case you need a cPouta VM, you can see instructions [here](./pouta/pouta-general-instructions)
- the Docker documentation ([https://docs.docker.com/install/linux/docker-ce/ubuntu/](https://docs.docker.com/install/linux/docker-ce/ubuntu/))
- and for example Digital Ocean guides ([https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04)).

For convenience a summary of the commands you need to run for a standard installation to our specific virtual machine follows (if you need some other specific settings, see the official Docker documentation).

```
# First, in order to ensure the downloads are valid, add the GPG key for the official Docker repository to your system and add the Docker repository to APT sources:

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb\_release -cs) stable"

# Update the apt package index.

sudo apt-get update

# Install the latest version of Docker CE and containerd, or go to the next step to install a specific version:

sudo apt-get install docker-ce docker-ce-cli containerd.io

# Verify that Docker CE is installed correctly by running the hello-world image.

sudo docker run hello-world
```

### Get docker user to root group
To be able to run docker without `sudo` add your user (cPouta default is cloud-user) to the *docker* group:
```
sudo usermod -aG docker $USER #sudo usermod -aG docker cloud-user
```
Before it takes effect, log out and log back in to your VM.

### Example automated ansible script
**Note** that you need to know Ansible before trying to make use of the script and that you might need to update/customize several parts of it.

This [example Ansible template](./ansible_docker_factory) serves as a template in case you want to automate the creation of the VM descried above.
