#!/bin/bash -l
#SBATCH --output=out_%A_%a.txt  # File to write the standard output to.
#SBATCH --error=err_%A_%a.txt  # File to write the standard error to.
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --time=02:00:00  # Maximum duration of the job. Upper limit depends on partition.  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=4  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem=8000  # Real memory required per node.
#SBATCH --array=1-3  # Indices to specify what array index values should be used. Multiple values may be specified using a comma separated list or a range of values separated by -.
#SBATCH --gres=nvme:10  # How much local disk to reserve. Default units are gigabytes. 

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