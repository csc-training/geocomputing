# Metashape in cPouta with VNC

Setting up virtual machine in cPouta environment for Metashape.
Instructions by Antti-Jussi Kieloaho (LUKE)

Useful documentation:
* [VirtualGL](https://wiki.archlinux.org/index.php/VirtualGL#Using_VirtualGL_with_VNC)
* [VirtualGL documentation](https://virtualgl.org/vgldoc/2_1_1/#hd004001)
* [Metshape documentation](https://www.agisoft.com/pdf/metashape-pro_1_7_en.pdf)
* [Running Metashape in calculation node](https://www.agisoft.com/forum/index.php?topic=10896.0)


## Configuration of Virtual machine

Create a GPU VM in pouta.csc.fi using Cuda image. For Cuda image username is cloud-user.

## Setting up remote desktop

### Configuration of remote (cPouta)

1. Install xorg and openbox

```
sudo apt-get update
sudo apt install lightdm
sudo apt-get install xorg openbox
```

2. Configure X for the NVIDIA driver

2.1 Find out the card's BusID address

```
nvidia-xconfig --query-gpu-info
```

2.2 Replace with a query result (as an example PCI:0:5:0)
```
sudo nvidia-xconfig -a --allow-empty-initial-configuration --use-display-device=None --virtual=1920x1200 --busid=PCI:0:5:0
```
 
- This step creates new X configuration file to '/etc/X11/xorg.conf'

 
2.3 Configure lightdm for vnc server

(Not sure if this is necessary but it didn’t hurt either)

```
sudo nano /etc/lightdm/lightdm.conf
```
 
```
[VNCServer]
enabled=true
command=Xvnc -rfbauth /etc/vncpasswd
port=5900
listen-address=localhost
width=1920
height=1200
depth=24
```

3. Download and install VirtualGL and TurboVNC servers

```
wget https://sourceforge.net/projects/virtualgl/files/2.6.5/virtualgl_2.6.5_amd64.deb
wget https://sourceforge.net/projects/turbovnc/files/2.2.6/turbovnc_2.2.6_amd64.deb
sudo dpkg -i virtualgl_*.deb turbovnc_*.deb
```

4. Configure the VirtualGL server

4.1 if you are the only user on the VM answer No to all questions (choose: 1,n,n,n,x)
 
```
sudo /etc/init.d/lightdm stop
sudo /opt/VirtualGL/bin/vglserver_config
```
 
- if did not work test following:
```
sudo /opt/VirtualGL/bin/vglserver_config  -config +s +f -t
```
 

5. Reboot your cPouta VM
```
sudo reboot
```
 

6. Launch VNC server with window size
```
/opt/TurboVNC/bin/vncserver -geometry 1920x1080
```
- First time type (up to) 8 characte password twice and reply NO to a view-only password
- Creating default startup script `/home/cloud-user/.vnc/xstartup.turbovnc`
- Starting applications specified in `/home/cloud-user/.vnc/xstartup.turbovnc`
- Log file is `/home/cloud-user/.vnc/metashape-vm:1.log`


7. Start X server (hit return twice) and set display number to 0
```
/usr/bin/X :0 &
```
- hit enter twice
```
export DISPLAY=:0
```
 
NOTE: IF VM IS REBOOTED, RUN STEPS 6 AND 7. AGAIN


### Ubuntu Firewall configuration

It is good practice to activate firewall!


1.1 check if firewall is active
```
sudo ufw status verbose
```
1.2 if active proceed to step 2. otherwise skip firewall configuration

 
2. allow SSH
```
sudo ufw allow OpenSSH
```
3.1 to allow a single port 5901
```
sudo ufw allow 5901/tcp
```
3.2 to allow series of ports from 5901 to 5910
```
sudo ufw allow 5901:5910/tcp
```
4. check that intended firewall rules has taken place
```
sudo ufw status verbose
```
 

### Configuration of locale (your PC)
Open an encrypted SSH tunnel for the VNC connection between PC and VM

#### Option 1. In Mac by built-in SHH and VNC clients

1 open encrypted SSH tunnel to VM
```
ssh -L 5901:localhost:5901 cloud-user@86.50.253.165 -i .ssh/your_private_key.pem
```
2 leave ssh tunnel window open and write following on new window
```
open vnc://localhost:5901
```
- password window is prompt and after that remote desktop is up and running

#### Option 2. In Mac by using TurboVNC
Install if necessary VNC client from https://sourceforge.net/projects/turbovnc/files/
1 Install TurboVNC (at the time of writing version 2.2.5) to your local desktop PC

2 Open encrypted SSH tunnel for the VNC connection between your PC and the VM

3 The port used by TurboVNC server is shown when TurboVNC starts:
```
"TurboVNC started on display name-of-VM:1"
```
4 At your PC, choose unused port, e.g. 5911

5 After establishing SSH tunnel
```
vncviewer -via user@host localhost:n
```
<- where n is display number

 ### Useful commands for VNC clients and X server

- Find out TurboVNC server display number and process ID
```
/opt/TurboVNC/bin/vncserver -list
```
- Close TurboVNC server running at display 1
```
/opt/TurboVNC/bin/vncserver -kill :1
```
- Check if X server is running
```
ps auxw | grep X
```
- Stop X server
```
sudo killall Xorg (Ubuntu)
```
- check port that is listened
```
sudo lsof -i -P | grep -o "listen"
```
- port is 590*


### Installation of Agisoft Metashape

```
sudo apt-get update
sudo apt-get install libxrender1
mkdir -p agisoft
cd agisoft
sudo wget https://s3-eu-west-1.amazonaws.com/download.agisoft.com/metashape-pro_1_7_1_amd64.tar.gz
tar zxvf metashape-pro_1_7_1_amd64.tar.gz
cd metashape-pro/
# If you want to run Metashape on node-mode and headless version use following
./metashape.sh --node -platform offscreen
# otherwise
# vglrun ./metashape.sh
```

If there is following error message
```
"This application failed to start because it could not find or load the Qt plaform plugin 'xcb' in ''."
```
- run the following
```
QT_DEBUG_PLUGINS=1 ./metashape.sh
```
- if there is some library missing, e.g. libxcb-xinerama
```
sudo apt install -y libxcb-xinerama0
```
               
### Activation and deactivation of Agisoft Metashape

- Metashape have node-locked licence and it allows the software on one machine at a time
- Standard activation requires the machine to be connected to the Internet
- Activation code does not contain zero digits - only letter "O"
```
./metashape.sh --activate AC_TI_VI_TION_CO_DE
```
 
- If you are to replaca major system components or re-install operation system
-> the licence have to be deactivated first and the same key can be used to activate the renewed system
```
./metashape.sh --deactivate
```
 

### Useful commands for Agisoft Metashape

```
./metashape.sh --help
```
 



### Running program through VNC remote desktop

Run program by opening terminal by right-click
```
vglrun /path/to/application/metashape.sh
```
 
### Ubuntu upgrade

* Ubuntu running on VM should upgrade regularly
* Follow notifications when new releases of Ubuntu are available
