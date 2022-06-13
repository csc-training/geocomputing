import arcpy
from arcpy.sa import *
import os

arcpy.env.overwriteOutput = True

directory = "./output/"

if not os.path.exists(directory):
    os.makedirs(directory)

outFlowDirection = FlowDirection("./dem.tif", "NORMAL")
outFlowDirection.save(directory+"flowdir.tif")
