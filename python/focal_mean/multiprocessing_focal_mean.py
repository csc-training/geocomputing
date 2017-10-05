import numpy as np
import multiprocessing
from scipy import ndimage	
import rasterio
from functools import partial
import sys

#Applies a focal function (such as sliding mean) to an array
def apply_focal(kernel, array):
	return ndimage.convolve(array,kernel, mode='constant', cval=-9999)

# Splits data into number of chunks defined in the chunks parameter, with amount of overlap defined in the margin parameter.
# returns a list containing the chunks.
def split_data(data, margin, chunks):
	if chunks==1:
		return [data]
	rows = np.shape(data)[0]
	chunk_size= rows/chunks
	return [data[max(0, chunk_size*p-margin):min(rows,chunk_size*(p+1)+margin)] for p in xrange(chunks)]

#Crops the margin from the split chunks and concatenates them back to single 2d array (reverse of split_data)
def crop_result(result, margin):
	if len(result)==1:
		return result[0]
	result = [
		result[i][:-margin] if i==0 
		else result[i][margin:] if i==len(result)-1  
		else result[i][margin:-margin]  
		for i in xrange(len(result))]
	return np.concatenate(result, axis=0)	


#Save output array as geotiff file in folder called "high_low".
def save_output(array, file_name, transform, crs):
	if not os.path.isdir('high_low'):
		os.makedirs('high_low')	
	with rasterio.open(file_name, 'w', driver='GTiff',
				height=array.shape[0], width=array.shape[1],
				count=1, dtype='float32',
				crs=crs, transform=transform) as new_dataset:
		new_dataset.write(array,1)
def main():

	# 1. Read input tif with rasterio in read mode.
	file_name=sys.argv[1]
	output_name="high_low.tif"
	with rasterio.open(file_name, 'r') as dataset:		
		data = dataset.read(1)

		# 2. Create a kernel with equal weight in each cell and cell weights summing up to 1. 
		kernel_size = 81
		kernel = np.ones((kernel_size,kernel_size))/(kernel_size*kernel_size)
	
		# 3. Split the data for example into 4 parts using split_data function provided
		procs = 1
		margin = kernel_size/2
		chunks = split_data(data, margin, procs)

		# 4. Create a Pool with as many processes as you split your data into and map apply_focal function to your chunks.
		pool = multiprocessing.Pool(processes=procs)
		func = partial(apply_focal, kernel)		
		result = pool.map(func, chunks, chunksize=1)
	
		result = crop_result(result, margin)
		high_low = data-result			

		# 7. Write output to raster file using rasterio. 
		save_output(high_low, os.path.join('high_low',os.path.basename(file_name)), dataset.affine, dataset.crs)

if __name__ == '__main__':
	main()
