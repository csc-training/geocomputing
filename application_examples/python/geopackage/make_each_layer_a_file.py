#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 15:38:52 2018

@author: ekkylli

Code for saving all layers of GeoPackage as separate files
"""
import os
from osgeo import gdal, ogr

#OutputFolder
outFolder='layers'

#Check that the folder exists
if not os.path.exists(outFolder):
    os.makedirs(outFolder)

#Make error messages visible
gdal.UseExceptions() #Fail when can't open!
def gdal_error_handler(err_class, err_num, err_msg):
    errtype = {
            gdal.CE_None:'None',
            gdal.CE_Debug:'Debug',
            gdal.CE_Warning:'Warning',
            gdal.CE_Failure:'Failure',
            gdal.CE_Fatal:'Fatal'
    }
    err_msg = err_msg.replace('\n',' ')
    err_class = errtype.get(err_class, 'None')
    print ('Error Number: %s' % (err_num))
    print ('Error Type: %s' % (err_class))
    print ('Error Message: %s' % (err_msg))
 
 #Enable error handler    USE THIS FIRST TO SEE THE ERRORS, remove late for faster throughput
 #It seems that some field width warnings are given when actual data is ok.
#gdal.PushErrorHandler(gdal_error_handler)    
 
 #Disable error handler
#gdal.PopErrorHandler()
 
# Note, the original GeoPackage is opened with both ogr and gdal.
# TODO, it might not be necessary actually
ogrDS = ogr.Open('/appl/data/geo/mml/maastotietokanta/2020/gpkg/MTK-vakavesi_20-02-06.gpkg')
gdalDS = gdal.OpenEx('/appl/data/geo/mml/maastotietokanta/2020/gpkg/MTK-vakavesi_20-02-06.gpkg', gdal.OF_VECTOR)

# get a layer with GetLayer('layername'/layerindex)
for layer in ogrDS:
    
    # Generate the name for new file
    layerName = layer.GetName()
    print("Saving layer " + layerName)
    outFile=os.path.join(outFolder,layerName +'.gpkg')
    
    # Remove output shapefile if it already exists
    outDriver = ogr.GetDriverByName('GPKG')
    if os.path.exists(outFile):
        outDriver.DeleteDataSource(outFile)   
        
    #Save file with gdal, only one layer per file
    ds1 = gdal.VectorTranslate(outFile, gdalDS, layers = [layerName] , format = 'GPKG') 
    #Important, this is the way to save the file!
    del ds1       
