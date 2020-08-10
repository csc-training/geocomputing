Some of the functions in `raster` package support parallel computing. 

This example includes a **parallel job** using `predict()` funcion from `raster` package.  The precence/absence of R logo is predicted in an image. This type of model is often used to predict species distributions. See the dismo package for more of that.

The example is from https://www.rdocumentation.org/packages/raster/versions/2.5-8/topics/predict and it's 
simplified and adapted to be run thorugh batch job system in Puhti.

`r_run.sh` shows how to submit parallel R jobs to Puhti SLURM system.

For further details see comments in script. For general instructions on how to use R in Puhti see https://docs.csc.fi/apps/r-env-singularity/
