# Upgrading GeoServer

Assuming you have the settings mentioned in the [basic Jetty GeoServer installation instructions](basic_geoserver_jetty.md). Especially:
- application folder symlink: `/usr/share/geoserver`
- data folder symlink: `/usr/share/geoserver_data`

For more details see GeoServer's [Upgrading existing versions](http://docs.geoserver.org/stable/en/user/installation/upgrade.html) page.

## Make a backup of your data folder
From GeoSever's documentation:

> **Warning**
>
> Be aware that some upgrades are not reversible, meaning that the data directory may be changed so that it is no longer compatible with older versions of GeoServer. See Migrating a data directory between versions for more details.

**Always make a backup of your data folder before you update GeoServer**, in case you would need to revert the upgrade.

Zip your data folder with a name that resembles the date and the GeoServer version:

For example if you current GeoServer version was 2.12.1:
```
sudo apt install zip
zip -r /home/cloud-user/geoserver_data_2.12.1_2018-09-07.zip /usr/share/geoserver_data
```
You would use this data backup in case that you need to go back to using the current GeoServer version if you encounter some problems with the upgraded version.

## Upgrade GeoServer
Download the new **Platform Independent Binary** version directly into the GeoServer virtual machine and unzip it to `/usr/shared/` folder:
```
wget <new_version_link_from_Geoserver_download_page>
sudo unzip geoserver-2.14.0-bin.zip -d /usr/share/
```

**Change the ownership of that folder to "cloud-user"**
```
sudo chown -R cloud-user /usr/share/geoserver-2.14.0/
```
**Change the GeoServer application's symlink to the new version**
```
# overwrite the previous version application folder with the new one
sudo ln -sfn /usr/share/geoserver-2.14.0 /usr/share/geoserver
```

The data directory can remain the same as it was previously.

Finally, reboot the machine:

```
sudo /sbin/reboot
```

 Your server should now be running the new GeoServer version with the same layers and configuration as before the upgrade.
