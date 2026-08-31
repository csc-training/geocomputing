#!/bin/bash

# Read the input and output files from argument
LINE="$1"
# Everything before ; is input files
FILES="${LINE%;*}"
# After ; is the output file name
OUTPUT="${LINE#*;}"

# Set userdir, separate for each set of inputs.
# Each job in Roihu as by default 20 Gb space in $TMPDIR, if that is enough, use it. 
# Note that with `xargs` parallel case this 20 Gb is common for all jobs.
# If that is not enough, use scratch.
JOBID=$$
USERDIR="$TMPDIR/snap_user_${JOBID}"
#USERDIR="/scratch/project_2000599/tmp/snap_user_${JOBID}"
# Create the folder
mkdir -p "$USERDIR"

# Run the SNAP GPT graph
# -q 2 - how many cores to use for calculating one GPT graph. This depends on task and data, so test different values. Also 1 could be a good choice.
# -c 5G - tile cache size, depends on task..
# -J-Xmx55G - Java maximum heap memory
# -c and -J-Xmx55G together shoudl be less than memory reserved in the batch job.
gpt snap_graph_stacking.xml \
    -J-Dsnap.userdir="$USERDIR" \
    -PfileList="$FILES" \
    -PoutputFile="$OUTPUT" \
    -q  $SLURM_CPUS_PER_TASK \
    -c 5G \
    -J-Xmx14G -e

# If using scratch, delete the userdir as last step.
#rm -r "$USERDIR"
