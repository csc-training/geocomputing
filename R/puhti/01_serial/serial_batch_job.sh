#!/bin/bash
#SBATCH --account=project_2002044
#SBATCH --output=out.txt
#SBATCH --error=err.txt
#SBATCH --time=0:05:00
#SBATCH --partition=test
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=1000

module load r-env

# Clean up .Renviron file in home directory
if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
fi

# Specify a temp folder path
# echo "TMPDIR=/scratch/<project>/tmp" >> ~/.Renviron
echo "TMPDIR=$PWD/tmp" >> ~/.Renviron

srun apptainer_wrapper exec Rscript --no-save Contours_simple.R
