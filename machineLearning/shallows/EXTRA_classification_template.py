import os, time
from imblearn.under_sampling import RandomUnderSampler
from joblib import dump, load
import numpy as np
import rasterio
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

# Set working directory and input/output file names.
base_folder = ''

# FILL HERE
inputImage = os.path.join(base_folder, '')
labelsImage = os.path.join(base_folder, '')

# Output image
outputImageBase = os.path.join(base_folder, 'predicted_image_')

# Available cores
n_jobs = 4

# Read data and shape it to suitable form for scikit-learn
# Exactly the same as for K-means for image data, labels part added
def prepareData(image_dataset, labels_dataset):
    print("Preparing the data")
    # Read the pixel values from .tif file as dataframe
    image_data = image_dataset.read()

    # We have to change the data format from bands x width x height to width*height x bands
    # This means that each pixel from the original dataset has own row in the result dataframe.
    # Check shape of input data
    print('Dataframe original shape, 3D: ', image_data.shape)
    # First move the bands to last axis.
    image_data2 = np.transpose(image_data, (1, 2, 0))
    # Check again the data shape, now the bands should be last.
    print('Dataframe shape after transpose, 3D: ', image_data2.shape)

    # Then reshape to 1D.
    pixels = image_data2.reshape(-1, 3)
    print('Dataframe shape after transpose and reshape, 2D: ', pixels.shape)

    # For labels only reshape to 1D is enough.
    labels_data = labels_dataset.read()
    input_labels = labels_data.reshape(-1)
    print('Labels shape after reshape, 1D: ', pixels.shape)

    # The forest classes are very imbalanced in the dataset, so undersample the majority classes
    rus = RandomUnderSampler(random_state=63)
    pixels_resampled, labels_resampled = rus.fit_resample(pixels, input_labels)
    print('Dataframe shape after undersampling of majority classes, 2D: ', pixels_resampled.shape)

    return pixels_resampled, labels_resampled


# Train the model and see how long it took.
def trainModel(x_train, y_train, clf, classifierName):
    print("Training the model")
    start_time = time.time()
    clf.fit(x_train, y_train)
    print('Model training took: ', round((time.time() - start_time), 2), ' seconds')

    # Save the model to a file
    modelFilePath = os.path.join(base_folder, ('model_' + classifierName + '.sav'))
    dump(clf, modelFilePath)
    return clf


# Predict on test data and see the model accuracy
def estimateModel(clf, x_test, y_test):
    print("Estimating model")
    test_predictions = clf.predict(x_test)
    print('Confusion matrix: \n', confusion_matrix(y_test, test_predictions))
    print('Classification report: \n', classification_report(y_test, test_predictions))


# Predict on whole image and save it as .tif file
def predictImage(modelName, inputImage):
    print("Predicting image")
    predictedClassesFile = outputImageBase + modelName + '.tif'
    predictedClassesPath = os.path.join(base_folder, predictedClassesFile)

    with rasterio.open(inputImage, 'r') as image_dataset:
        start_time = time.time()
        # Reshape data to 1D as we did before model prediction
        image_data = image_dataset.read()
        image_data2 = np.transpose(image_data, (1, 2, 0))
        pixels = image_data2.reshape(-1, 3)

        # Load the model from the saved file
        modelFilePath = os.path.join(base_folder, ('model_' + modelName + '.sav'))
        trained_model = load(modelFilePath)

        # predicting the class for each pixel
        prediction = trained_model.predict(pixels)

        # Reshape back to 2D
        print('Prediction shape in 1D: ', prediction.shape)
        prediction2D = np.reshape(prediction, (image_dataset.meta['height'], image_dataset.meta['width']))
        print('Prediction shape in 2D: ', prediction2D.shape)

        # Save the results as .tif file.
        # Copy the coorindate system information, image size and other metadata from the satellite image
        outputMeta = image_dataset.meta
        # Change the number of bands and data type.
        outputMeta.update(count=1, dtype='uint8')
        # Writing the image on the disk
        with rasterio.open(predictedClassesPath, 'w', **outputMeta) as dst:
            dst.write(prediction2D, 1)

        print('Predicting took: ', round((time.time() - start_time), 1), ' seconds')


def main():

    ### Read the input datasets with Rasterio
    labels_dataset = rasterio.open(labelsImage)
    image_dataset = rasterio.open(inputImage)

    ### Prepare data for all the models
    input_image, input_labels = prepareData(image_dataset, labels_dataset)
    ### Divide the data to test and training datasets
    x_train, x_test, y_train, y_test = train_test_split(input_image, input_labels, test_size=0.2, random_state=42)

    ### FILL HERE Choose the shallow model you want and train it
    model_name = '' # This is just the name as text, it will go to the filename of the model
    model_object = ''
    #for example this: RandomForestClassifier(n_estimators=100, max_depth=10, random_state=0, n_jobs=n_jobs)

    model = trainModel(x_train, y_train, model_object, model_name)
    estimateModel(model, x_test, y_test)
    predictImage(model_name, inputImage)
    print('Feature importances band INFRA-RED RED GREEN: \n', model.feature_importances_)

if __name__ == '__main__':
    ### This part just runs the main method and times it
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round((end - start), 0)) + " seconds")
