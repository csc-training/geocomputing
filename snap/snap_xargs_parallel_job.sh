#!/bin/bash -l
#SBATCH --account=project_200XXXX    # Choose the project to be billed
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --time=00:10:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=4  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=2  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem=80000  # Memory required per job.

module load snap
cat filelist.csv | xargs -I {} -P $SLURM_NTASKS bash process_one_file.sh "{}"
