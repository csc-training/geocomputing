#!/bin/bash -l
#SBATCH --account=project_2002044
#SBATCH --job-name=r_multi_proc
#SBATCH --output=output.txt
#SBATCH --error=errors.txt
#SBATCH --time=00:05:00
#SBATCH --ntasks=1
#SBATCH --partition test
#SBATCH --mem-per-cpu=1000
#Equal to number of workers. Max 40 in Puhti.
#SBATCH --cpus-per-task=3

module load r-env

# If you have installed packages this helps resolve problems related to those
if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
    sed -i '/OMP_NUM_THREADS/d' ~/.Renviron   
fi

# Specify a temp folder path
# echo "TMPDIR=/scratch/<project>/tmp" >> ~/.Renviron
echo "TMPDIR=$PWD/tmp" >> ~/.Renviron

srun apptainer_wrapper exec Rscript --no-save Calc_contours_future_multicore.R
