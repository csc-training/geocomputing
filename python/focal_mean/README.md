## Overview
In this example we'll read a geotiff image and blur it using sliding mean. We'll first run the script for a single file using Taito's batch job system and then take a look on how to process multiple files in parallel using array jobs in Taito. Lastly we'll process a single image in multiple parts using multiprocessing python package.

There are two python scripts in this folder: simple\_folcal\_mean.py and multiprocessing\_focal\_mean.py The first uses a single process to blur the image while the latter splits the image into chunks and processes those in parallel.

There are also three .sh files called batch\_job\_simple.sh, array\_job.sh and batch\_job\_multiprocessing.sh These files are used to submit batch jobs to Taito.

## Simple focal mean python script
The first script is fairly straightforward. It uses rasterio to open the georeferenced image (could be anything supported by GDAL including virtual raster) as numpy array and then uses scipy's ndimage.convolve to apply the focal mean function. In this example we'll just fill the image edges wiht nodata value where focal mean can't be computed. Lastly rasterio is used again to save output to folder 'smooth'. It's worth noting that rather than hardcoding the filename into to script we supply it as argument using sys.argv. This allows us to use the same python script in the next step when we want to process multiple files using array jobs.

## Simple batch job file

A more detailed documentation on batch job system can be found here: https://research.csc.fi/taito-batch-jobs

In the batch job file batch\_job\_simple.sh we define where the output and error messages are written as well as computing resources assigned for our program. In this case 5 seconds of execution time on once cpu and 1mb of memory is plenty.

Batch job can then be submitted with command sbatch batch\_job\_simple.sh. This will also give us a job id which we can use to check state and efficiency of our batch job with seff <jobid>

Once the job is finished we can see output in out.txt and any possible errors in err.txt

## Array jobs and python gis in Taito
Array jobs are an easy way of taking advantage of taitos parallel processing capabilities. For more detailed instructions on array jobs see: https://research.csc.fi/taito-array-jobs#3.5.2

Array jobs are useful when same code is executed many times for different datasets or with different parameters. In GIS context a typical use would be to run some model on study area split into multiple files where output from one file doesn't have an impact on result of an other area. In this example we can use the script from previous exercies without any further modifications to blur several images at the same time.

## Using arrayjobs to smooth multiple files
Because we supplied the input filename as an argument to our python script we can easily construct an arrayjob file to process multiple files at the same time. We give list of files to be processed as parameter to the array job file and when we submit the arrayjob a new job is submitted for each file in the file list. 

--array parameter is used to tell how many jobs we want to start. Value 1-2 in this case means we will have $SULRM\_ARRAY\_TASK\_ID variable running from 1 to 2, which means we will use sed to read first two lines from our input file list and start jobs for those files. If we want to process all files in the file list we should set --array=1-<number of lines>

Output from each job is written to array\_job\_out\_<array\_job\_id>.txt and array\_job\_err\_<array\_job\_id>.txt files. Memory and time allocations are per job, so we don't have to modify them from last example.

we can then submit this array job file with:
sbatch array\_job.sh file\_list.txt

## Using multiprocessing library
In last example we were able to use array jobs to process 2 files basically in the same time it took to process just one file in the first exmple because we had 2 separate files to process at the same time. In cases where we are just going to run a script once on a single file (that can be large) this isn't going to speed thigns up. If we wan't to utilize Taito's parallel processing capabilities in these cases and to process each file faster we will have to  write our code to utilize parallel processing. We can do this pretty easily using pythons multiprocessing library that allows us to run our code in parallel processes.

Idea behind our modified python script is to split our numpy array that we read from a source raster into even sized chunks that we can process individually and once each chunk has been computed we combine results. We can then submit this python script using either batch\_job script from the first example (single file) or array\_job script from second example (multiple files). The only modification we need to do to our batch job files is to increase number of --cpus-per-task variable to match the number of processes we used in our python script.

It is worth noting that our script at least in this case gets a bit more complicated when multiprocessing is introduced and it might be worthwile option to consider just splitting our data to smaller files and then process them using arrayjobs. On the other hand if our source data didn't have any overlap between files it might be simpler to create a virtual raster and process that using multiprocessing, otherwise we would have to somehow handle edge effects between each file which would also result in additional coding.
