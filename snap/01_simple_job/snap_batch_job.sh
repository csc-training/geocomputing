#!/bin/bash -l
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --time=04:00:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=2  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem=60000  # Real memory required per node.
#SBATCH --gres=nvme:50  # How much local disk to reserve. Default units are gigabytes. 

#The last row resrves 50G of local fast disk on the compute node, it will be used for SNAP and JAVA cache, set by snap_add_userdir.

module load snap
source snap_add_userdir $LOCAL_SCRATCH
gpt /scratch/project_200XXXX/scripts/CreateStackGraph.xml -q 2 -c 40G -J-Xmx55G -e

# Match values in gpt command with job reservation: 
# -q 2 with --cpus-per-task=2
# -J-Xmx55G with --mem=60000, use for job a few Gb less than reserved
# -c 40G with -J-Xmx55G, use ~75 % of available memory for data cache, depends on task..