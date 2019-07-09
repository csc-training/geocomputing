# Software for routing at CSC computing environment

Below is given a list of routing tools that can be used in CSC computing environment, either Taito or cPouta. At the very end also the main routing data sources are listed.  
Contributors: Kylli Ek (CSC), Elias Annila (CSC), Henrikki Tenkanen (HY), Janne Helin (LUKE), Tuomas Nummelin (LUKE), Olli-Jussi Korpinen (LUT).  
If you have any comments or additions, please send them to giscoord@csc.fi

## Routing in Taito
The best routing tools for Taito seem to be different Python libraries: 
* `networkx` is the slowest and requires most memory. One routing from North to South in Finland takes ca **3 minutes** and required **37GB** of memory. But it is likely the easiest tool and has a lot of examples available.
* `igraph` is clearly faster and requires less memory. One routing from North to South in Finland takes **3 seconds** and required **8 Gb** of memory.
* `graph-tool` should be fastest, but installation to Taito failed at the moment, though should be possible in principle.
* A more detailed performance comparision can be found [here](https://graph-tool.skewed.de/performance).
* `osmnx` is a good library for importing data from OpenStreetMap.

### Python osmnx
https://github.com/gboeing/osmnx  
Taito: available in geoconda module

`osmnx` is a libarary for retrieving OpenStreetMap data for routing. It can:
* Create a graph suitable for `networkx` library directly.
* There is a possiblity to choose type of network, driving, walking, etc. (no highways only though)
* Save the `networkx` graph in GraphML format, from where the data can be used also with `igraph` and `graph-tool` libraries.
* Read from OSM API. Data retrieval time from OSM: ~30mins for Helsinki area, 19h 30min for whole Finland.
* Read local .osm file. .osm files are available from Geofabrik.

Notes:
* If graph is needed repeatedly, it is good to save it as GraphML. Reading from GraphML file is much faster than reading local .osm file. GraphML size is also smaller both on disk and in memory.
* `networkx` graph requires a lot of memory if the study area is big, so make sure that you have enough memory. For example the OSM Finland graph requires ca 40 Gb.

### Python networkx
https://networkx.github.io/  
Taito: available in geoconda and geopython modules.

Pure Python routing library, which is simple and easy to use. 
* It can use any network data as input, from OSM or Shape file. The Shape file reader does not work with Digiroad data, but Henrikki Tenkanen has written own [importer for Digiroad](https://gist.github.com/HTenkanen/6ed582a97a83e9530bbdcca84bca8d0c).
* A lot of algorithms available. [Shortest path ones](https://networkx.github.io/documentation/stable/reference/algorithms/shortest_paths.html), inc Dijkstra and A*.
* Possible to run in parallel in Taito, some extra memory is needed. [Example code](https://github.com/csc-training/geocomputing/tree/master/python/routing).
* [A lof of examples for networkx and osmnx](https://github.com/gboeing/osmnx-examples/tree/master/notebooks).
* HY, Helle Joose used networkx in his gradu, source code in [GitHub](https://github.com/hellej/quiet-paths-msc/tree/master/src/batch_jobs/full_hel_nw)

### Python igraph
http://igraph.org/python/  
Taito: Easily to install with pip.

Python routing library which is based on C/C++ `igraph` library.
* [Different algoritms supported](http://igraph.org/python/doc/igraph.Graph-class.html#shortest_paths_dijkstra).
* Has GML-reader and GraphML-reader, loading the data for whole Finland from GraphML file for analysis use takes some minutes.
* No tools for Shape-file data. Possible work-around: read Shape files with `networkx`, save as GraphML, read with `igraph`.
* Possible to run in parallel in Taito, some extra memory is needed. [Example code](https://github.com/csc-training/geocomputing/tree/master/python/routing).
* Read `igraph` C documentation, if `igraph` Python documentation is unclear.

### Python graph-tool
https://graph-tool.skewed.de/  
Taito: Should work, but installation with conda was not successful in 2018 (just doing `conda install graph-tool` results in somehow broken gdal being installed). Installation not possible with pip, compiling from source should be possible, but not tested.

Python routing library with OpenMP support.
* [Supports Dijkstra and A*](https://graph-tool.skewed.de/static/doc/search_module.html).
* Can run in parallel.
* Can read GraphML, so data import with `osmnx` should be possible.
* No tools for Shape-file data. Possible work-around: read Shape files with `networkx`, save as GraphML, read with `graph-tool`.
   
### Othe tools
* **R** has rather limited support for routing. Something can be done for [example](https://rstudio-pubs-static.s3.amazonaws.com/278859_4b1f19cfba1640f3bd8a08b078ea99d0.html) with [osmar](http://osmar.r-forge.r-project.org/) and [igraph](http://igraph.org/r/) packages. There should be the same C-code behind doing the work as with Python `igraph` package. Taito: `igraph` is currently installed, `osmar` can be easily added.
* **SpatiaLite**. [Latuviitta guidelines for routing based on Finnish topographic map](http://latuviitta.org/documents/Maastotietokannan_reititys_ja_Spatialite.pdf), in Finnish. SpatiaLite is not currently installed to Taito, but should be possible.
* **OSMR, GraphHopper**. These can be installed to Taito for some limited use, but suite better to cPouta, so see comments below.

## Routing in cPouta
To cPouta any tool can be installed from techical point of view. If network is changing or custom network modifications are needed then PgRouting is likely the best option. OSMR and GraphHopper enable fast routing on OpenStreetMap data.

### PostGIS pgrouting
https://pgrouting.org/

PostGIS extention, enaboling queries as SQL, for example `select * from pgr_dijkstra(data, start point, end point)`.

Tools: 
* osm2pgrouting - data import from OSM.
* pgRouting - routing engine, backend for pgRoutingLayer.
* [pgRoutingLayer](https://github.com/pgRouting/pgRoutingLayer/wiki) - QGIS plug-in.

It can: 
* Use any network data as input: OSM, Digiroad, etc.
* Do routing on part of the data. 
* Use data that is changing.

Comments:
* 3 postgresql extensions needed: routing, postgis, pgrouting (CREATE EXTENSION ..).
* Routing from North to South in Finland takes ca 15 seconds.
* Check indexing for speed-ups.
* PostgresXL can not be used for distributing work load to a cluster of PostGIS servers, if using PgRouting functions.
* University of Helsinki has developed a door-to-door routing tool based on PgRouting called [DORA](https://blogs.helsinki.fi/saavutettavuus/autoilu-2018-door-to-door-routing-analyst-dora/).

Guidelines:
* [Importing Digiroad for pgRouting](https://www.paikkatietomies.fi/pgrouting_miehen_tiella_pitaa/), in Finnish.
* [Routing with QGIS pgRoutingLayer](https://gispohelp.zendesk.com/hc/fi/articles/115003510509-Reititys-pgRouting-laajennusosan-avulla), in Finnish.

### OSMR
https://github.com/Project-OSRM/osrm-backend

MapBox routing library, wrapped with API.
OSRM has two shortcut algoritms: Multi-level dijkstra and contraction hierarchies, for making the queries faster, so that not all possible combinations are checked, but some likely subset.
Reads in OSM data in PBF format, available for example from GeoFabrik.

Services:
* Tile: MapBox tile with roads, good for inspecting what your data looks like.
* Route: Get route from A to B. JSON result, inc geometry and turn instructions.
* Nearest: Find the nearest road to a point, use this for routing.
* Match: Snap GPS track to road.
* Trip: Route optimizing to many points.
* Table: Input n points, gives time matrix. From this data isocrones can be calculated, how much time it takes to drive to points around you.

Limitatons:
* One instance for one profile: driving, walking, cyclying.
* Other data than OSM difficult.
* Modifying data is difficult.

OSRM from R: https://github.com/rCarto/osrm

Taito: Possible to install to Taito, but the usage is limited to C/C++ or Node.js.  

### GraphHopper
https://github.com/graphhopper/graphhopper

* Reads in OSM data in PBF format or public transportation data in GTFS format.
* Routing with Dijkstra, A* and CH.
* Multiple weightings (fastest/shortest/...) and pre-built routing  profiles: car, bike, racingbike, mountain bike, foot, motorcycle, ...
* Displays and takes into account elevation data (per default disabled).
* Turn costs and restrictions (flexible and hybrid mode only).
* Scales from small indoor-sized to world-wide-sized graphs.
* Find nearest point on street e.g. to get elevation or 'snap to road'.
* Calculate isocrones.
* Fast for finding one route.

Taito: Might be possible to install, but usage limited to Java.

### Python arcpy
http://desktop.arcgis.com/en/arcmap/10.5/tools/network-analyst-toolbox/find-routes.htm
cPouta: Some kind of installation possible with ArcGIS Server.

* Very easy to use ESRI's road and street network data.
* Can use any network data as input: OSM, Digiroad, etc.
* Easy to use, script can be created with Model builder.
    
Limitations:
* ArcPro/ArcMap has front-end for ArcPy, but it can not be used in CSC env.

### Other tools
* [SNAP](https://snap.stanford.edu/snappy/)
* [SparkGraph](https://spark.apache.org/graphx/) - Spark analysis on huge networks.
* [Graphillion](https://github.com/takemaru/graphillion)
* [OpenTripPlanner](http://www.opentripplanner.org/) Good for public transportation routing. Can mix different transport modes, for example bike and bus. Used in HSL.
* [R5](https://github.com/conveyal/r5) Can handle all travel modes
* [A list with tools implementing different algorithms](https://gist.github.com/systemed/be2d6bb242d2fa497b5d93dcafe85f0c)

## Routing data sources for Finland
* OpenStreetMap, [GeoFabrik](https://download.geofabrik.de/europe/finland.html)
* [Digiroad](www.digiroad.fi) - Road data by Finnish Transport Agency
* [ESRI road and street network for Finland](https://avaa.tdata.fi/adata/esri/esri_stk.html), available for free for univeristies in CSC consortium. Based on Digiroad.
* Public transport data in [GTFS format](http://transitfeeds.com/l/530-finland)

