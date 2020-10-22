#!/bin/bash -l
#SBATCH --account <YOUR-PROJEC>
#Name of the job, this makes it easier to identify your job
#SBATCH -J lidR_batch_job
#output_%j.txt - Everything that would normally be printed into to the terminal when you run a program gets printed to this file. The %j refers to job number so that you don't overwrite the same file for each job
#SBATCH -o batch_output_%j.txt
#error_%j.txt - As above but for error messages. It's however always not so clear what messages go to errors and what to output so it's always best to check both.
#SBATCH -e batch_error_%j.txt
#Partition you want to submit your job to. Possible values are small, large, longrun, hugemem and test. 
#SBATCH -p small
#Time limit for the job in hh:mm:ss, Once this amount of time has passed the job will be terminated regardless of weather it has finished.
#SBATCH -t 00:15:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#The number of cpus used by the lidR task
#SBATCH --cpus-per-task=9

#Tells the batch job sytem to reserve 1000MB (1GB) of memory for core
#SBATCH --mem-per-cpu=2000

#As the job is not run on the login node where we submit the job from, it's necessary to load necessary modules in the batch job script. Loading the modules on the login node before sending the batch job will not help.
module load r-env-singularity

# If you have installed packages this helps resolve problems related to those
if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
fi

# Remove and creates new output folder
rm -rf batch_output
mkdir batch_output
srun singularity_wrapper exec Rscript --no-save simple_catalog_lidR.R

mv batch_output_$SLURM_JOBID.txt ./batch_output
mv batch_error_$SLURM_JOBID.txt ./batch_output
