# OpenDroneMap

Notes: 
* The basic OpenDroneMap is also available in [Puhti](https://docs.csc.fi/apps/opendronemap/), but OpenDroneMap Web requires cPouta. 
* UEF drone lab has very detailed instructions for OpenDroneMap and OpenDroneMap Web in [GeoPortti](https://www.geoportti.fi/tools/instruments/) (see the end of the page).
* These guidelines are from 2019, so they might be out-dated.

## Installing OpenDroneMap with Docker in a cPouta VM

1. [Create Ubuntu virtual machine](https://docs.csc.fi/cloud/pouta/launch-vm-from-web-gui/)
2. [Install Docker](https://docs.docker.com/engine/install/ubuntu/)
3. [Install OpenDroneMap CLI with Docker](./docker-opendronemap.md)

### Example automated ansible script
**Note** that you need to know Ansible before trying to make use of the script and that you might need to update/customize several parts of it.

This [example Ansible template](./ansible_docker_factory) serves as a template in case you want to automate the creation of the VM descried above.


