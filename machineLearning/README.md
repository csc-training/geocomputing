
# Scripts for the CSC Practical machine learning for spatial data course

Clustering. 
* Data: Sentinel satellite image. 
* Goal: Identify clouds.
* Models: [shallow](02_shallows/04_clustering.py)

Classification1
* Data: Sentinel satellite image + Finnish forest center forest stand polygons for labels.
* Goal: Classify image to pine, spurce, deciduous trees and no-forest. 
    * In CNN_solaris only spurce.
    * In CNN_keras all classes and only spruce.

* Models: [shallow](02_shallows/05_classification.py), [deep](03_deep/07_deepClassification.py), [CNN_solaris](04_cnn_solaris), [CNN_keras](05_cnn_keras)

Classification2
* Data: NLS infrared orthoimage + NLS topographic database (maastotietokanta) buildings for labels.
* Goal: Classify image to buildings and no-buildings. 
* Models: no ready models provided, similar code to forest classification could be used.

Regression
* Data: Paavo postcode areas.
* Goal: Predict average income of post-code areas.
* Models: [shallow](02_shallows/03_regression.py), [deep](03_deep/06_deepRegression.py).

Before the starting with the models also the [data preparation scripts](01_data_preparation) must be run.

Exercise data is available in two versions:
* [Source data, as downloaded from different sources](https://a3s.fi/gis-courses/GIS_ML_course_data.zip). 
* [Analysis-ready data](https://a3s.fi/gis-courses/GIS_ML_course_data_prepared.zip) as back-up and check-point. 

The numbers in the beginning of folders and files note the order exercises are done during the course.

The shallow learning exercises can well be run on any PC, likely also the deep learning examples here, for CNN a GPU machine is needed, for example CSC Puhti. For deep learning exercises therefore also Puhti batch job files are provided. 

Main used libraries:
* GDAL command-line, rasterio and geopandas for data preparations
* scikit-learn for shallow learning and some helping functions also for deep learning scripts (Puhti [geoconda](https://docs.csc.fi/apps/geoconda/) module)
* Keras for deep learning and CNN_keras (Puhti [tensorflow/2.0.0](https://docs.csc.fi/apps/tensorflow/) module)
* solaris and pytorch for CNN_solaris (Puhti [solaris](https://docs.csc.fi/apps/solaris/) module). The course materials have been tested with solaris-0.1.3, Puhti now includes also newer solaris-0.3.0.
* (There are also some minor libraries used, so check the imports of scripts before doing the installations to your own PC. Conda installation of Python packages is warmly recommended, you can use the [gis.yml](gis.yml) file provided here.)

GIS and machine learning libraries in Puhti:
In Puhti there are a lot of installations of GIS and machine learning libraries, including [geoconda](https://docs.csc.fi/apps/geoconda/), [keras/tensorflow](https://docs.csc.fi/apps/tensorflow/) and [pytorch](https://docs.csc.fi/apps/pytorch/). But these are all conda installations, so you can choose only one at a time.

### Options for using GIS and machine-learning libraries at the same time
* [geoconda](https://docs.csc.fi/apps/geoconda/) includes scikit-learn 
* [solaris](https://docs.csc.fi/apps/solaris/) includes pytorch, the tensorflow in solaris installation is unfortunatelly broken, so do not us it.
* [tensorflow/2.0.0](https://docs.csc.fi/apps/tensorflow/) includes geopandas and rasterio
* [pytorch/1.4](https://docs.csc.fi/apps/pytorch/) and pytorch/nvidia-20.07-py3 include geopandas and rasterio
* If you want to use some other version of keras/tensorflow, pytorch or some other machine learning library already available in Puhti you can add GIS-libraries with pip. For example for adding geopandas to pytorch/1.3.1:

```
module load pytorch/1.3.1
module load gcc/9.1.0 gdal
export PYTHONUSERBASE='/projappl/project_XXX/python_pip/lib/python3.7/site-packages'
pip install --user shapely fiona pyproj geopandas
```

The same first 3 rows must be later included also to your batch job.

GDAL is required by geopandas, if you use some other library it might not be necessary.
