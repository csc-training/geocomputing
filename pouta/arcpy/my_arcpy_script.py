import arcpy
from arcpy.sa import *
import os

arcpy.env.overwriteOutput = True

directory = "/home/cloud-user/output/"

if not os.path.exists(directory):
    os.makedirs(directory)

outFlowDirection = FlowDirection("/home/cloud-user/data/dem.tif", "NORMAL")
outFlowDirection.save(directory+"flowdir.tif")
