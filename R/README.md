Examples for doing spatial analysis with **R** in CSC computing environment:

* [puhti](puhti) - examples for different job types in Puhti: simple serial, array and parallel: `snow`, `parallel` and `future`.
* [Working with Allas data from R](allas)
* [Reading NLS topographic database geopackage with R](geopackage)
* Some R packages have in-built support for parallization, for example `raster`, `terra` and `lidR`.
  * [raster](raster_predict) - Predicting precence/absence of some species using using `predict()` funcion from `raster` package. Some of the functions in `raster` package support parallel computing and `predict()` is one of these. Includes also the batch job (parallel) file for Puhti.
  * [R for LiDAR data](R_LiDAR) - examples and exercises
  * `terra` - just follow [terra manual](https://cran.r-project.org/web/packages/terra/terra.pdf), see for example predict example. For batch job file see `raster` package example.

References for CSC's R spatial tools:
* [Puhti's R for GIS documentation](https://docs.csc.fi/apps/r-env-for-gis/), at the end of page are several links to good learning materials about R for spatial data analysis.
* [Puhti's R documentation](https://docs.csc.fi/apps/r-env-singularity/)
