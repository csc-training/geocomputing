## Setting up a virtual machine in cPouta

When you set up a new virtual machine, you are creating a new "cloud computer" with a specific hardware (Pouta flavors) and an operating system (provided by an image you select).

The end result is something similar to what your own desktop computer is, just it is running in the cloud and usually does not have a graphical user interface (but you can install one if needed, see [how to set a remote desktop in cPouta](../ubuntu-remote-desktop/README.md)).

**List of steps**
- [Log in to the Pouta web interface](#log-in-to-the-pouta-web-interface)
- [Set up basic access components](#set-up-basic-access-components)
- [Create a virtual machine](#create-a-virtual-machine)
- [Connect to your virtual machine](#connect-to-your-virtual-machine)

## Log in to the Pouta web interface

Although there are other ways to manage your Pouta project (command line, Ansible…) you will use the Pouta web interface for this exercise.

- Open a web browser and go to [**http://pouta.csc.fi**](http://pouta.csc.fi)
- Log in with your course account

## Set up basic access components

Since cloud virtual machines are available via the internet, one very important difference to using a desktop machine is that you must configure different access and security rules.

Before you start creating virtual machines, you need to create these security components:

- a **key pair** , which plays the role of a password. Note that you can reuse this key pair for any virtual machine you create.
- a **security group** , which is a set of rules to specify what communication is allowed from which specific IP addresses (as opposed to allowing anyone in the world to attempt breaking into your virtual machine).

**Create a key pair**

In **Access & Security > Key Pairs** , click on **Create Key Pair**

- Name it, for example: **lastname_firstname_key**
- save the key pair file to your local computer

You need to make a few modifications to the key pair to work with it. Follow the instructions below according to your operating system.

In **Windows** machines , you will use Putty to connect to your virtual machines. Because the key pair created in Pouta is in Linux format, to use your key in Windows you need to convert it first.

Use **Puttygen** tools to convert your key (if not installed in your computer,  download Putty tools from: [https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)):
- go to **File > Load private key** , and load your *lastname_firstname_key.pem* key (note that you have to select **All Files (\*.\*)** in the file browse window to see it)
- Add a **Key passphrase**
- click on **Save private key** , save as, for example *lastname_firstname_key.ppk*

In **Linux** or **Mac OS X**, setup your key pair as follows:
```bash
# Create .ssh directory in ~ (the users home directory) if it is not there already.
mkdir -p  ~/.ssh
chmod 600 ~/.ssh

# Move the key into .ssh directory and make it read-write only
mv ~/Downloads/lastname_firstname_key.pem ~/.ssh
chmod 600 ~/.ssh/lastname_firstname_key.pem

# Add a password to it (recommended).
ssh-keygen -p -f ~/.ssh/lastname_firstname_key.pem
```

**Create a security group**

In cPouta web interface **Access & Security > Security Groups** :

- Click on **Create Security Group**.
- Name it: *lastname_firstname_SSH*
- Click on **Create Security Group**

You will add security to your future virtual machines by setting your current IP address as the only one allowed to connect to them. This actually means that nobody else will be able to even try to connect to it.

- First, **find out your local computer's IP address** by, for example, opening a **new web browser window** and going to [http://v4.ident.me](http://v4.ident.me), the IP address being shown is the one you will add to your security group.

Now you can modify your security group to accept connections only from your current local computer's IP address:

Go back to the **Pouta web interface** and:
- Find the security group you created previously and click on **Manage Rules** on its right
- Add a new rule with **Add Rule** , then select **SSH** from the **Rule** drop down
- Leave **Remote** as **CIDR**
- In the **CIDR** field, you should change the default value (193.87.45.14/32) to the IP address you got above (from http://v4.ident.me)

**Note that you don't need to redo these steps for every virtual machine you create. You can reuse these key pair and security group for all your virtual machines in your project!**

## Create a virtual machine

To create a new virtual image, you will use an *Ubuntu 16.04* image (from the existing Pouta images) and the access settings you just created.

Go to the **Images** page in the cPouta web interface:
- Find the image named **Ubuntu-16.04** and click on **Launch**
- In **Source** , make sure that **Create New Volume** is set to **No**
- In **Details > Instance Name** : *lastname_firstname_vm*
- In **Flavor** , select *standard.tiny*
- In **Security Groups** and **Key Pair** , select the ones you just created
- You can leave the rest as defaults and click on **Launch Instance**

Your instance should be visible in the **Instances** view, wait until it has started. You can check its details by clicking on the name of the instance.

## Connect to your virtual machine
A brand new virtual machine is automatically given a local IP address but to be able to connect to your new instance you need to **assign it a public IP address.**

Go to the **Instances** view and:
- Find your VM's name and from the drop down on the right, select **Associate Floating IP**.
- **Select an IP** from the drop down (if there are not available IPs, click on the **"+"** sign).
- You can see the IP you assigned to your VM in the **Instances** page, next to the name of your virtual machine.
- To connect to the instance, you will use this **public-IP** address(floating IP) you just assigned.


**Important note to log in to VMs created from CSC images:**
- the CSC images have only one user by default **cloud-user**. This user has no password so the only way to connect to this virtual machine is via SSH and using this user.
- except for VM's created from Ubuntu 18.04 image in which case the default user is **ubuntu**.


**FROM WINDOWS**, use **Putty** to connect to your VM:
- Open **Putty** and add the **public-ip** you assigned to your VM as the **Host Name (or IP address)**
- Go to **Connection > SSH > Auth** then in **Private key file for authentication** add your key pair file in ppk format (*lastname_firstname_key.ppk*)
- You can also connect to your instance with **WinSCP** for transferring files (use the same settings as in Putty)

**FROM LINUX** or **MacOS**, use ssh commands to connect to your VM:
```
# use these commands to add your key to your keys archive
ssh-agent /bin/bash
ssh-add lastname_firstname_key.pem
ssh -A cloud-user@<public-ip>
```
You can notice that the terminal in your very own virtual machine is very similar to what you have seen when using Taito, which is also a Linux based machine.

Remember that you are the administrator of your own virtual machines and as such: 1) you have full control (and responsibilities) to install and maintain the software; 2) you have the responsibility to configure security and firewalls for connections from the internet to you VM to your hosted services (http, databases, map servers…).
