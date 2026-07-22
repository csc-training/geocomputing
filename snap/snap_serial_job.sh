#!/bin/bash -l
#SBATCH --account=project_200XXXX    # Choose the project to be billed
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --time=00:03:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=2  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem=20000  # Real memory required per node.

module load snap

bash process_one_file.sh "/dataset/project_2019680/mml/dem10m/2019/M4/M42/M4231.tif,/dataset/project_2019680/luke/erosion_risk/2021/fields_10m/E_r_k_ls_c_bare_fallow_kgha_10m_cog.tif;M4231.tif"
