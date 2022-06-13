#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 08:35:45 2018

@author: ekkylli

This file lists the layers of GeoPackage, the number of features in each layer an d their type.
"""

from osgeo import ogr

data = ogr.Open('/appl/data/geo/mml/maastotietokanta/2020/gpkg/MTK-vakavesi_20-02-06.gpkg')

print('Data Name:', data.GetName())

# get a layer with GetLayer('layername'/layerindex)
for layer in data:
    print('Layer Name:', layer.GetName())
    print('Layer Feature Count:', len(layer))
    
    layer_defn = layer.GetLayerDefn()
    for i in range(layer_defn.GetGeomFieldCount()):
        # some times the name doesn't appear
        # but the type codes are well defined
        print(layer_defn.GetGeomFieldDefn(i).GetName(), layer_defn.GetGeomFieldDefn(i).GetType())
        
        
        
