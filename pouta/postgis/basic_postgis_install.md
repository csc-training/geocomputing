# Basic PostGIS installation

The following instructions describe the steps to install PostGIS in an Ubuntu 16.04 virtual machine in cPouta environment.

## Prerequisites
You need to have a basic virtual machine (VM) with a ready Ubuntu OS. These instructions have been tested in a CSC's cPouta environment and with a Ubuntu 16.04 OS.

Hardware requirements:
- a machine with 1 core and 4 Gb of RAM is enough for testing and not demanding purposes. For cPouta virtual machines' configurations, see [cPouta flavours](https://docs.csc.fi/cloud/pouta/vm-flavors-and-billing/)).

Security recommendations:
- Define the VM's security settings carefully (for cPouta, see [Security Guidelines for cPouta](https://docs.csc.fi/cloud/pouta/security/)):
  - VM ssh access is secured with a keypair.
  - security groups for firewall rules for ports 22 and 5432.
  - restrict the access to limited ip addresses to avoid risks.

## Postgis installation
The steps below will install a PostgreSQL 9.6 database with PostGIS 2.3.

The installation is based on the general [OSGeo PostGIS installation instructions](https://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS23UbuntuPGSQL96Apt). You should be able to understand the installation steps and make modifications if needed for your case.

### Preparation steps

Connect to your VM and run the following commands from the terminal, see comments in the code for more details:

````sh
# Run as superuser
sudo su
# Verify what version of Ubuntu you are running
apt-get update
lsb_release -a

# Add PostgreSQL respository in the file sources.list.
# For xenial (16.04 LTS) (replace "xenial" in the command below with whatever
# version lsb states)
sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt xenial-pgdg main" >> /etc/apt/sources.list'
# Add Keys
wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
apt-get update

# Install PostgreSQL and PostGIS
# The following will install postgresql 9.6, PostGIS 2.3, PGAdmin4, pgRouting 2.3 and additional supplied modules including the adminpack extension:
apt-get install -y postgresql-9.6  postgresql-contrib-9.6
apt-get install -y postgresql-9.6-pgrouting postgresql-9.6-pgrouting-scripts
apt-get install -y postgresql-9.6-postgis-2.3 postgresql-9.6-postgis-2.3-scripts

# To get the commandline tools shp2pgsql, raster2pgsql you need to install also postgis.
apt-get install -y postgis

# Optionally install also GUI tools: postgis-gui (sh2pgsql-gui) and pgadmin
apt-get install -y postgis-gui pgadmin3

### Fix postgres installation filenames
#(there is a bug inthe basic installation of some of the plugins)
mv /usr/share/postgresql/9.6/extension/pgrouting.control /usr/share/postgresql/9.6/extension/pg_routing.control
mv /usr/share/postgresql/9.6/extension/pgrouting--2.5.2.sql /usr/share/postgresql/9.6/extension/pg_routing--2.5.2.sql

# Enable Adminpack in postgres databse
# Create a "gisdb" database and the schema postgis into it
# Enable PostGIS, pgRouting and other extensions for schema postgis
su - postgres <<POSTGRESSETUP
psql -U postgres
CREATE EXTENSION adminpack;
-- Never install PostGIS in the postgres database, create a user database
-- Enable postgis in gisdb database
CREATE DATABASE gisdb;
\connect gisdb;
CREATE SCHEMA postgis;
ALTER DATABASE gisdb SET search_path=public, postgis, contrib;
-- this is to force new search path to take effect
\connect gisdb;
CREATE EXTENSION postgis SCHEMA postgis;
-- SELECT postgis_full_version();
CREATE EXTENSION pg_routing SCHEMA postgis;
CREATE EXTENSION fuzzystrmatch SCHEMA postgis;
CREATE EXTENSION postgis_topology; -- not into: SCHEMA postgis;
CREATE EXTENSION postgis_tiger_geocoder; -- not into:  SCHEMA postgis;
\q
POSTGRESSETUP

su - postgres <<POSTGRESSETUP
# Enable postgres to listen on all IP's
# Configuration is normally set in: /etc/postgresql/9.6/main/postgresql.conf
# but when done within psql, it goes to /var/lib/postgresql/9.6/main/postgresql.auto.conf
psql -U postgres
-- It takes effect only after restarting the service (service postgresql restart)
ALTER SYSTEM SET listen_addresses='*';
\q
POSTGRESSETUP

# Edit pg_hba.conf to allow md5 connections from any IP
# sed -i -e 's/host    all             all             127.0.0.1\/32/host    all             all             0.0.0.0\/0/g' /etc/postgresql/9.6/main/pg_hba.conf
sed -i -e 's/host    all             all             127.0.0.1\/32/hostssl    all             all             0.0.0.0\/0/g' /etc/postgresql/9.6/main/pg_hba.conf

# Restart postgresql
service postgresql restart

# Create new PGSQL user
# EDIT THE USER'S NAME AND PASSWORD
su - postgres <<NEWUSER
psql -U postgres
-- edit this to your own user and password
CREATE ROLE geo LOGIN PASSWORD 'geoman' SUPERUSER;
NEWUSER
````

You are done!

You can test your PostGIS database by connecting to it at the VM's public IP on port 5432 from your local machine. Use for example your local pgAdmin or QGIS applications to test it.
