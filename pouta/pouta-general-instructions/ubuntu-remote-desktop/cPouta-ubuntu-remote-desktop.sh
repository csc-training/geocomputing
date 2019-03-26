#!/bin/bash
## Run as root, using "sudo"
set -x #echo on

#####################
###Install Gnome, TightVNC & xRDP servers, autocutsel and g++ compiler
#####################
apt-get update
apt-get upgrade -y
apt-get install -y ubuntu-desktop gnome-session-flashback tightvncserver xrdp autocutsel g++

##Configure VNC for user cloud-user
su cloud-user << CLOUD-USER
cd
mkdir -p ~/.vnc
# change the password in next line and uncomment
#echo <your-secret-password> | vncpasswd -f > ~/.vnc/passwd
chmod 600 ~/.vnc/passwd

##Ensure that the desktop environment is launched when connecting to VNC + enable Copy/Paste using ClipBoard

bash -c 'cat > ~/.vnc/xstartup <<EOF
#!/bin/sh
xrdb $HOME/.Xresources
xsetroot -solid grey
autocutsel -fork
def
export XKL_XMODMAP_DISABLE=1
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS

gnome-panel &
gnome-settings-daemon &
metacity &
nautilus &
gnome-terminal &
EOF'

#Give execution permissions
chmod +x ~/.vnc/xstartup
exit
CLOUD-USER

##Configure xRDP
bash -c 'cat > /etc/xrdp/xrdp.ini <<EOF
[globals]
bitmap_cache=yes
bitmap_compression=yes
port=3389
crypt_level=low
channel_code=1
[vnc1]
name=vncserver
lib=libvnc.so
ip=localhost
port=5901
username=cloud-user
password=ask
EOF'


#####################
###Setup vnc as a system service
#####################
su - cloud-user << CLOUD-USER
touch ~/.Xauthority
mkdir -p ~/.config
exit
CLOUD-USER

# create a VNC system service:
bash -c 'cat > /etc/systemd/system/vncserver@:1.service <<EOF
[Unit]
Description=Start TightVNC server at startup
After=syslog.target network.target

[Service]
Type=forking
User=cloud-user
PAMName=login
PIDFile=/home/cloud-user/.vnc/%H%i.pid
#ExecStartPre=/usr/bin/vncserver -kill %i > /dev/null 2>&1
ExecStart=/usr/bin/vncserver -depth 24 -geometry 1920x1080 %i
ExecStop=/usr/bin/vncserver -kill %i

[Install]
WantedBy=multi-user.target
EOF'

#Reload the systemctl daemon as root
systemctl daemon-reload
#Start the VNC service as root.
systemctl start vncserver@:1.service
#Enable it on system startup as root.
systemctl enable vncserver@:1.service

#####################
###Change keyboard leyout in for xrdp session
#####################
cd /etc/xrdp
cp km-041d.ini km-040b.ini
chown xrdp:xrdp km-040b.ini
#Reboot xrdp server
/etc/init.d/xrdp restart

#####################
###Install Browser, text editor and other useful stuff
#####################
apt-get install firefox gedit -y

#Install Google Chrome
bash -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list'
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
apt update
apt install google-chrome-stable -y
