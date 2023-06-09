# STAC R examples

The [STAC](https://stacspec.org/en/) is a specification to describe geospatial information, so it can easily **searched and downloaded**. 
STAC includes metadata of datasets and links to actual files, the data files are usually stored in the cloud. See [Paituli STAC page](https://paituli.csc.fi/stac.html) for general introduction about STAC and what Collections (=datasets) are included in Paituli STAC.

In this repository we provide examples to work with:

* [Paituli STAC API](STAC_CSC_example.R)
* See, also similar [Python STAC examples](../../python/STAC)

The examples mainly cover data search and download, using [rstac](https://cran.r-project.org/web/packages/rstac/index.html). For analyzing data [gdalcubes](https://gdalcubes.github.io/) or [terra](https://cran.r-project.org/web/packages/terra/index.html) can be used.  When working with bigger datasts, gdalcubes supports also parallelization.

The examples can be run on any computer with R installation. The required R packages can be seen from the beginning of the example scripts. The examples download all data from cloud storage, so relatively good internet connection is needed.

In CSC Puhti supercomputer, the examples can be run with [r-env module](https://docs.csc.fi/apps/r-env/), which includes all necessary R packages. The easiest is to use RStudio with Puhti web interface:

* Open [Puhti web interface](https://www.puhti.csc.fi/)
* Click "RStudio" on dashboard
* Select following settings:
	* Project: project_2002044 during course, own project otherwise 
	* Partition: interactive
	* Number of CPU cores: 1
	* Memory (Gb): 8 
	* Local disk (GB): 0
	* Time: 1:00:00 (or adjust to reasonable)
* Click launch and wait until granted resources 
* Click "Connect to RStudio Server" 