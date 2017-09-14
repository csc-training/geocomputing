import numpy as np
import rasterio
import time
import os
from scipy import ndimage
import sys


def sliding_mean(array, kernel_size):
	#create a kernel with each cell value being 1/<number of cells in kernel> which results in mean from kernel area being assigned to each cell, Any other kernel of user's choosing could be used as well.
	kernel = np.ones((kernel_size,kernel_size))/(kernel_size*kernel_size)
	return ndimage.convolve(array,kernel, mode='constant', cval=-9999)

#Save output array as geotiff file in folder called "smooth".
def save_output(array, file_name, transform, crs):
	if not os.path.isdir('smooth'):
		os.makedirs('smooth')	
	with rasterio.open(file_name, 'w', driver='GTiff',
				height=array.shape[0], width=array.shape[1],
				count=1, dtype='float32',
				crs=crs, transform=transform) as new_dataset:
		new_dataset.write(array,1)
	
def main():
	#input file
	file_name=sys.argv[1]
	with rasterio.open(file_name) as dataset:
		myarray = dataset.read(1)
		kernel_size = 50
		blurred = sliding_mean(myarray, kernel_size)
		save_output(blurred, os.path.join('smooth',os.path.basename(file_name)), dataset.affine, dataset.crs)

if __name__ == '__main__':
	t0 = time.time()
	main()
	t1 = time.time()
	total = t1-t0
	print "Everything done, took: ", str(total)+"s" 

