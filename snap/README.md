# Array jobs and SNAP
This is an example of running a SNAP graph for multiple Sentinel-2 Level 2 images with an array job in Puhti supercomputer

# Contents

## resample_and_lai.xml

This file is the SNAP Graph that dictates the processes that will be computed for each image. In this example it resamples the bands and calculates LAI (Leaf area index) for each image

More information on creating SNAP graphs

*[Creating a GPF Graph](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/70503590/Creating+a+GPF+Graph)
*[Bulk Processing with GPT command](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/70503475/Bulk+Processing+with+GPT)


## snap_array_job.sh

This is the batch job script that is submitted to the Puhti queuing system. It creates a list of all the Sentinel SAFE-folder paths, spawns jobs for each of them (3) and runs the gpt_array command for each SAFE-folder path.

**gpt_array** command is a slightly modified version of the gpt-command. It makes sure that when several SNAP jobs are running at the same time, they don't use the same cache folder for temporary files. If you're using array jobs, use gpt_array rather than gpt 
