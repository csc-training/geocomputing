# Docker factory VM creation
A good alternative to having docker installed locally is to create a cloud VM to create and manage your docker images creation and containers testing. Docker can easily fill up your machine and creating images can take long times. In a cloud environment both managing disk space and leaving processes to the background can be easily done. Besides, in many cases you will want to test access to the containers via internet rather than locally, which is easily done in a remote VM.

The following steps will be needed to create a VM than can be used to manage docker images and containers for CSC's Notebooks and Rahti platforms:

1. Manually create a virtual machine in CSC's Pouta whith the approriate security settings and with docker installation. You may use the exampl ansible script which creates vm and installs docker.

2. To create docker images to be used in CSC's Notebooks platform, clone the `notebook-images` repository which includes example dockerfiles and building scripts to create docker images that are compatible with CSC's Notebooks and Rahti platforms.
```
git clone https://github.com/CSCfi/notebook-images.git
```

### Get docker user to root group
To be able to run docker without `sudo`:

```
sudo usermod -aG docker $USER #sudo usermod -aG docker cloud-user
```
Before it takes effect, log out and log back in to your VM.

## OpenStack and OpenShift command line
To eficiently manage your Pouta and Rahti projects from the command line you need to install some tools:
```
sudo apt -y install python-pip && pip install --upgrade pip && pip install python-swiftclient

sudo apt-get -y install python-setuptools
sudo easy_install pip

sudo pip install python-keystoneclient
```
Install the OpenShift command line tool `oc`:

```
wget https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz

tar -xvzf openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz

chmod +x openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc

sudo mv openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc /usr/local/sbin
```
You can check that you can now run ´oc´ from the comand line.
