# -*- coding: utf-8 -*-
"""
This script compares prediction results to ground truth (test data) and prints out confusion matrix and classification report.
The images do not need to be exactly of the same area, but the pixel size should be the same.
Data of only overlapping area is used for evaluation.

For binary classification a treshold must be given for dividing the pixels between two classes.

Created on Thu Mar 19 18:32:47 2020

This runs on small dataset in a moment so run with
module laod geoconda
python 09_3_evaluate.py

OR
module load tensorflow/nvidia-19.11-tf2-py3
singularity_wrapper exec python 09_3_evaluate.py

@author: ekkylli
"""
import os
import rasterio
import rasterio.mask
from sklearn.metrics import classification_report, confusion_matrix

# Paths for INPUTS: data and predcition image to evaluate
#TOFIX: Set file paths and the number of classes
data_dir='/scratch/project_2002044/data/GIS_ML_COURSE_DATA/data/forest'
results_dir='/scratch/project_2002044/students/ekkylli'

no_of_classes = 2

predicted_image_output_path = os.path.join(results_dir, 'T34VFM_20180829T100019_CNN_spruce_05_001.tif')
#predicted_image_output_path = os.path.join(results_dir, 'T34VFM_20180829T100019_CNN_multiclass_05_001.tif')

#Using the  clipped versions of labels, because of speed.
#In real case use the validation area. 
if no_of_classes == 2: 
    test_image_path = os.path.join(data_dir, 'forest_spruce_clip.tif')  
else:
    test_image_path = os.path.join(data_dir, 'forest_species_reclassified_clip.tif')
    
#Treshold for the binary classification
#Try to look from map a good value, or just try different ones.
prediction_treshold = 0.35    

def estimateModel():
    # Open image files of predicted data and test data
    with rasterio.open(predicted_image_output_path, 'r') as prediction_dataset:      
        with rasterio.open(test_image_path, 'r') as test_labels_dataset:           
            
            #Find out the overlappin area of two images.
            #Because of tiling the prediction image is slightly smaller than the original clip.
            left = max(prediction_dataset.bounds.left,test_labels_dataset.bounds.left)
            bottom = max(prediction_dataset.bounds.bottom,test_labels_dataset.bounds.bottom)
            right = min(prediction_dataset.bounds.right,test_labels_dataset.bounds.right)
            top = min(prediction_dataset.bounds.top,test_labels_dataset.bounds.top)
            
            common_bbox = [{
                        "type": "Polygon",
                        "coordinates": [[
                            [left, bottom],
                            [left, top],
                            [right, top],
                            [right, bottom],
                            [left, bottom]]]}]
                        
            # Read data from only the overlapping area
            y_pred, transform = rasterio.mask.mask(prediction_dataset, common_bbox, crop=True)
            y_true, transform = rasterio.mask.mask(test_labels_dataset, common_bbox, crop=True)
            
            # Reshape data for scikit-learn
            y_pred2 = y_pred.reshape(-1)
            y_true2 = y_true.reshape(-1)
            
            # If results of binary classification, reclassify the data based on the treshold.
            if no_of_classes == 2: 
                y_pred2[(y_pred2 >= prediction_treshold)] = 1
                y_pred2[(y_pred2 < prediction_treshold)] = 0
                y_pred2 = y_pred2.astype('int')
                print('Prediction_treshold: ', prediction_treshold) 
                                    
            print('Confusion Matrix')    
            print(confusion_matrix(y_true2, y_pred2))
            print('Classification Report')
            print(classification_report(y_true2, y_pred2, zero_division=0))
               
if __name__ == '__main__':
    estimateModel()             