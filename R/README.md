Examples for doing spatial analysis with **R** in CSC computing environment:

* [puhti](puhti) - examples for different job types in Puhti: simple serial, array and parallel: `snow`, `parallel` and `future`.
* [Working with Allas data from R](allas)
* [Reading NLS topographic database geopackage with R](geopackage)
* [R for LiDAR data](R_LiDAR) - examples and exercises
* Some R packages have in-built support for parallization, for example `raster`, `terra` and `lidR`.
  * [raster](raster_predict) - includes also the batch job (parallel) file for Puhti.
  * [lidR](R_LiDAR/R_lidar_course_exercises)
  * `terra` - mainly follow [terra manual](https://cran.r-project.org/web/packages/terra/terra.pdf), see for example predict example. For batch job file see `raster` package example.
   *  With `terra` it is important to set memory settings manually, because by default it does not understand memory availability on supercomputers correctly. For example if reserving 8Gb memory from batch job, tell it also to `terra`. Adjust also used memory share, the default is 50%.

```
terraOptions(memmax=8)
terraOptions(memfrac=0.9)
```

References for CSC's R spatial tools:
* [Puhti's R for GIS documentation](https://docs.csc.fi/apps/r-env-for-gis/), at the end of page are several links to good learning materials about R for spatial data analysis.
* [Puhti's R documentation](https://docs.csc.fi/apps/r-env-singularity/)
