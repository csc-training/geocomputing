#!/bin/bash -l
#SBATCH --job-name=snap_array_job
#SBATCH --output=out_%A_%a.txt
#SBATCH --error=err_%A_%a.txt
#SBATCH --account=<YOUR-PROJECT>
#SBATCH --partition=small
#SBATCH --time=02:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=2000
#SBATCH --array=1-3

### Load SNAP module
module load snap

### For looping through all the files:

### Make a list of input files. This folder has 3 S2L2 images
readlink -f /appl/data/geo/sentinel/s2_example_data/S2* > image_path_list.txt

### Select the inputfile row by row
image_path=$(sed -n ${SLURM_ARRAY_TASK_ID}p image_path_list.txt)

### Parse image basename to be used in output filename
image_filename="$(basename -- $image_path)"

### -q is num of cores, -t is target file, -SsourceProduct is the xml inside each SAFE folder
gpt_array <PROJECT-SCRATCH-FOLDER>/tmp_snap_userdir_"$SLURM_ARRAY_TASK_ID" resample_and_lai.xml -q 4 -t <OUTPUT-FOLDER-HERE>/$image_filename_LAI.tif -SsourceProduct=$image_path/MTD_MSIL2A.xml
