# STAC Python examples

The [STAC](https://stacspec.org/en/) is a specification to describe geospatial information, so it can easily **searched and downloaded**. 
STAC includes metadata of datasets and links to actual files, the data files are usually stored in the cloud. See [Paituli STAC page](https://paituli.csc.fi/stac.html) for general introduction about STAC and what Collections (=datasets) are included in Paituli STAC.

In this repository we provide examples to work with:

* STAC API:
    * [Paituli STAC API](STAC_CSC_example.ipynb)
    * [Element84 STAC API](stac_xarray_dask_example.ipynb)
* Static STAC: 
    * [FMI STAC](static_stac.ipynb)
* See, also similar [R STAC examples](../../R/STAC)

The examples mainly cover data search and download, using [pystac-client](https://pystac-client.readthedocs.io/en/stable/) and [stackstac](https://stackstac.readthedocs.io/en/latest/).  For analyzing data [xarray](https://docs.xarray.dev/en/stable/) and [xarray-spatial](https://xarray-spatial.org/) can be used. If unfamiliar with xarray, [Pangeo 101](https://pangeo-data.github.io/foss4g-2022/intro.html) is one option to get started. When working with bigger datasts, xarray supports also parallelization with [dask](https://www.dask.org/).

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


## Running the STAC example Jupyter Notebook on your own computer

You can also run the STAC example notebook on your own computer.

Download the example code to your computer (either by copying the whole repository to your computer with git (`git clone https://github.com/csc-training/geocomputing.git`) or by downloading only the needed files via github webinterface (find `python/STAC/environment.yml` and `python/STAC/STAC_CSC_example.ipynb` and in the upper right corner of the file "Download raw file button"). 

If you have [Conda](https://conda.io/projects/conda/en/latest/index.html) installed, you can for example create a new environment and use the provided `environment.yml` file to create a new Python environment with all needed packages:

```
conda env create -f path/to/your/downloaded/environment.yml
```

## Using STAC and dask for whole Finland (scaling the example)

The example notebook covers only small area and therefore runs fast and requires little resources. The same code can be easily extended to cover whole Finland or some other bigger area. Basically only a few changes are needed:
* Extend analysis area in the Python code
  	* Change location criteria in the STAC search, use a bigger bbox or remove the location criteria.
	* Change `bounds` setting in `stackstac.stack`, use a bigger bbox or remove `bounds` setting.
* If running in HPC, give your Jupyter more computing resources. Start a new Jupyter session and give it more cores and memory than recommended in the example. If running the notebooks locally, then no changes are needed. 
* Start Dask cluster
	* Uncomment the Dask cluster starting cell.
  	* Dask will pick up all available computing resources automatically.
 
### How many cores and how much memory to use?

From Dask point of view, it is easy to use up to the full node of HPC, that would be 40 cores in Puhti supercomputer. With [Dask-Jobqueue] it is possible to run also multi-node jobs. But in STAC use case, the computation time is heavily dependent on data download speed, which does not scale so well. So in practice a smaller number of cores is more reasonable. With computationally easier analysis, the recommended number of **cores is 5-12**. If the computational part takes significant amount of time compared to data download, also bigger numbers of cores could be used. 

The **memory** requirements depend more on the specific analysis, but a starting point could be **8-10Gb/core**. 

### Run the code via batch jobs

For longer analysis, it is recommended to switch from Jupyter notebook to usual Python code and run it via HPC batch job system.

### Dask chunk size
One more optimization option is to manually assign [Dask chunksize](https://docs.xarray.dev/en/v0.14.0/dask.html#chunking-and-performance). In our tests bigger chunksize (4096x4096 compared to 1024x1024) resulted in clearly shorter compute times, if 1-5 cores were used. But with 10-20 core the chunksize had no influence on compute times.

Some HPC specific comments:
* Use `--mem-per-cpu` in the batch job file, when defining the memory reservation.
* The dask clusters are unlikely to give direct "Out of memory" errors to SLURM scheduler, that would directly kill the job. Rather different warnings and errors appear in the job output file, so keep an eye on that.
* Normally `seff` output can be used for planning batch jobs memory requirements, but with Dask clusters clearly bigger extra buffer is needed.
