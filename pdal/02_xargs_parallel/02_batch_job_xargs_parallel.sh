#!/bin/bash -l
#SBATCH --account=project_200XXXX    # Choose the project to be billed
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --time=00:05:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=4  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem-per-cpu=1000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

module load python-geo

xargs -a ../filelist.txt -n1 -P4 sh -c '
    infile="$1"
    base=$(basename "$infile" .laz)
    pdal pipeline \
        --readers.las.filename="$infile" \
        --writers.gdal.filename="${base}.tif" \
        ../pipeline.json
' sh
