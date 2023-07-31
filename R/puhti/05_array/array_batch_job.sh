#!/bin/bash
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --output=slurm-%A_%a.out  # File to write the standard output to. %A is replaced by the job ID and %a with the array index.
#SBATCH --error=slurm-%A_%a.err  # File to write the standard error to. %A is replaced by the job ID and %a with the array index. Defaults to slurm-%A_%a.out if not provided.
#SBATCH --time=00:02:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --mem-per-cpu=1000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.
#SBATCH --array=1-3  # Indices to specify what array index values should be used. Multiple values may be specified using a comma separated list or a range of values separated by -.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

# load the Puhti module for R
module load r-env

if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
fi

# Specify a temp folder path
# echo "TMPDIR=/scratch/<project>/tmp" >> ~/.Renviron
echo "TMPDIR=$PWD/tmp" >> ~/.Renviron

# read the file that has filepaths for mapsheets and pick one row according to variable $SLURM_ARRAY_TASK_ID
name=$(sed -n "$SLURM_ARRAY_TASK_ID"p ../mapsheets.txt)

# run the analysis command
srun apptainer_wrapper exec Rscript Contours_array.R $name
