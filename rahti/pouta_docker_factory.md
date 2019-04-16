# Setup OpenShift and CSC's Notebooks Images repo
The following instructions can be used to set up an environment to manage CSC's Rahti environment and use CSC's Notebooks Images repository to create your own custom Rahti images for Notebooks

Many things are general to managing docker containers and the rahti platform, so read along for hints.

## Install OpenShift command line tool
Besides the graphical interface to interact with the Rahti's platform, you will neet to offten work with the OpenShift CLI tools from the command line.

Install some basic tools:
```shell
sudo apt -y install python-pip && pip install --upgrade pip && pip install python-swiftclient
sudo apt-get -y install python-setuptools
sudo easy_install pip
sudo pip install python-keystoneclient
```

Install the OpenShift command line tool `oc` (see [OKD download pages](https://www.okd.io/download.html) for newest version):
```shell
wget https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz
tar -xvzf openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz
chmod +x openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc
sudo mv openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc /usr/local/sbin
```

You can check that you can now run `oc` from the comand line.
```shell
oc --help
```

See [`oc` Command Line Tools instructions](https://docs.okd.io/latest/cli_reference/get_started_cli.html) to get started.


## Clone  CSC's Notebooks Images repo
To make sure that your custom Docker images are compatible with CSC's Notebooks and Rahti platforms and work as expected, you should make use of the scripts and templates available in the CSC's Notebooks Images repo.

Clone the [`notebook-images`](https://github.com/CSCfi/notebook-images.git) to your environment:
```
git clone https://github.com/CSCfi/notebook-images.git
```
