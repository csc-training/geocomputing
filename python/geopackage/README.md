## Reading NLS topographic database geopackage with Python
The NLS topographic database has been saved into several geopackage files in Puhti at /appl/data/geo/mml/maastotietokanta/2020/gpkg. The larger layers are in their own gpkg files and the smaller layers have been bundled into a single file. The larger layers are quite large and reading them takes some time. If the whole layers are not however needed it is possible to use Geopandas to only read the desired parts of the files. The examples can be found in the read_gpkg.py script

In Puhti [geoconda](https://docs.csc.fi/apps/geoconda/) module can be used.

Similar examples for reading the geopackage with R using SF package can be found [here](https://github.com/csc-training/geocomputing/tree/master/R/geopackage).
