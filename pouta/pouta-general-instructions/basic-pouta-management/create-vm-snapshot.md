## Create a VM snapshot in cPouta
In order to back up a VM state (or to s save billing units when a VM is not used) you can create a snapshot from it, so that you can continue use it to start new virtual machines later.

#### Create a snapshot
In the Pouta web interface:

- Shut down your instance: **Compute > Instances >** *instance_name* **> Shut Off Instance**
- Then, **Compute > Instances >** instance\_name **> Create Snapshot**
- Name it: *lastname_firstname_vm_date*
- This creates a new image visible in the **Compute > Image** view in cPouta web interface

A snapshot can be thought of a version of your virtual machine that can be launch later on as an instance (this instance will be the same as that you have in the moment of taking the snapshot). The snapshots are stored in Pouta as **Images**.

#### Reuse your snapshot to create a new VM
To review that the snapshot was created properly:
- Go to **Compute > Images**
- Click on the **name of your image (snapshot)** to see its details

If you want to reuse your snapshot to create a new virtual machine:
- Go to **Compute > Images**
- Find your **image snapshot** and click on **Launch**

#### Some notes about your cPouta snapshots:
- when you create a VM from an image snapshot the key pairs you had added before creating the snapshots are still working
- if you define a new key pair when creating the new VM, this key pair will be also valid
- the public ip, security groups and VM flavor settings must be defined again
