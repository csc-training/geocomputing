#!/bin/bash -l
#SBATCH --account=project_2002044
#SBATCH -J r_multi_proc
#SBATCH --output output.txt
#SBATCH --error errors.txt
#SBATCH -t 00:05:00
#SBATCH --ntasks=3
#Test partition is used for testing, for real jobs use either serial or parallel depending on how many nodes you need.
#SBATCH -p test
#SBATCH --mem-per-cpu=1000

module load r-env

if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
fi

# Specify a temp folder path
# echo "TMPDIR=/scratch/<project>/tmp" >> ~/.Renviron
echo "TMPDIR=$PWD/tmp" >> ~/.Renviron

srun apptainer_wrapper exec Rscript --no-save --slave Calc_contours_foreach.R
