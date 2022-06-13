import grass.script as gscript
import grass.script as gcore
import pprint

import json

file='/appl/data/geo/mml/dem10m/2019/W3/W33/W3331.tif'
grassfile='W3331'
grasscontoursfile='W3331_contours'
contoursfile="/scratch/project_2000599/grass/output/V4132.gpkg"

# Register external GeoTIFF in current mapset:
gscript.parse_command("r.external", input=file,output=grassfile,flags="e",overwrite=True)

# Set GRASS region
gscript.run_command('g.region', rast=grassfile)

# Perform GRASS analysis, here calculate contours from DEM
gscript.run_command('r.contour', input=grassfile, output=grasscontoursfile, minlevel=200, maxlevel=800, step=10, overwrite=True)

#Write output to file
gscript.run_command('v.out.ogr', input=grasscontoursfile, output=contoursfile, overwrite=True)

# These can be left out, just debug info
# TODO: not working properly!
print( "\n\n ***DEBUG INFO***")
print( "GRASS version")
print(gscript.read_command("g.version"))

print("\nGRASS env settings: gisdatabase, location, mapset")
print(gscript.read_command("g.gisenv", flags="s"))

print("\nAvailable datasets:")
print(gscript.read_command("g.list", type="all", flags='m'))

print("\nInput file info")
print(gscript.read_command("r.info", map=grassfile, flags='g'))

print("\nOutput  info")
print(gscript.read_command("v.info", map=grasscontoursfile, flags='g'))