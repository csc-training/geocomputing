#!/bin/bash -l
#SBATCH --account=project_2002044
#SBATCH -J r_multi_proc
#SBATCH -o output_%j.txt
#SBATCH -e errors_%j.txt
#SBATCH -t 00:04:00
#Reserve cores for 1 master + 3 workers
#SBATCH --ntasks=4
#Test partition is for small test jobs only. For real jobs use either serial or parallel partition dependeing on how many nodes you need
#SBATCH -p test
#SBATCH --mem-per-cpu=1000

module load r-env

if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
fi

# Specify a temp folder path
# echo "TMPDIR=/scratch/<project>/tmp" >> ~/.Renviron
echo "TMPDIR=$PWD/tmp" >> ~/.Renviron

srun apptainer_wrapper exec RMPISNOW --no-save --slave -f Calc_contours_snow.R
