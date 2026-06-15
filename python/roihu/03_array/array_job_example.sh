#!/bin/bash
#SBATCH --account=project_2001659   # Choose the project to be billed
# SBATCH --reservation=geocomputing_day2 # Only available during the course
#SBATCH --time=00:05:00             # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1                  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=1           # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem-per-cpu=2G            # Minimum memory required per usable allocated CPU.  Default units are megabytes.
#SBATCH --partition=small           # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --array=1-3                 # Indices to specify what array index values should be used. Multiple values may be specified using a comma separated list or a range of values separated by -.

module load python-geo

# Select the inputfile from row n to the array job n.
file_path=$(sed -n ${SLURM_ARRAY_TASK_ID}p ../mapsheets_URLs.txt)

# Feed the filename to the Python script
srun python array_job_example.py $file_path
