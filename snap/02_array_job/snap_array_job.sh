#!/bin/bash -l
#SBATCH --output=out_%A_%a.txt
#SBATCH --error=err_%A_%a.txt
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --partition=small
#SBATCH --time=02:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8000
#SBATCH --array=1-3
#SBATCH --gres=nvme:10

### Load SNAP module
module load snap

### For looping through all the files:

### Make a list of input files. This folder has 3 S2L2 images
readlink -f /appl/data/geo/sentinel/s2_example_data/L2A/S2* > image_path_list.txt

### Select the inputfile row by row
image_path=$(sed -n ${SLURM_ARRAY_TASK_ID}p image_path_list.txt)

### Parse image basename to be used in output filename
image_filename="$(basename -- $image_path)"

### Assign an output_folder
output_folder=/scratch/project_2000599/snap/output/

# Set custom SNAP user dir
source snap_add_userdir $LOCAL_SCRATCH/cache_"$SLURM_ARRAY_TASK_ID"

### -q is num of cores, -t is target file, -SsourceProduct is the xml inside each SAFE folder
gpt resample_and_lai.xml -q 4 -c 5G -J-Xmx7G -t ${output_folder}/${image_filename}_LAI.tif -SsourceProduct=${image_path}/MTD_MSIL2A.xml -e

# Match values in gpt command with job reservation: 
# -q 4 with --cpus-per-task=4
# -J-Xmx7G with --mem=8000, use for job a few Gb less than reserved
# -c 5G with -J-Xmx7G, use ~75 % of available memory for data cache, depends on task..