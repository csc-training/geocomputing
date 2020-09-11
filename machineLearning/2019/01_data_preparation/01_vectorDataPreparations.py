
"""

This script prepares the PAAVO zip code dataset retrieved from Paituli (originally from the Statistics of Finland)
for machine learning purposes. It reads the original shapefile, scales all the numerical values, joins some auxiliary
data and encodes one text field for machine learning purposes. The result is saved as geopackage.

author: johannes.nyman@csc.fi
"""

import time
import geopandas as gpd
import pandas as pd
import os
from shapely.geometry import Point, MultiPolygon, Polygon
from sklearn.preprocessing import StandardScaler
from sklearn.externals.joblib import dump, load

### FILL HERE the path where your data is. e.g "/scratch/project_2000599/students/26/data"
#base_folder = "/home/cscuser/gis-ml/data/paavo"
base_folder = "/Users/jnyman/Documents/local/rndm/ml_course_DEV/test"

### Path to the input files. Zipcode level Paavo dataset with population statistics and the finnish regions (maakunta) shapefile
zip_code_shapefile = os.path.join(base_folder,"pno_tilasto_2020.shp")
finnish_regions_shapefile = os.path.join(base_folder,"SuomenMaakuntajako_2020_10k.shp")

### The output geopackage file of the data preparation script
output_file_path =  os.path.join(base_folder,"zip_code_data_after_preparation.gpkg")

### Settings for pandas so it agrees to print all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

def readZipcodesAndCleanData(zipcode_filepath):

    ### Read the data from a shapefile to a geopandas dataframe
    gdf = gpd.read_file(zipcode_filepath,encoding='utf-8')
    print("Original dataframe size: " + str(len(gdf.index))+ " zip codes with " + str(len(gdf.columns)) + " columns")
    
    ### Drop all rows that have missing values or where average income is -1 (=not known) or 0
    gdf = gdf.dropna()    
    gdf = gdf[gdf["hr_mtu"]>0].reset_index(drop=True)

    print("Dataframe size after dropping some rows: " + str(len(gdf.index))+ " zip codes with " + str(len(gdf.columns)) + " columns")

    ### Remove some columns that are strings (nanm, kunta = name of the municipality in Finnish and Swedish.
    ### or which might make the modeling too easy ('hr_mtu','hr_tuy','hr_pi_tul','hr_ke_tul','hr_hy_tul','hr_ovy')
    columns_to_be_removed_completely = ['namn','kunta','hr_ktu','hr_tuy','hr_pi_tul','hr_ke_tul','hr_hy_tul','hr_ovy']
    gdf = gdf.drop(columns_to_be_removed_completely,axis=1)
    print("Dataframe size after dropping some columns: " + str(len(gdf.index))+ " zip codes with " + str(len(gdf.columns)) + " columns")
    
    return gdf

def scaleNumericalColumns(original_gdf): 
    
    ### Get list of all column headings
    all_columns = list(original_gdf.columns)

    ### List the column names that we don't want to be scaled
    col_names_no_scaling = ['postinumer','nimi','hr_mtu','geometry']

    ### List of column names we want to scale. (all columns minus those we don't want)
    col_names_to_scaling = [column for column in all_columns if column not in col_names_no_scaling]

    ### Subset the data for only those to-be scaled
    gdf = original_gdf[col_names_to_scaling]

    ### Apply a Scikit StandardScaler for all the columns left in gdf
    scaler = StandardScaler()
    scaled_values_array = scaler.fit_transform(gdf)

    ### You can save the scaler for later use if you want
    dump(scaler, os.path.join(base_folder,'zip_code_scaler.bin'), compress=True)

    ### The scaled columns come back as a numpy ndarray, switch back to a geopandas dataframe again
    gdf = pd.DataFrame(scaled_values_array)
    gdf.columns = col_names_to_scaling

    ### Join the non-scaled columns back with the the scaled columns by index
    final_gdf = original_gdf[col_names_no_scaling].join(gdf)

    return final_gdf

def addAndEncodeCategoricalColumns(scaled_gdf,finnish_regions_shapefile):

    ###### Join spatially region (maakunta) name to every zip code

    ### Read the regions shapefile and choose only the name of the region and its geometry
    finnish_regions_gdf = gpd.read_file(finnish_regions_shapefile)
    finnish_regions_gdf = finnish_regions_gdf[['NAMEFIN','geometry']]

    ### A function we use to return centroid point geometry from a zip code polygon
    def returnPointGeometryFromXY(polygon_geometry):
        ## Calculate x and y of the centroid
        centroid_x,centroid_y = polygon_geometry.centroid.x,polygon_geometry.centroid.y
        ## Create a shapely Point geometry of the x and y coords
        point_geometry = Point(centroid_x,centroid_y)
        return point_geometry

    ### Stash the polygon geometry to another column as we are going to overwrite the 'geometry' with centroid geometry
    scaled_gdf['polygon_geometry'] = scaled_gdf['geometry']

    ### We will be joining the region name to zip codes according to the zip code centroid. 
    ### This calls the function above and returns centroid to every row
    scaled_gdf["geometry"] = scaled_gdf['geometry'].apply(returnPointGeometryFromXY)

    ### Spatially join the region name to the zip codes using the centroid of zip codes and region polygons
    scaled_gdf = gpd.sjoin(scaled_gdf,finnish_regions_gdf,how='inner',op='intersects')

    ### Switch the polygon geometry back to the 'geometry' field and drop uselesss columns
    scaled_gdf['geometry'] = scaled_gdf['polygon_geometry']
    scaled_gdf.drop(['index_right','polygon_geometry'],axis=1, inplace=True)

    ### Encode the region name with the One-hot encoding (= pandas dummy encoding) 
    ### method so machine learning can understand it better
    encoded_gdf = pd.get_dummies(scaled_gdf['NAMEFIN'])

    ### Join scaled gdf and encoded gdf together
    scaled_and_encoded_gdf = scaled_gdf.join(encoded_gdf).drop('NAMEFIN',axis=1)

    ### The resulting dataframe has Polygon and Multipolygon geometries. 
    ### This upcasts the polygons to multipolygon format so all of them have the same
    scaled_and_encoded_gdf["geometry"] = [MultiPolygon([feature]) if type(feature) == Polygon else feature for feature in scaled_and_encoded_gdf["geometry"]]
    print("Dataframe size after adding region name: " + str(len(scaled_and_encoded_gdf.index))+ " zip codes with " + str(len(scaled_and_encoded_gdf.columns)) + " columns")

    return scaled_and_encoded_gdf

def main():
    ### Read the data into a geopandas dataframe named original_gdf
    ### Drop unnecessary rows and colulmns
    original_gdf = readZipcodesAndCleanData(zip_code_shapefile)

    ### Scale numerical columns. 
    scaled_gdf = scaleNumericalColumns(original_gdf)
    
    ### Add region (maakunta) names and encode them as categorical values
    scaled_and_encoded_df = addAndEncodeCategoricalColumns(scaled_gdf,finnish_regions_shapefile)

    ### Write the prepared zipcode dataset to a geopackage
    scaled_and_encoded_df.to_file(output_file_path, driver="GPKG")


if __name__ == '__main__':
    ### This part just runs the main method and times it
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round(((end - start)),0)) + " seconds")
