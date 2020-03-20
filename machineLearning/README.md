
# Scripts for the CSC Practical machine learning for spatial data course

Clustering. 
* Data: Sentinel satellite image. 
* Goal: Identify clouds.
* Models: [shallow](02_shallows/04_clustering.py)

Classification
* Data: Sentinel satellite image + forest stand polygons for labels.
* Goal: Classify image to pine, spurce, deciduous trees and no-forest. 
    * In CNN_solaris only spurce.
    * In CNN_keras all classes and only spruce.
 
* Models: [shallow](02_shallows/05_classification.py), [deep](03_deep/07_deepClassification.py), [CNN_solaris](04_cnn_solaris), [CNN_keras](05_cnn_keras)

Regression
* Data: Paavo postcode areas.
* Goal: Predict average income of post-code areas.
* Models: [shallow](02_shallows/03_regression.py), [deep](03_deep/06_deepRegression.py).

Before the starting with the models also the [data preparation scripts](01_data_preparation) must be run.

The shallow learning exercises can well be run on any PC, likely also the deep learning examples here, for CNN a GPU machine is needed, for example CSC Puhti. For deep learning exercises therefore also Puhti batch job files are provided. 
