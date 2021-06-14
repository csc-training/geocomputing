# GRASS GIS examples for Puhti HPC

GRASS commands can be run in HPC batch jobs with:

* [GRASS shell scripts](https://grasswiki.osgeo.org/wiki/GRASS_Python_Scripting_Library). [Example](01_serial_cli)
* [GRASS Python Scripting Library](https://grasswiki.osgeo.org/wiki/GRASS_Python_Scripting_Library). [Example](02_python_scripting_serial)
* [PyGRASS](https://grasswiki.osgeo.org/wiki/Python/pygrass). Examples: [basic serial](03_pygrass_serial) and [parallel with GridModule](03_pygrass_parallel)

Useful links:
* [GRASS database, location, mapset and region](https://grass.osgeo.org/grass79/manuals/grass_database.html), the basic concepts always needed with GRASS GIS. 
In case of using parallel computation, be extra careful with `region`.
* [GRASS GIS Python library documentation](https://grass.osgeo.org/grass79/manuals/libpython/script.html)
* [Using GRASS GIS through Python and tangible interfaces (workshop at FOSS4G NA 2016)](https://grasswiki.osgeo.org/wiki/Using_GRASS_GIS_through_Python_and_tangible_interfaces_(workshop_at_FOSS4G_NA_2016)), 
including Parallelization examples with GRASS `ParallelModuleQueue`, GRASS `GridModule` and Python `multiprocessing`.
