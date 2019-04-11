## Reading NLS topographic database geopackage with Python
The NLS topographic database has been saved into several geopackage files in Taito at /proj/ogiir-csc/mml/maastotietokanta/2019. The larger layers are in their own gpkg files and the smaller layers have been bundled into a single file. The larger layers are quite large and reading them takes some time. If the whole layers are not however needed it is possible to use Geopandas to only read the desired parts of the files. The examples can be found in the read_gpkg.py script

In Taito [geoconda](https://research.csc.fi/-/geoconda) module can be used.

Similar examples for reading the geopackage with R using SF package can be found [here](https://github.com/csc-training/geocomputing/tree/master/R/geopackage).
