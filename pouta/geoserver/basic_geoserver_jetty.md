
# Basic GeoServer installation

The following instructions describe the steps to install a GeoServer server (with in-built Jetty container) in an Ubuntu 16.04 virtual machine.

## Prerequisites
You need to have a basic virtual machine (VM) with a ready Ubuntu OS. These instructions have bee tested in a CSC's cPouta environment and with a Ubuntu 16.04 OS.

Hardware requirements:
- a machine with 1 core and 4 Gb of RAM is enough for testing and not demanding purposes (tested with cPouta's hpc-gen1.1core flavour, see about [cPouta flavours](https://research.csc.fi/pouta-flavours))

Security recommendations:
- Define the VM's security settings carefully (for cPouta, see [Security Guidelines for cPouta](https://research.csc.fi/pouta-security)):
  - VM ssh access is secured with a keypair.
  - security groups for firewall rules for ports 22 and 8080.
  - restrict the access to limited ip addresses to avoid risks.

## GeoServer installation
Installation of GeoServer is done using the [**Linux binary** official installation instructions](
http://docs.geoserver.org/maintain/en/user/installation/linux.html).

The installation steps differ from the basic installation in the following:
- Ubuntu machine set to Europe/Helsinki timezone for the logs to be in local time.
- GeoServer is added as a service to Ubuntu for automatic startup on reboot.

Below are specific installation commands and settings.

### Install basic platform-independent GeoServer

Copy the [**Platform Independent Binary** installation package](http://geoserver.org/release/maintain/) to the VM.

From your VM's terminal:

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

Note that you still need to add GeoServer as a service and restart the machine for GeoServer to start.

### Add GeoServer to start automatically at VM boot
````bash
# Check path to Java and set to environment
sudo update-alternatives --config java
# When setting your java path in the service definition below, use it without the "/jre/bin/java" part

# Add GeoServer as service so it starts with VM starts
sudo vim /etc/systemd/system/geoserver.service
# --- start of geoserver.service file ---
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
# --- end of geoserver.service file ---

# Add the service
sudo systemctl daemon-reload
sudo systemctl enable geoserver.service
sudo shutdown -r now
````

After your VM restars, test that your GeoServer is up and running via the web GUI: http://vm-public-ip:8080/geoserver/web/ (edit the vm-public-ip with your VM public ip).

You can check that the server is running via the terminal for example with:
````bash
ps aux | grep GEOSERVER
journalctl -b | less | grep GEOSERVER
````

### Set the `admin` and `master` passwords

After GeoServer has been installed, the first thing you **must do** is to change the passwords for admin and master users and add new user for students.

Use the links in the home page of GeoServer web interface and:
- Change the `admin` password the first time you login (default password is `geoserver`).
- Set the `master` account password (see [Root account](http://docs.geoserver.org/stable/en/user/security/root.html) from GeoServer documentation).

## Optional settings to GeoServer
The following are some possibly interesting customization of GeoServer. Review the intention the customiataions and implement them if needed.

### Enabling CORS to allow JavaScript applications
If students want to use GeoServer services for example from a OpenLayers application, which code they write on the local machine, CORS must be allowed on GeoServer.
- Edit manually the GeoServer configuration following these [instruction](http://docs.geoserver.org/latest/en/user/production/container.html#enable-cors).
