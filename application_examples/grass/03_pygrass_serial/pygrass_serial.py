from grass.pygrass.modules.shortcuts import general as g
from grass.pygrass.modules.shortcuts import raster as r
from grass.pygrass.modules.shortcuts import vector as v
#from grass.pygrass.modules.shortcuts import temporal as t

from grass.pygrass.modules.grid import GridModule

file='/appl/data/geo/mml/dem10m/2019/W3/W33/W3331.tif'
grassfile='W3331'
grasscontoursfile='W3331_contours'
contoursfile="/scratch/project_2000599/grass/output/V4132.gpkg"

# Register external GeoTIFF in current mapset:
r.external(input=file,output=grassfile,flags="e",overwrite=True)

# Set GRASS region
g.region(raster=grassfile)

# Perform GRASS analysis, here calculate contours from DEM
r.contour(input=grassfile, output=grasscontoursfile, minlevel=200, maxlevel=800, step=10, overwrite=True)

#Write output to file
v.out_ogr(input=grasscontoursfile, output=contoursfile, overwrite=True)

# These can be left out, just debug info
# TODO: not working properly!
print( "\n\n ***DEBUG INFO***")
print( "GRASS version")
print(g.version())

print("GRASS env settings: gisdatabase, location, mapset")
print(g.gisenv())

print("Available datasets:")
print(g.list(type="all", flags='m'))

print("Input file info")
print(r.info(map=grassfile, verbose=True))

print("Output  info")
print(v.info(map=grasscontoursfile, verbose=True))