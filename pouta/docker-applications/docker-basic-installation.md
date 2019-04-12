## Installing Docker in a cPouta VM
Docker is a platform for developers and sysadmins to develop, deploy, and run applications with containers.

Containerization is increasingly popular because containers are:
- **Flexible** : Even the most complex applications can be containerized.
- **Lightweight** : Containers leverage and share the host kernel.
- **Interchangeable** : You can deploy updates and upgrades on-the-fly.
- **Portable** : You can build locally, deploy to the cloud, and run anywhere.
- **Scalable** : You can increase and automatically distribute container replicas.
- **Stackable** : You can stack services vertically and on-the-fly.

Installing Docker to an Ubuntu machine (the virtual machine we are using has that operating system) is relatively simple. You would find the best instructions on how to install it from:
- in case you need a cPouta VM, you can see instructions [here](./pouta/pouta-general-instructions)
- the Docker documentation ([https://docs.docker.com/install/linux/docker-ce/ubuntu/](https://docs.docker.com/install/linux/docker-ce/ubuntu/))
- and for example Digital Ocean guides ([https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04)).

For convenience a summary of the commands you need to run for a standard installation to our specific virtual machine follows (if you need some other specific settings, see the official documentation).

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
