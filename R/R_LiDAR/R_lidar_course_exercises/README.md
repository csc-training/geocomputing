## R lidar exercise CSC's R lidar course
In these exercises the most basic functions of the `rlas` and `lidR` R packages by Jean-Romain are demonstrated. See the documentation for these packages from [rlas](https://cran.r-project.org/web/packages/rlas/index.html) and [lidR](https://github.com/Jean-Romain/lidR/wiki).

The materials in this repository are based mostly on the above mentioned documentation with some edits and new parts to adapt them to using these libraries in CSC's Taito supercluster.

## Course related info
The original 2019 CSC's course page: [Lidar data analysis in Taito, with PDAL and R](https://www.csc.fi/web/training/-/lidar-data-analysis-in-taito-with-pdal-and-r)


You need to download the dataset from: https://gis-open.object.pouta.csc.fi/r_lidar_data.zip. Unzip the data to your $WRKDIR directory. The data will be accessible by your scripts at  `/wrk/your-username-here/R_lidar_2019/r_lidar_data/`

The original NLS lidar files might not workd with `lidR`, because of scale errors. For fixing this, use e.g. las2las

fix one file with: 
```
las2las -i /wrk/project_ogiir-csc/mml/laserkeilaus/2008_17/2017/T522/1/T5224F1.laz -rescale 0.01 0.01 0.01 -auto_reoffset -o ~/outfolder/T5224F1.laz
```

all with (in same directory):
```
las2las -i ~/original_las_dir/*.laz -rescale 0.01 0.01 0.01 -auto_reoffset -olaz -odir ~/outdir/
```

The most up-to-date version of the exercises is in this repository. Download the contents of this repository as a zip file to your $WRKDIR in Taito and unzip it with `unzip R_lidar_2019.zip`. Then connect to Taito using NoMachine and start RStudio. Open the `R_lidar.Rproj` project from the `r_exercise` folder you just unziped.

Note that all the necessary software packages are already installed in the Taito supercluster and thus their installation is not covered in these exercises. To see a description of the installed R spatial packages ready installed see: https://research.csc.fi/-/rspatial-env
