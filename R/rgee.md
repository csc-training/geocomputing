# Using R library rgee in Puhti

→ https://github.com/r-spatial/rgee

  * recent update from Google: authentication now requires gcloud CLI → https://cloud.google.com/sdk 
  * provides access to data and functions from Google Earth Engine (GEE) via R

RGEE can currently not easily be initialized on Puhti only; it is done on own computer instead and configuration files copied to Puhti

Please follow below steps to initialize RGEE on Puhti:

1) on your own computer:

  * with RGEE, gcloud installed on your own computer, do the initialization in R:

`ee_Initialize()` with all needed arguments

  * use miniconda or venv for the Python installation or manually provide the path to a Python where earthengine-api and numpy are installed (`EARTHENGINE_PYTHON=/path/to/python` in `.Renviron`)
  * this creates some files under `$HOME/.config/earthengine` ,
  * copy full earthengine directory to your `$HOME/.config` (`/users/<username>/.config`) directory on Puhti (e.g. via Puhti webinterface, scp or FileZilla) ( in this step, if you know what you are doing you can also copy just the configuration files to Puhti; but do this AFTER running ee_Install() on Puhti.)



2) on Puhti:

	* open the `$HOME/.config/earthengine/rgee_sessioninfo.txt` and check that all paths are correct for Puhti, if you did the initialization on a Windows machine, you need to change all paths here! For Linux you might only need to change the username in the path form your own computer name to your puhti username

    	* set up the installation directory for you or your groups R installations and
    	* tell R where to find it (see also https://docs.csc.fi/apps/r-env-singularity/#r-package-installations for more instructions)

```
.libPaths(c("/projappl/<project>/project_rpackages_<rversion>" , .libPaths()))
libpath <- .libPaths()[1]
# This command can be used to check that the folder is now visible:
.libPaths() # It should be first on the list
```

	* add this to .Renviron to be loaded at R startup (or add `.libPaths(c("/projappl/<project>/project_rpackages_<rversion>" , .libPaths())`) to every R script that needs rgee library)

`echo "R_LIBS=/projappl/<project>/project_rpackages_<rversion>" >> ~/.Renviron`
  
  * install `rgee` to that directory with

`install.packages("rgee")`

  * load rgee with `library(rgee)` run `ee_Install()` with all needed arguments (but same as you ran on your own computer) in R session, say no to miniconda, this creates a python virtual environment (based on Puhtis system Python) called rgee in your $HOME/.virtualenvs/ directory and installs earthengine-api and numpy into it
  * say yes to adding the `EARTHENGINE_x` environment variables to your `.Renviron`, your `.Renviron` may look like this:

```
R_LIBS=/projappl/project_<projectnumber>/project_rpackages_4.1.1
EARTHENGINE_PYTHON="/users/<username>/.virtualenvs/rgee/bin/python"
EARTHENGINE_ENV="rgee"
```

> Notes:
  
> * important to do same thing on own computer as what you want on Puhti, updates like adding GC support need to be done on own computer first and then resulting config files copied to Puhti
> * RGEE installation can be shared among members of same CSC project as long as they are using same R version; every member needs own credentials dir though;
might also be possible to share Python venv (not tested), adjust variables in .Renviron
> * restart R session after every step to make sure things are read correctly from the config and environment files
  
