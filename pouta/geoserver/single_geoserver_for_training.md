# Single GeoServer VM for teaching
The aim of this workflow is to set up GeoServer for a university course. The same GeoServer instance is used by several students. Students upload their data using QGIS [GeoServer Explorer plugin](https://plugins.qgis.org/plugins/geoserverexplorer/) and then continue adjusting settings from GeoServer web admin interface.

The installation is done using [GeoServer "Platform Independent Binary" installation package](http://geoserver.org/release/stable/), which includes built-in Jetty servlet container. The basic installation has been modified so that the GeoServer is started at boot time (see details below).

## How GeoServer is used by the students
- The students have only access to the GeoServer web GUI and REST API.
- All students share the same GeoServer "student" user account.
- The students have access to most of the administrator functionality of GeoServer.
- The students have no shh access to the web server machine.
- The exercise instructions ask the students to be careful with the GeoServer general definitions (that affect the whole platform) and are request to limit their edits to their own Workspaces.
- The student creates its own named Workspace where edits are made adding and editing stores, layers, styles... (also named with the student's name).

## Course GeoServer installation
Follow these instruction to set up a GeoServer VM for a course with the above mentoined specifications.

If you need such a GeoServer VM, and you are a CSC's customer,  you can also request for a ready VM image from servicedesk@csc.fi.


### Basic GeoServer installation
Start with the basic installation of a GeoServer virtual machine as described in:
- [Basic GeoServer installation](basic_geoserver_jetty.md).
- To allow for JavaScript applications to run, enable CORS as specified in the  from the installatione the [Basic GeoServer installation](basic_geoserver_jetty.md) optional settings section.

### Adding a `student` user
To limit (a little bit) what students can do with the GeoServer, make them a separate user account. Here students are still given a lot of permissions, depending on your course exercises, it might make sense to limit more.
- Modify the `GROUP_ADMIN` role to have `ADMIN` role as parent (gives full admin capabilities)
- Add a user named `student` with `GROUP_ADMIN` role

Potential problems with the `student` account having administrator rights:
- Students can edit GeoServer general details that affect everyone
- Students can change Admin and student passwords (on purpose or by simply testing what it does), locking everyone out
- Students can see, edit, delete other student's work and settings

Preparations for problem situations:
- if student password is changed, Admin user can reset
- if admin password is changed, student user can reset
- if Admin and student password is changed, master password needs to be used
  - login as "root", password is same as for Admin
  - edit the Admin password to original value
- if students delete other students work, try to recover from a backup of the data directory (not yet implemented in the installation instructions above).

### Contact info (optional)
You can add some general information to GeoServer to indicate course specific details. For example:
- Add course/department specific details to the GeoServer [contact information](http://docs.geoserver.org/stable/en/user/configuration/contact.html)
