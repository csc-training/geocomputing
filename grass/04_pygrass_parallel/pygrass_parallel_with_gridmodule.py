import grass.script as gscript
from grass.pygrass.modules.shortcuts import general as g
from grass.pygrass.modules.shortcuts import raster as r
from grass.pygrass.modules.shortcuts import vector as v
#from grass.pygrass.modules.shortcuts import temporal as t

from grass.pygrass.modules.grid import GridModule

file='/appl/data/geo/mml/dem10m/2019/W3/W33/W3331.tif'
grassfile='W3331'
grasscontoursfile='W3331_contours'
contoursfile="/scratch/project_2000599/grass/output/V4132.gpkg"
cpus=4

# Register external GeoTIFF in current mapset:
r.external(input=file,output=grassfile,flags="e",overwrite=True)

# Set GRASS region
g.region(raster=grassfile)

#Perform GRASS analysis, here calculate contours from DEM, parallelization with GridModule
region = gscript.region()
width = region['cols'] // 2 + 1
height = region['rows'] // 2 + 1
    
grd = GridModule('r.contour',
    width=width, height=height, overlap=20,
    processes=cpus, input=grassfile,
    output=grasscontoursfile, 
    minlevel=200, maxlevel=800, step=10, overwrite=True)    
grd.run()

#Write output to file
v.out_ogr(input=grasscontoursfile, output=contoursfile, overwrite=True)

# These can be left out, just debug info
print( "\n\n ***DEBUG INFO***")
print( "GRASS version")
print(g.version())

print("GRASS env settings: gisdatabase, location, mapset")
g.gisenv()

print("Available datasets:")
g.list(type="all", flags='m')

print("Input file info")
r.info(map=grassfile, verbose=True)

print("Output  info")
v.info(map=grasscontoursfile, verbose=True)