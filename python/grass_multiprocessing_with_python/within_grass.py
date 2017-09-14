#!/usr/bin/env python
#This script requires to be run from within grass in order to use grass.script
import copy
import sys
import time

#Importing grass.script requires grass session to be running.
import grass.script as gscript
from grass.pygrass.modules import Module, ParallelModuleQueue

def main():

    #create a list for parallel mapcalc modules and a mapcalc module to act as template 
    mapcalc_list = []
    mapcalc = Module("r.mapcalc", overwrite=True, run_=False)
    
    #get number of tiles in each row and col from arguments 
    tile_rows = int(sys.argv[1])
    tile_cols = int(sys.argv[2])
    
    #Create que for parallel processes
    queue = ParallelModuleQueue(nprocs=sys.argv[3])
    
    #Use temporary region that will be reset after execution of this script
    gscript.use_temp_region()
    
    input="input_raster"
    
    #Read raster boundaries and resolution into numeric variables
    info = gscript.raster_info(input)
    no = float(info['north'])
    so = float(info['south'])
    we = float(info['west'])
    ea = float(info['east'])
    ro = int(info['rows'])
    co = int(info['cols'])
    ewr = int(info['ewres'])
    nsr = int(info['nsres'])

    #Start mapcalc module for each tile
    k = 0
    for i in xrange(tile_rows):
        for j in xrange(tile_cols):
            #Set processing region to specific part of the raster (column+row)
            gscript.run_command('g.region', 
                    n=so+(i+1)*ro/tile_rows*nsr, 
                    s=so+i*ro/tile_rows*nsr, 
                    e=we+(1+j)*co/tile_cols*ewr, 
                    w=we+j*co/tile_cols*ewr, 
                    rows=ro/tile_rows, 
                    cols=co/tile_cols, 
                    nsres=nsr, 
                    ewres=ewr)
            #Create a copy of mapcalc template, give it mapcalc expression and put it into parallel que where it will be executed when a process becomes available.
            new_mapcalc = copy.deepcopy(mapcalc)
            mapcalc_list.append(new_mapcalc)
            m = new_mapcalc(expression="test_pygrass_%i = %s * (%i+1)"%(k,input, k))
            queue.put(m)
            k+=1
    #wait for all mapcalc modules to have finished execution
    queue.wait()

    #print mapcalc returncodes to check that everything went as expected
    for mapcalc in mapcalc_list:
        print(mapcalc.popen.returncode)

    #delete temporary region to restore the region that was in use at the start of the script
    gscript.del_temp_region()
    
if __name__ == '__main__':
    main()
