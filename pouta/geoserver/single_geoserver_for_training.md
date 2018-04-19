# Installation of single GeoServer VM for teaching

Prerequisites to follow installation instructions:
- Virtual machine (VM) with Ubuntu 16.04 (use for ex. CSC's cPouta environment)
- Proper security settings are defined:
  - keypair to access the VM
  - security groups for firewall rules for ports 22 and 8080
  - restrict the access to limited ip addresses to avoid risks
- You have SSH and GeoServer access to the VM
- You have copied the GeoServer "Platform Independent Binary" installation package to the server

## Summary details about the GeoServer VM

The operating system of the VM is Ubuntu 16.04 and the installationof GeoServer is done using the **Linux binary** based on the official installation instructions:
http://docs.geoserver.org/maintain/en/user/installation/linux.html

The installation steps differ from the basic installation in the following:
- Ubuntu machine set to Europe/Helsinki timezone for the logs to be in local time
- GeoServer is added as a service to Ubuntu for automatic startup on reboot
- CORS is manually enabled to allow JavaScript apps to run

See below for specific installation commands and settings.

## GeoServer customization for teaching purposes
GeoServer configuration can been customized this way:
- The GROUP_ADMIN role is modified to have ADMIN role as parent (gives full admin capabilities)
- A user named "student" has been created with GROUP_ADMIN role
- the Admin and Master/root user accounts are set to the same password

If you need such a GeoServer VM, you can also request for a ready VM image from CSC's service desk. The image has the specifications described above. You can also create such a VM yourself by following instructions below.


## GeoServer customization
After GeoServer has been installed, make following edits:
- At first login (admin:geoserver), the Admin and Master/root user accounts are set to the same password <course-admin-password>
- The GROUP_ADMIN role is modified to have ADMIN role as parent (gives full admin capabilities)
- A user named "student" has been created with GROUP_ADMIN role

## Suggested customizations
- Add course/department specific details to the GeoServer contact information


## How GeoServer is used by the students
- The students have only access to the GeoServer web GUI using the "student" user with the provided password.
- The students have access to most of the administrator functionality of GeoServer
- No access to the web server machine
- The exercise instructions requests the students to be careful with the GeoServer general definitions (that affect the whole platform) and are request to limit their edits to their own Workspaces
- The student creates its own named Workspace where edits are made adding and editing stores, layers, styles... (also named with the student's name).

## Potential problems
- Students can edit GeoServer general details that affect everyone
- Students can change Admin and student passwords (on purpose or by simply testing what it does), locking everyone out
- Students can see, edit, delete other student's work and settings

## Preparations for problem situations
- if student password is changed, Admin user can reset
- if admin password is changed, student user can reset
- if Admin and student password is change, master password needs to be used
  - login as "root", password is same as for Admin
  - edit the Admin password to original value



## Installation commands and settings
````bash
# You have an Ubuntu 16.04 server with proper security groups (firewalls) in place (you need access to at least ports 22 and 8080). You also have the "Platform Independent Binary" installation package in the server.

# Preliminary steps
# ----------------
# Update VM
sudo apt-get update
sudo apt-get -y upgrade
# Change server's time zone to Helsinki
sudo timedatectl set-timezone Europe/Helsinki

### Install Java
sudo add-apt-repository -y ppa:webupd8team/java
sudo apt-get update
# Manually accept licenses for oracle java
sudo apt-get install -y oracle-java8-installer

# Install GeoServer following http://docs.geoserver.org/maintain/en/user/installation/linux.html
sudo apt install unzip
sudo unzip geoserver-2.12.1-bin.zip -d /usr/share/
# change owner of geoserver folder to "cloud-user"
sudo chown -R cloud-user /usr/share/geoserver-2.12.1/

# Set up environment variables
# Check path to Java and set to environment
sudo update-alternatives --config java
# copy your java path without the "/jre/bin/java" part
sudo bash -c "echo JAVA_HOME=/usr/lib/jvm/java-8-oracle >> /etc/environment"
source /etc/environment
echo $JAVA_HOME
# Set GeoServer home variable
echo "export GEOSERVER_HOME=/usr/share/geoserver-2.12.1" >> ~/.profile
source ~/.profile
echo $GEOSERVER_HOME

# Test your GeoServer manually
screen sh $GEOSERVER_HOME/bin/startup.sh
# To detach the screen terminal just push Ctr+A +D
# Check process is running
ps aux | grep GEOSERVER
# Check also the GeoServer web GUI at http://vm-public-ip:8080/geoserver/web/
# Stop the server
sh $GEOSERVER_HOME/bin/shutdown.sh

# Add GeoServer as service so it starts with VM starts
sudo vim /etc/systemd/system/geoserver.service
# Manually add these lines to the file
# Edit the parts with the Java and GeoServer paths as mentioned above
[Unit]
Description=GeoServer Jetty container starter (metadata service crawler)
After=network.target

[Service]
User=cloud-user
Environment=JAVA_HOME=/usr/lib/jvm/java-8-oracle
Environment=GEOSERVER_HOME=/usr/share/geoserver-2.12.1
ExecStart=/usr/share/geoserver-2.12.1/bin/startup.sh
ExecStop=/usr/share/geoserver-2.12.1/bin/shutdown.sh

# Output needs to appear in instance console output
StandardOutput=journal+console

[Install]
WantedBy=multi-user.target
# end of service file

# Add the service
sudo systemctl daemon-reload
sudo systemctl enable geoserver.service
sudo shutdown -r now

# After restart, check that GeoServer is running after VM restarts at http://vm-public-ip:8080/geoserver/web/
# Check also from the terminal
ps aux | grep GEOSERVER
journalctl -b | less | grep GEOSERVER

# Enabling CORS to allow JavaScript applications
# Edit manually following http://docs.geoserver.org/latest/en/user/production/container.html#enable-cors

````
