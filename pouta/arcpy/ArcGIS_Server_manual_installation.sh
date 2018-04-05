
##Installing ArcGIS for server in a cPouta instance

# This is a guideline for setting up a single CentOS 6.6 instance running ArcGIS for Server Enterprise

#You will need an ArcGIS Linux installation package and licence that you can get from ESRI (or ask CSC personnel for a university license).

##Set up your cPouta instance

# In pouta.csc.fi open Access & Security and create a security group that has a rule allowing SSH.
# If you want to use your ArcGIS server with a ArcMap Desktop client you need to add rules to allow
# ingress and egress for the following TCP ports:
# 4000-4003, 6080(HTTP), 6443(HTTPS)
#
# In pouta.csc.fi Access & Security, create a key pair and download the private key on your computer.
#
# Launch the instance in pouta.csc.fi with the flavor you need and set the boot source to CentOS 6.6.
# Set the key pair and security groups properly.
#
# In pouta.csc.fi, associate a Floating IP for the instance and establish a SSH connection with a
# SSH client. The username is cloud-user. Use the private key of the key pair you chose for
# authentication.
#
# Now you should be in your instance.

## Prepare the installation

#The following command installs all the dependencies

sudo yum install fontconfig mesa-libGL mesa-libGLU libXtst libXext libX11 libXi libXdmcp libXrender libXau xorg-x11-server-Xvfb libXfont -y

# Get the ArcGIS installation package and unpack it.
# For example if you have the file in Taito you can use something like:

scp username@taito-shell.csc.fi:/homeappl/home/username/ArcGIS_for_Server_Linux_1031_145870.tar.gz ~/

# If you use ArcGIS 10.3.1 the checksum should be 96bcced74d2f6cf654819a9048fcb591
md5sum ArcGIS _for_Server_Linux_1031_145870.tar.gz

# You need to authorize your installation with a .prvc or .ecp file.
# "provision" a file from my.esri.com and save it somewhere on the virtual instance.
# The provision file is quite short so you can simply copy & paste it with a text editor or
# send it to the instance using echo PROVISIONFILECONTENTS > ~/_Server.prvc or whatever you
# feel is the most straightforward way.

# Unpack the ArcGIS installation package:

tar xvzf ArcGIS _for_Server_Linux_1031_145870.tar.gz

# ArcGIS for Server requires you to increase the maximum number of open files, you can do this with:
echo cloud-user soft nofile 65535 | sudo tee -a /etc/security/limits.conf
echo cloud-user hard nofile 65535 | sudo tee -a /etc/security/limits.conf
echo cloud-user soft nproc 25059  | sudo tee -a /etc/security/limits.conf
echo cloud-user hard nproc 25059  | sudo tee -a /etc/security/limits.conf

# Log in & log out for the changes to the limits to take effect.

# ArcGIS Server requires a minor addition to the /etc/hosts file, you can do this with:

ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | cut -d ' ' -f1  | xargs -I ip echo 'ip ${fqdn} ${hostname}' | sudo tee -a /etc/cloud/templates/hosts.redhat.tmpl

 

##Install ArcGIS for server

# Now we are ready to actually install

cd ArcGISServer /
./Setup -m silent -l Yes -a /full/path/to/_Server.prvc

# Now you can start the server from /home/cloud-user/arcgis/server/startserver.sh
# If you need only Python and arcpy you don't need to start the server.
# Note that you have to use ArcGIS 's own Python installation instead of the default system
# installation. Python on ArcGIS Server for Linux runs a Windows version of Python under Wine.
# You can find the Python for ArcGIS from /home/cloud-user/arcgis/server/tools/python

/home/cloud-user/arcgis/server/tools/python ~/helloWorld.py

#
# If you want to connect to the server from your ArcMAP Desktop you have to open a few ports.
# You can do this with a bash script:
#
# #!/bin/bash
# iptables -F
# iptables -A INPUT -p tcp --dport 22 -j ACCEPT
# iptables -A INPUT -p tcp --match multiport --dports 6443,6080,4000:4003 -j ACCEPT
# iptables -A INPUT -p udp --match multiport --dports 6443,6080,4000:4003 -j ACCEPT
# iptables -P INPUT DROP
# iptables -P FORWARD DROP
# iptables -P OUTPUT ACCEPT
# iptables -A INPUT -i lo -j ACCEPT
# iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
# /sbin/service iptables save
# iptables -L -v
#

 
# For using ArcGIS Server using ArcMap Desktop as a client, check out http://server.arcgis.com/en/server/latest/publish-services/linux/a-quick-tour-of-publishing-a-geoprocessing-service.htm 
