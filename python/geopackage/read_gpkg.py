#!/usr/bin/python3
"""
Examples on reading data from NLS geopackage with geopandas, fiona and sqlite3. The geopackge is nearly 80GB so reading the whole thing takes a while. We can however read parts of it quickly without having to inspect each row as shown in below examples:
"""
import geopandas as gpd
import fiona
fn_muut= "/proj/ogiir-csc/mml/maastotietokanta/2019/MTK-muut_19-01-23.gpkg"
fn_suo = "/proj/ogiir-csc/mml/maastotietokanta/2019/MTK-suo_19-01-23.gpkg" 

"""
Reading a layer into a dataframe. Some layers are large, but for smaller layers this can be quick enough.
"""
def read_whole_layer():
    df=gpd.read_file(fn_muut, layer="hylky")
    print("Hylky:\n",df.head())

"""
Reading an area specified by a boundingbox from a single layer into a dataframe. Geopandas takes advantage of geopackage's spatial indexing and this is a fast operation even on large layers. For line and polygon geometries all features that at least intersect bounding box are selected.
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

if __name__=='__main__':
    read_whole_layer()
    read_specific_rows()
    read_rows_in_range()
    read_area()    
    
