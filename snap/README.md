# SNAP GPT in Puhti

Examples:

* [Simple job with one GPT graph](simple_job). This example is S1 stacking with several input files.
* [Array job with one GPT graph for 3 images](array_job). This is an example of running the SNAP graph for multiple Sentinel-2 Level 3 images with an [array job](https://docs.csc.fi/computing/running/array-jobs/). It resamples the bands and calculates LAI (Leaf area index) for one image.


Both examples include 2 files:

* .xml-file - the SNAP Graph that defines the processing workflow.  
* .sh-file - the batch job script that makes resource (time, memory, cores) reservations to Puhti and starts the gpt command. The batch job file [is submitted to the Puhti queuing system](https://docs.csc.fi/computing/running/submitting-jobs/)

```
sbatch snap_batch_job.sh
OR
sbatch snap_array_job.sh
```