#!/bin/bash -l
# SBATCH --account <YOUR-PROJECT>
#SBATCH --account project_2001659
#Name of the job, this makes it easier to identify your job
#SBATCH -J lidR_batch_job
#output_%j.txt - Everything that would normally be printed into to the terminal when you run a program gets printed to this file. The %j refers to job number so that you don't overwrite the same file for each job
#SBATCH --output=batch_output_%j.txt  # File to write the standard output to.
#error_%j.txt - As above but for error messages. It's however always not so clear what messages go to errors and what to output so it's always best to check both.
#SBATCH --error=batch_error_%j.txt  # File to write the standard error to.
#Partition you want to submit your job to. 
#SBATCH -p test
#Time limit for the job in hh:mm:ss, Once this amount of time has passed the job will be terminated regardless of weather it has finished.
#SBATCH -t 00:10:00
#SBATCH --nodes=1  # Number of compute nodes. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#The number of cpus used by the lidR task, equal to number of workers. Max 40 in Puhti.
#SBATCH --cpus-per-task=5  # How many processors work on one task. Upper limit depends on number of CPUs per node.

#Tells the batch job sytem to reserve 8000MB (8GB) of memory for core
#SBATCH --mem-per-cpu=8000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

module load r-env-singularity

# If you have installed packages this helps resolve problems related to those
if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
    sed -i '/OMP_NUM_THREADS/d' ~/.Renviron   
fi

# Specify a temp folder path
echo "TMPDIR=/scratch/<YOUR-PROJECT>" >> ~/.Renviron

# Match thread number with set_lidr_threads(n) setting in the R-script
# echo "OMP_NUM_THREADS=2" >> ~/.Renviron

# Remove and creates new output folder
rm -rf batch_output_multicore
mkdir batch_output_multicore
srun singularity_wrapper exec Rscript --no-save simple_catalog_lidR_multicore.R
