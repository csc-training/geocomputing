import numpy as np
import rasterio
import time
import os
from scipy import ndimage
import sys
import multiprocessing

def sliding_mean(array, kernel_size):
	kernel = np.ones((kernel_size,kernel_size))/(kernel_size*kernel_size)
	return ndimage.convolve(array,kernel, mode='constant', cval=-9999)

def save_output(array, file_name, transform, crs):
	if not os.path.isdir('smooth'):
		os.makedirs('smooth')	
	with rasterio.open(file_name, 'w', driver='GTiff',
				height=array.shape[0], width=array.shape[1],
				count=1, dtype='float32',
				crs=crs, transform=transform) as new_dataset:
		new_dataset.write(array,1)

# Multiprocessing worker function that takes a chunk out of our array and calculates sliding mean for that chunk. 
# Note that because of edge effects in sliding window mean we have to add overlap of kernel size to both ends of a chunk.
def worker(chunk, kernel_size, processes, res, i):
	C=sliding_mean(chunk, kernel_size)
	if i==0:
		res[i]=C[:-kernel_size]
	elif i==processes-1:
		res[i]=C[kernel_size:]
	else:
		res[i]=C[kernel_size:-kernel_size]

def main():
	file_name=sys.argv[1]
	with rasterio.open(file_name) as dataset:		
		myarray = dataset.read(1)
		kernel_size = 50		
		processes = 8 # here we should choose number of processes that allow as to divide our 1200 rows evenly
		chunk_length = len(myarray)/processes
		if processes*chunk_length != len(myarray):
			print "Not doing splitting into chunks properly, exiting"
			return

		# Create a manager list for results. Manager list ensures that we can write to the list from parallel 
		# processes without conflicts.
		man = multiprocessing.Manager()		
		res = man.list([None]*processes)

		#Create list to keep track of processes
		jobs = [None]*processes

		#start worker function for each chunk of our array in a separate process
		for i in xrange(0, processes):
			chunk = myarray[max(0,i*chunk_length-kernel_size):min((i+1)*chunk_length+kernel_size, len(myarray))]
			p = multiprocessing.Process(target=worker,args=(chunk, kernel_size, processes,res, i,))
			p.start()
			jobs[i]=p

		#wait that all jobs are finished and then concatenate results
		[job.join() for job in jobs]
		E = np.concatenate(res, axis=0)		
		save_output(E, os.path.join('smooth',os.path.basename(file_name)), dataset.affine, dataset.crs)

if __name__ == '__main__':
	t0 = time.time()
	main()
	t1 = time.time()
	total = t1-t0
	print "Everything done, took: ", str(total)+"s" 

