# Single GeoServer VM for teaching
The aim of this workflow is to set up GeoServer for a university course. The same GeoServer instance is used by several students. Students upload their data using QGIS [GeoServer Explorer plugin](https://plugins.qgis.org/plugins/geoserverexplorer/) and then continue adjusting settings from GeoServer web admin interface.

The installation is done using [GeoServer "Platform Independent Binary" installation package](http://geoserver.org/release/stable/), which includes built-in Jetty servlet container.

## How GeoServer is used by the students
- The students have only access to the GeoServer web GUI and REST API.
- All students share the same GeoServer "student" user account.
- The students have access to most of the administrator functionality of GeoServer.
- The students have no shh access to the web server machine.
- The exercise instructions ask the students to be careful with the GeoServer general definitions (that affect the whole platform) and are request to limit their edits to their own Workspaces
- The student creates its own named Workspace where edits are made adding and editing stores, layers, styles... (also named with the student's name).

# Installation
## Prerequisites
Prerequisites to follow installation instructions:
- Virtual machine (VM) with Ubuntu, the instructions are tested with Ubuntu 16.04 (use for ex. CSC's cPouta environment)
  - TODO: size recommendatation, links to cPouta page?
- Proper security settings are defined: (TODO links?)
  - keypair to access the VM
  - security groups for firewall rules for ports 22 and 8080
  - restrict the access to limited ip addresses to avoid risks
- The ports for SSH and GeoServer are open, at least ports 22 and 8080 (TODO: correct?)
- You have copied the GeoServer "Platform Independent Binary" installation package to the server

## GeoServer installation
Installation of GeoServer is done using the [**Linux binary** official installation instructions:](
http://docs.geoserver.org/maintain/en/user/installation/linux.html)

The installation steps differ from the basic installation in the following:
- Ubuntu machine set to Europe/Helsinki timezone for the logs to be in local time.
- GeoServer is added as a service to Ubuntu for automatic startup on reboot.
- CORS is manually enabled to allow JavaScript apps to run.
- New `student` user is added to GeoServer.

If you need such a GeoServer VM, you can also request for a ready VM image from CSC's service desk. The image has the specifications described here. You can also create such a VM yourself by following these instructions.

Below are specific installation commands and settings.

### Basic GeoServer installation

````bash
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
````

### Install a service for GeoServer to start with the VM at boot
````bash
# Check path to Java and set to environment
sudo update-alternatives --config java
# When setting your java path in the service definition below, use it without the "/jre/bin/java" part

# Add GeoServer as service so it starts with VM starts
sudo vim /etc/systemd/system/geoserver.service
# Manually add these lines to the file
# Edit the parts with the Java and GeoServer paths to match your system
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
````
Test that your GeoServer is up and running via the web GUI: http://<vm-public-ip>:8080/geoserver/web/ (edit the <vm-public-ip> with your VM public ip).

You can check that the server is running via the terminal for example with:
````bash
ps aux | grep GEOSERVER
journalctl -b | less | grep GEOSERVER
````

### Enabling CORS to allow JavaScript applications
Edit manually the GeoServer configuration following the instruction at: http://docs.geoserver.org/latest/en/user/production/container.html#enable-cors


### Managing GeoServer users
After GeoServer has been installed, change the Master password and add new user for students:
- At first login (admin:geoserver), sey the Admin and Master/root user accounts to the same password <course-admin-password> (TODO: unclear)
- Modify the GROUP_ADMIN role to have ADMIN role as parent (gives full admin capabilities)
- Add a user named "student" with GROUP_ADMIN role

#### Potential problems
- Students can edit GeoServer general details that affect everyone
- Students can change Admin and student passwords (on purpose or by simply testing what it does), locking everyone out
- Students can see, edit, delete other student's work and settings

#### Preparations for problem situations
- if student password is changed, Admin user can reset
- if admin password is changed, student user can reset
- if Admin and student password is changed, master password needs to be used
  - login as "root", password is same as for Admin
  - edit the Admin password to original value
  
### Contact info (optional)
- Add course/department specific details to the GeoServer contact information
