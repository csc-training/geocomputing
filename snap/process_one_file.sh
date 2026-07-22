#!/bin/bash

LINE="$1"

echo "$LINE"

# Everything before ; is input files
FILES="${LINE%;*}"
# After ; is the output file name
OUTPUT="${LINE#*;}"

echo "$FILES"
echo "$OUTPUT"

JOBID=$$

USERDIR="$TMPDIR/snap_user_${JOBID}"
#USERDIR="/scratch/project_2000599/tmp/snap_user_${JOBID}"

mkdir -p "$USERDIR"

gpt snap_graph_stacking.xml \
    -J-Dsnap.userdir="$USERDIR" \
    -PfileList="$FILES" \
    -PoutputFile="$OUTPUT" \
    -q  $SLURM_CPUS_PER_TASK -c 5G -J-Xmx14G -e

# Match values in gpt command with job reservation: 
# -q 2 with --cpus-per-task=2
# -J-Xmx55G with --mem=60000, use for job a few Gb less than reserved
# -c 40G with -J-Xmx55G, use ~75 % of available memory for data cache, depends on task..

#rm -r "$USERDIR"