# NOTE: THIS EXAMPLE WAS FOR TAITO. GRASS PYTHON LIBRARIES ARE NOT INSTALLED ON PUHTI SUPERCOMPUTER AT THE MOMENT

If you wish to use GRASS with Python on Puhti, contact servicedesk@csc.fi

## Multiprocessing with python and grass
Pygrass has ParallelModuleQue class that allows to run number of pygrass modules (=grass tools) in parallel. In this example a raster is processed in tiles using mapcalc module in a way that each tile is processed separately and result saved into it's own raster dataset. All the tiles (if enough cores is available) are processed in parallel. Splitting the input raster into tiles is done by setting the computational region to cover the particular tile being added to the processing que. 

More info on ParallelModuleQue: https://grass.osgeo.org/grass72/manuals/libpython/pygrass.modules.interface.html#pygrass.modules.interface.module.ParallelModuleQueue

In this example the pygrass code is run in two ways:

1. Starting grass and running the python code within grass.
2. Running python code directly and setting up grass enviroinment within python script. (for more info see https://grass.osgeo.org/grass70/manuals/libpython/script.html#module-script.setup)
