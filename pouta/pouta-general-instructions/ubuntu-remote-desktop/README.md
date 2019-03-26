# Create a remote Ubuntu desktop machine in cPouta

This is an example for a basic setup of a remote desktop virtual machine (VM) from an Ubuntu 16.04 server in cPouta.

This document is based on Henrikki Tenkkane's work for **Automating GIS processes** and **Introduction to Quantitative Geology** -courses.

Some other reference documentation used:
- https://www.linode.com/docs/applications/remote-desktop/install-vnc-on-ubuntu-16-04 https://help.ubuntu.com/community/VNC/Servers
- https://peteris.rocks/blog/remote-desktop-and-vnc-on-ubuntu-server/

**Description**

The installation script will set up a TightVNC and an xRDP servers. The connection to the RDP server is done via the VNC server so you will need set up (and use) one single password (edit the password in the script before installing).

The connection ports are 5901 for the VNC server and 3389 for the xRDP server. The installed desktop is Gnome with copy/paste functionality. Firefox, Chrome and gedit tools are installed too.

The user name used for the setup is **cloud-user** (this user must exist in the VM).

**Prerequisites**

You need to have:
- access to a cPouta project
- and an existing Ubuntu 16.04 VM running in cPouta
- a public ip linked to your VM
- the keypair to connect via SSH to that server machine
- a correct setup of the cPouta security groups to access the VM to ports 22 (for SSH), 5901 (for VNC) and 3389 (for XRDP).

See [CSC's Pouta documentation](https://research.csc.fi/pouta-user-guide) if needed.

## Installation

The installation steps are included in the `ubuntu-remote-desktop\cPouta-ubuntu-remote-desktop.sh` bash script. Read it carefully and modify at least the password set for the remote connections. Edit other content to match your needs if necessary.

Steps:
- connect as **cloud-user** to your VM via SSH
- move the script to your VM (for ex. using WinSCP)
- run the modified script with:
```bash
sudo sh ubuntu-remote-desktop\cPouta-ubuntu-remote-desktop.sh
```

## Test the remote connection
You can connect to the VM using whether a VNC or a RDP client tool.

*VNC connection*
The VNC server connection should be available at port 5901. Use your VNC client (for ex. TightVNC) to connect to:

`<vm-public-ip>:5901`

You will be asked for the password you set previously.

*Windows Remote Desktop Connection client (RDP)*
In Windows you can use the default RDP client (Windows Remote Desktop Connection) to connect to port 3389 at (replace the `xxx` values with the IP address your cPouta VM has been assigned):

`<vm-public-ip>:3389`

After connecting you will be asked for password you set previously (same as for the VNC connection).

## Known issues
Copy/paste works in both directions well when you use a VNC client tool (for ex. TightVNC) but using Windows Remote Desktop Connection tool works only in direction VM to Desktop.
