#!/bin/bash
#SBATCH --account=<YOUR-PROJECT>
#SBATCH -J rspatial_job
#SBATCH -o out.txt
#SBATCH -e err.txt
#SBATCH -t 0:05:00
#SBATCH -p test
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=1000

module load r-env-singularity

if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
fi

# Specify a temp folder path
echo "TMPDIR=/scratch/<project>" >> ~/.Renviron

srun singularity_wrapper exec Rscript --no-save Contours_simple.R
