#!/bin/bash
#SBATCH --account=project_20xxxxx   # Choose the project to be billed
# SBATCH --reservation=geocomputing_thu # Only available during the course
#SBATCH --output=slurm-%j.out       # File to write the standard output to. %j is replaced by the job ID.
#SBATCH --error=slurm-%j.err        # File to write the standard error to. %j is replaced by the job ID. Defaults to slurm-%j.out if not provided. 
#SBATCH --time=00:05:00             # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1                  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=1           # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem-per-cpu=2G            # Minimum memory required per usable allocated CPU.  Default units are megabytes.
#SBATCH --partition=small            # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

module load geoconda

data_folder=/appl/data/geo/sentinel/s2_example_data/L2A/

srun python single_core_example_folder.py $data_folder
