#!/bin/bash
#SBATCH --output=slurm-%A_%a.out    # File to write the standard output to. %A is replaced by the job ID and %a with the array index.
#SBATCH --error=slurm-%A_%a.err     # File to write the standard error to. %A is replaced by the job ID and %a with the array index. Defaults to slurm-%A_%a.out if not provided.
#SBATCH --account=project_200xxxx   # Choose the project to be billed
#SBATCH --time=00:05:00             # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1                  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=1           # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem-per-cpu=4G            # Minimum memory required per usable allocated CPU.  Default units are megabytes.
#SBATCH --partition=small           # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --array=1-3                 # Indices to specify what array index values should be used. Multiple values may be specified using a comma separated list or a range of values separated by -.

module load geoconda

# For looping through all the files:

# Make a list of input files
readlink -f /appl/data/geo/sentinel/s2_example_data/L2A/S2* > image_path_list.txt

# Select the inputfile from row n to the array job n.
image_path=$(sed -n ${SLURM_ARRAY_TASK_ID}p image_path_list.txt)

# Feed the filename to the Python script
srun python array_job_example.py $image_path
