# Examples on reading data from NLS geopackages with sf. 
# The geopackges are quite large files so reading the whole thing takes a while. 
# We can however read parts of it quickly without having to inspect each row as shown in below examples. 
# Requires sf 0.7

library(sf)
fn_suo<-"/proj/ogiir-csc/mml/maastotietokanta/2019/MTK-suo_19-01-23.gpkg"
fn_muut<-"/proj/ogiir-csc/mml/maastotietokanta/2019/MTK-muut_19-01-23.gpkg"
#Reading a layer into a dataframe. Some layers are large, but for smaller layers this can be quick enough.
read_whole_layer <- function(){
    layer="hylky"    
    df<-read_sf(fn_muut, layer)
    print(df)
}

# Geopackage is internally an sqlite database which can be connected to and queried. 
# The read_sf function takes a query= parameter that allows us to specify an SQL query to select only some parts of data. 
# The given SQL is handled by OGR, so see https://www.gdal.org/ogr_sql.html for available further details.
# Basically selection based on any attribute is possible, but selection by geometry does not seem to be possible.

# SQL selections can be used in several ways:

# Reading rows in range 10-20. Only the rows that we want will be read regardless of the actual number of rows in the layer.
read_rows_in_range <- function(){
    layer<-"suo"
    start <- 10
    end <- 20
    sql <- sprintf("select * from %s where rowid >= %s and rowid < %s",layer, start, end)
    df<-read_sf(fn_suo, layer=layer, query=sql)
    print(df)
}

#As above but for specific rows
read_specific_rows <- function(){
    layer<-"suo"
    rows<-c(1,5,100)
    sql <- sprintf("select * from %s where rowid in (%s)",layer, paste(rows, collapse=", "))
    print(sql)
    df<-read_sf(fn_suo, layer=layer, query=sql)
    print(df)
}


#We can use the query parameter to ask rows based on any attribute not just rowid. This may however be slow depending on number of rows and indexes available in the geopackage. If the column you want to use is not indexed you can create the index as follows
create_index <- function(){
    layer<-"suo"
    attr_col<-"mtk_id"
    attr_value<-219920480
    con <- dbConnect(RSQLite::SQLite(), fn)
    res<-dbSendQuery(con, sprintf("CREATE INDEX index_%s_%s ON %s (%s)",layer, attr_col, layer, attr_col))	
    dbClearResult(res)    
    dbDisconnect(con)
}

#After this you can quickly query the layer based on the column.
read_by_attribute <- function(){
    layer<-"suo"
    attr_col<-"mtk_id"
    attr_value<-219920480
    
    sql <- sprintf("select * from %s where %s=%s", layer, attr_col, attr_value)
    df<-read_sf(fn,layer=layer, query=sql)
    print(df)

}


#If we want to query based on a bounding box efficiently we need to be able to take advantage of spatial indexing. The NLS Geopackage includes a spatial index for each layer already so we don't have to worry about creating it. Depending on how your version of GDAL has been compiled we still may need to enable spatilite extension to be able to take advantage of the indexing (=use RTreeIntersects function). To do this first open connection to the geopackage, enable spatialite extension and then supply that connection to read_sf rather than the filename. You can also try to just supply the filename to read_sf function and skip enabling spatialite as this may also work. 

read_area <- function(){
    con <- dbConnect(RSQLite::SQLite(), fn)
    
    #Linux:    
    res<-dbSendQuery(con, "select load_extension('libspatialite.so')")
    #Windows:    
    #res<-dbSendQuery(con, "select load_extension('libspatialite.dll')")    
    
    dbClearResult(res)    
    bb<-c(374692, 6671989, 379750, 6676677)
    layer<-"suo"
    geom_col<-"sijainti_alue"
    sql <- sprintf("select * from %s where rowid in (select id from rtree_%s_%s where id match RTreeIntersects(%s,%s,%s,%s))",layer, layer, geom_col, bb[1],bb[2],bb[3],bb[4])
    df<-read_sf(con, query=sql)
    dbDisconnect(con)
    print(df)
}


