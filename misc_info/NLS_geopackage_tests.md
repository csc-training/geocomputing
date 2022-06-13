## NLS Geopackage tests

Main findings:
* Tested using with geopandas, R sf library and ogr2ogr. Geopandas and ogr2ogr both have some good advantages, sf not so much.
* Memory usage: Ogr2ogr is clearly more memory efficient as it seems that it's memory consumption is more or less constant regardless of input size. It probably handles the files in some sort of pieces. Geopanadas and sf on the other hand have to read the whole file into memory at once, but sf memory consumption is about 2x that of geopandas. Ogr2ogr 0.5GB, geopandas up to 15GB for single layer, sf up to 39 GB single layer.
* Computation time: Extracting the largest layers takes 21 and 24 mins with sf and geopandas (only read to memory), 49 mnins for ogr2ogr (includes saving to another file). Interestingly there wasn't significant time performance differences in smaller layers.
* Extracting a small area efficiently is possible. At least geopandas can make use of spatial indexes built into the geopackage format and read a small area defined by a bounding box fast even from largest layers. For the other two this should also be possible as there's an option to use SQL queries, but I couldn't make them perform any faster than reading the whole layer.
* Buffering & similar analysis using SQL queries is possible with ogr2ogr. With sf and geopandas you'll have to use different libraries after reading the file into a dataframe.
* Geopackage standard doesn't enforce a specific name for the geometry column, you can see it with ogrinfo.
* Example code for [R](R/geopackage) and [Python](python/geopackage).

### Testing results

Geopandas (read)

Layer		|Time	|Max rss|
--------------| ----- | ----- |
Hylky		|1s	|	|
Kallioalue (4,5GB)|10:31|6,6GB|
Suo 14GB|24:09	|15GB|
Suo small bbox (7 features)*|0:03|0.8GB|

*~`geopandas.read_file(file, layer, bbox=)` Takes features that are at least partially within bbox.

R sf (read)

Layer		|Time	|Max rss|
-------------- | ----- | ----- |
Hylky		|2s	|	|
Kallioalue (4,5GB)|8:03|12GB|
Suo 14GB|21:26	|39GB|

ogr2ogr (read & write)  
`ogr2ogr kallio.gpkg MTK-geopackage-test-18-06-07.gpkg -sql "select * from kallioalueet"`

Layer		|Time	|Max rss|
-------------- | ----- | ----- |
Kallioalue (4,5GB)|11:09|0.38GB|
Suo 14GB|49:09	|0.33GB|
