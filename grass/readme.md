# GRASS GIS example batch jobs for Puhti supercomputer

* [GRASS shell scripts](https://grasswiki.osgeo.org/wiki/GRASS_Python_Scripting_Library). [Example](01_serial_cli)
* [GRASS Python Scripting Library](https://grasswiki.osgeo.org/wiki/GRASS_Python_Scripting_Library). [Example](02_python_scripting_serial)
* [PyGRASS](https://grasswiki.osgeo.org/wiki/Python/pygrass). Examples: [basic serial](03_pygrass_serial) and [parallel with GridModule](04_pygrass_parallel)
* In these examples temporary location is used, in many cases it is better to use permanend GRASS mapset and location. If using temporary location with bigger datasets, use compute nodes with [local NMVE disk](https://docs.csc.fi/computing/running/creating-job-scripts-puhti/#local-storage), which have more temporary space available or set TMPDIR to be a folder in scratch (`export TMPDIR=/scratch/project_200xxxx/grass/tmp`
).

Python Scripting suits simpler cases when chaining existing tools is enough, PyGRASS enables data access from Python.
See [GRASS page in CSC Docs](https://docs.csc.fi/apps/grass/#references), for addtional external references.
