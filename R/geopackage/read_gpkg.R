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
# The read_sf function takes a query= parameter that allows us to specify an sql query to select only some parts of data. 
# This can be used in several ways:

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


read_whole_layer()
read_specific_rows()
read_rows_in_range()


