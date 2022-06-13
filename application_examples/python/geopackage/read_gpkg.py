#!/usr/bin/python3
"""
Examples for reading data from NLS geopackage with geopandas, fiona and sqlite3. 
The geopackges are rather big, so reading the whole file might not be optimal. 
We can however read parts of it quickly without having to inspect each row as shown in examples below:
"""
import geopandas as gpd
import fiona
fn_muut= "/appl/data/geo/mml/maastotietokanta/2020/gpkg/MTK-muut_20-02-06.gpkg"
fn_suo = "/appl/data/geo/mml/maastotietokanta/2020/gpkg/MTK-suo_20-02-06.gpkg" 

"""
Reading a layer into a dataframe. Some layers are large, but for smaller layers this can be quick enough.
"""
def read_whole_layer():
    df=gpd.read_file(fn_muut, layer="hylky")
    print("Hylky:\n",df.head())

"""
Reading an area specified by a boundingbox from a single layer into a dataframe. 
Geopandas takes advantage of geopackage's spatial indexing and this is a fast operation even on large layers. 
For line and polygon geometries all features that at least intersect bounding box are selected.
"""
def read_area():

    bb=(374692, 6671989, 379750, 6676677)
    df=gpd.read_file(fn_suo, layer="suo", bbox=bb)
    print("\n\nSuo:\n",df.head())


"""
Reading rows in range 10-20. Again only the rows that we want will be read.
"""
def read_rows_in_range():
    c = fiona.open(fn_suo,layer="suo")
    start=10
    end=20
    df=gpd.GeoDataFrame.from_features(c[start:end])
    print(df)

"""
Reading specific rows. As above but for specific row numbers rather than a range of rows.
"""
def read_specific_rows():
    with fiona.open(fn_suo,layer="suo") as c:
        rows = (1,5,100)
        df=gpd.GeoDataFrame.from_features([c[i] for i in rows])
        print(df)
        
"""
Reading rows where an attribute has a certain value (or based on any SQL query).
Fiona and thus geopandas don't support reading only specifc rows based on an attribute. However if you really need to be able to do this fast you can do it by first creating an index for the column you want to use and then using sqlite to get numbers of rows you need. After this you can create dataframe as above. This method can of course be used to run any SQL query to first select IDs of the rows that we want before reading the data into memory. Weather these queries need to actually inspect each row or if faster execution is possible depends on the query and the indexes available. The main benefit here is that you can take advantage of additional indexes and you don't need to first read all the rows into geopandas dataframe.
Geopandas also specifies read_postgis() method that you can use to accomplish the same end result, but using this with geopackage creates a need for some geometry type conversions that can be problematic.
"""

import sqlite3
def create_index():
    table="suo"
    col="mtk_id"
    conn = sqlite3.connect(fn)
    c = conn.cursor()
    sql="CREATE INDEX index_{}_{} ON {} ({})".format(table, col, table, col)
    c.execute(sql)
    conn.commit()
    conn.close()

def read_by_attribute():
    conn = sqlite3.connect(fn)
    c = conn.cursor()
    layer="suo"
    attribute_col="mtk_id"
    attribute_val=219920480
    id_col = 'fid'
    sql="select {} from {} where {}={}".format(id_col, layer, attribute_col, attribute_val)
    c.execute(sql)
    rows = c.fetchall()
    rows = [r[0] for r in rows]
    print(rows)
    with fiona.open(fn,layer="suo") as c:
        df=gpd.GeoDataFrame.from_features([c[i] for i in rows])
        print(df)

if __name__=='__main__':
    read_whole_layer()
    read_specific_rows()
    read_rows_in_range()
    read_area()    
    
