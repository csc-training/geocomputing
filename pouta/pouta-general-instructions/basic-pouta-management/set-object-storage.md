## Setting up cPouta object storage
Every project in cPouta has a default object storage space of 1Tb. You can access this object storage from the cPouta web interface at the **Object store** view. See the documentation about [cPouta object storage](https://research.csc.fi/pouta-object-storage) for more information.

In order to use your cPouta object storage via its command line API from your VM, you will need to first install some software:

```bash
sudo apt-get update
sudo apt install python-pip python-dev python-setuptools s3cmd git -y
sudo pip install python-openstackclient
#Then you need to download a CSC's provided script that will help you set up your cPouta project's object storage:
wget https://tools.object.pouta.csc.fi/poutaos_configure

chmod u+x poutaos_configure

./poutaos_configure
```
The **poutaos_configure** command asks first for your cPouta user and password.

Then it lists your cPouta projects and asks you to define the name of the cPouta project to be used, copy the project name and paste it to select it.

During the following configuration steps, the system asks you about the values that will be used for the Pouta Object Storage connection. In most cases you can just accept the proposed default values, but there are two exceptions:
1. It is recommended that you define a password that is used to encrypt the data traffic to and from Object Storage server.
2. As the last question the configuration process asks if the configuration is saved. The default is **no** but you should answer **y (yes)** so that configuration information is stored to file **$HOME/.s3cfg**.

This configuration needs to be defined only once. In the future s3cmd will use this Object Storage connection described in the .s3cfg file automatically.

After this you can use the Object Storage area of your cPouta Project with s3cmd command.
```bash
# List the buckets in your cPouta project with:
s3cmd ls

# List the contents of the bucket odm-datasets with:
s3cmd ls s3://odm-datasets

# Check the contents of the pseudo-folder s3://odm-datasets/odm_data_aukerman/
s3cmd ls s3://odm-datasets/odm_data_aukerman/
```
You can find more detailed instructions on how to set-up access to your project's object storage from your virtual machine from the CSC's research pages at: [https://research.csc.fi/-/how-can-i-mount-my-pouta-object-storage-bucket-to-an-ubuntu-vm-running-in-cpouta](https://research.csc.fi/-/how-can-i-mount-my-pouta-object-storage-bucket-to-an-ubuntu-vm-running-in-cpouta)

Now you can get the OpenDroneMap example dataset from object store to your VM. Use the **s3cmd sync** command:
```bash
s3cmd sync s3://odm-datasets/odm_data_aukerman /home/cloud-user
# check the contents of your local folder
ls odm_data_aukerman/images
```
(This dataset was copied from [https://github.com/OpenDroneMap/odm\_data\_aukerman](https://github.com/OpenDroneMap/odm_data_aukerman) )
