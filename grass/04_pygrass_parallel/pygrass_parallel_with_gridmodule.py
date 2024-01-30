import grass.script as gscript
from grass.pygrass.modules.shortcuts import general as g
from grass.pygrass.modules.shortcuts import raster as r
from grass.pygrass.modules.shortcuts import vector as v
#from grass.pygrass.modules.shortcuts import temporal as t

from grass.pygrass.modules.grid import GridModule

file='/appl/data/geo/mml/dem10m/2019/W3/W33/W3331.tif'
grassfile='W3331'
grasscontoursfile='W3331_contours'
aspectfile="/scratch/project_2000599/grass/output/aspect.tif"
cpus=4

# Register external GeoTIFF in current mapset:
r.external(input=file,output=grassfile,flags="e",overwrite=True)

# Set GRASS region
g.region(raster=grassfile)

#Perform GRASS analysis, here calculate contours from DEM, parallelization with GridModule
region = gscript.region()
width = region['cols'] // 2 + 1
height = region['rows'] // 2 + 1

grd = GridModule('r.slope.aspect',
    width=width, height=height, overlap=2,
    processes=cpus, split=False,
    elevation=grassfile,
    aspect='aspect', overwrite=True)
grd.run()
    
# grd = GridModule('r.contour',
    # width=width, height=height, overlap=20,
    # processes=cpus, input=grassfile,
    # output=grasscontoursfile, 
    # minlevel=200, maxlevel=800, step=10, overwrite=True)    
# grd.run()

#Write output to file
r.out_gdal(input='aspect', output=aspectfile, overwrite=True)
#r.out_ogr(input=grasscontoursfile, output=outfile, overwrite=True)

# These can be left out, just debug info
g.version()
g.gisenv()
g.list(type="all", flags='m')
r.info(map=grassfile, verbose=True)
v.info(map=grasscontoursfile, verbose=True)
