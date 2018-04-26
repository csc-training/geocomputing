
##Installing ArcGIS for server in a cPouta instance

# This is a guideline for setting up a single CentOS 7.o instance running ArcGIS for Server Enterprise

#You will need an ArcGIS Linux installation package and licence that you can get from ESRI (or ask CSC personnel for a university license).

##Set up your cPouta instance

# In pouta.csc.fi open Access & Security and create a security group that has a rule allowing SSH.
# If you want to use your ArcGIS server with a ArcMap Desktop client you need to add rules to allow
# ingress and egress for the following TCP ports:
# 4000-4003, 6080(HTTP), 6443(HTTPS)
# Some references about arcgis server ports:
# - http://server.arcgis.com/en/server/latest/install/linux/arcgis-server-system-requirements.htm
# - http://server.arcgis.com/en/server/latest/install/linux/ports-used-by-arcgis-server.htm

# In pouta.csc.fi Access & Security, create a key pair and download the private key on your computer.
#
# Launch the instance in pouta.csc.fi with the flavor you need and set the boot source to CentOS-7.
# Set the instance's keypair and security groups properly.
#
# In pouta.csc.fi, associate a Floating IP for the instance and establish a SSH connection with a
# SSH client. The username is cloud-user. Use the private key of the keypair you chose for
# authentication.
#
# Now you should be in your instance.

#####
## Prepare the installation
#####
#The following command installs all the dependencies
sudo yum install fontconfig mesa-libGL mesa-libGLU libXtst libXext libX11 libXi libXdmcp libXrender libXau xorg-x11-server-Xvfb libXfont -y

# Get the ArcGIS installation package and unpack it.
# For example if you have the file in Taito you can a command like this from the cPouta instance terminal:
scp username@taito-shell.csc.fi:/homeappl/home/username/ArcGIS_for_Server_Linux_xxxx_xxxxxx.tar.gz ~/

# You need to authorize your installation with a .prvc or .ecp file.
# "provision" a file from my.esri.com and save it somewhere on the virtual instance.
# The provision file is quite short so you can simply copy & paste it with a text editor or
# send it to the instance using echo PROVISIONFILECONTENTS > ~/_Server.prvc or whatever you
# feel is the most straightforward way.

# Unpack the ArcGIS installation package:

tar xvzf ArcGIS_for_Server_Linux_xxxx_xxxxxx.tar.gz

# ArcGIS for Server requires you to increase the maximum number of open files.
# Ref: http://server.arcgis.com/en/server/10.4/install/linux/arcgis-for-server-system-requirements.htm
# You can do that with:
echo cloud-user - nofile 65535 | sudo tee -a /etc/security/limits.conf
echo cloud-user - nproc 25059  | sudo tee -a /etc/security/limits.conf

# Log in & log out for the changes to the limits to take effect.

#####
## Install ArcGIS for server
#####

# Now we are ready to actually install

cd ArcGISServer /
./Setup -m silent -l Yes -a /home/cloud-user/provision_file_ArcGIS_Server.prvc

# The installation will take some minutes.

# If you need only Python and arcpy you don't need to start the server.
# Note that you have to use ArcGIS' own Python installation instead of the
# default system installation. Python on ArcGIS Server for Linux runs
# a Windows version of Python under Wine.

# You start the ArcGIS Python console with:
/home/cloud-user/arcgis/server/tools/python

#####
## Test installation with a simple ArcPy script
#####
# The test_data folder includes a test elevation file dem.tif and a simple
# script that makes loads some arcpy libraries and uses the FlowDirection
# function (see http://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/flow-direction.htm).
# The result is store to the ./test_data/output/ directory
#
# Move the test_data folder to the ArcGIS Server instance
# and run my_arcpy_script.py from there with:
/home/cloud-user/arcgis/server/tools/python my_arcpy_script.py

# You are done!
