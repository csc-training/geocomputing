# STAC Python examples

The [STAC](https://stacspec.org/en/) is a specification to describe geospatial information, so it can easily **searched and downloaded**. 
STAC includes metadata of datasets and links to actual files, the data files are usually stored in the cloud. See [Paituli STAC page](https://paituli.csc.fi/stac.html) for general introduction about STAC and what Collections (=datasets) are included in Paituli STAC.

In this repository we provide examples to work with:

* STAC API:
    * [Paituli STAC API](STAC_CSC_example.ipynb)
    * [Element84 STAC API](stac_xarray_dask_example.ipynb)
* Static STAC: 
    * [FMI STAC](static_stac.ipynb)

The examples mainly cover data search and download, for analyzing data [xarray](https://docs.xarray.dev/en/stable/) and [xarray-spatial](https://xarray-spatial.org/) can be used. If unfamiliar with xarray, [Pangeo 101](https://pangeo-data.github.io/foss4g-2022/intro.html) is one option to get started. When working with bigger datasts, xarray supports also parallelization with [dask](https://www.dask.org/).

The examples can be run on any computer with Python installation, the required Python packages can be seen from beginning of the notebooks. The examples download all data from cloud storage, so relatively good internet connection is needed.

In CSC Puhti supercomputer, the notebooks can be run with [geoconda module](https://docs.csc.fi/apps/geoconda/), which includes all necessary Python packages. The easiest is to use Jupyter with Puhti web interface:

* Open [Puhti web interface](https://www.puhti.csc.fi/)
* Click "Jupyter" on dashboard
* Select following settings:
	* Project: project_2002044 during course, own project otherwise 
	* Partition: interactive
	* CPU cores: 1
	* Memory (Gb): 8 
	* Local disk: 0
	* Time: 1:00:00 (or adjust to reasonable)
	* Python: geoconda 
	* Jupyter type: Lab
	* Working directory: /scratch/project_2002044 during course, own project scratch otherwise
* Click launch and wait until granted resources 
* Click "Connect to Jupyter" 
* If you want to use Dask extension in JupyterLab, see [Dask instructions in docs.csc.fi](https://docs.csc.fi/support/tutorials/dask-python/#dask-with-jupyter)
