
def extract_training_samples(csvText):
    """
    Read the coordinates and actual classification from the csv.
    :param csvText: a text file containing coordinates of ground truth samples
    :return: two separate lists containing training data and its corresponding labels are returned
    """
    try:
        import csv
    except Exception as ex:
        print(ex)
    else:
        # create a list of coordinates such as [[32,34], [34,23]], which is a list of lists
        xys = []
        # create a list of associated classes to each point such as [82, 119, 48]
        classes = []
        with open(csvText) as fp:
            #initialize a CSV reader instance for reading the lines
            reader = csv.reader(fp)
            #skip the first line of the CSV file
            next(reader)
            for row in reader:
                # appending each row of coordinates into the list named xys
                xys.append([float(n) for n in row[:2]])
                # appending associated classes to the list called classes
                classes.append(int(row[2]))
        # returning list of coordinates and their associated classes
        return xys, classes


def calculate_image_offsets(band, coordinates):
    """
    :param band: one band
    :param coordinates: a list of ground truth coordinates in geographic CRS
    :return: ground truth coordinates in image coordinate system
    """
    try:
        from osgeo import gdal
    except Exception as ex:
        print(ex)
    else:
        # opening a image
        ds = gdal.Open(band)
        # Initializing a transformer object to convert world coordinates to pixel coordinates system
        pixel_trans = gdal.Transformer(ds, None, [])
        # 
        offset, ok = pixel_trans.TransformPoints(True, coordinates)
        cols, rows, z = zip(*offset)
        return cols, rows


def stack_bands(filenames):
    """
    :param filenames: a list of bands' names
    :return: a 3D array containing all band data
    """
    try:
        import numpy as np
        from osgeo import gdal
    except Exception as ex:
        print(ex)
    else:
        bands = []
        for fn in filenames:
            ds = gdal.Open(fn)
            for i in range(1, ds.RasterCount + 1):
                # reading each band and appending it to the list named bands
                bands.append(ds.GetRasterBand(i).ReadAsArray())
        # stacking all bands on top of each other
        return np.dstack(bands)


def make_raster(in_ds, fn, data, data_type, nodata=None):
    """ Create a one-band GeoTIFF
    :param in_ds: datasource to copy projection and geotransform from
    :param fn: path to the file to create
    :param data: numpy array containing data to write
    :param data_type: output data type
    :param nodata: optional NoData value
    :return: a new GeoTIFF band
    """
    try:
        from osgeo import gdal
        import os
    except Exception as ex:
        print(ex)
    else:
        # initializing a tiff driver to be able to generate an image
        driver = gdal.GetDriverByName('GTiff')
        if os.path.exists(fn):
            os.remove(fn)
        # create an image based on size of given image (in_ds)
        out_ds = driver.Create(fn, in_ds.RasterXSize, in_ds.RasterYSize, 1, data_type)
        # setting up the projection and transformation metadata based on the given image
        out_ds.SetProjection(in_ds.GetProjection())
        out_ds.SetGeoTransform(in_ds.GetGeoTransform())
        # extracting the first band of new dataset for writing
        out_band = out_ds.GetRasterBand(1)
        if nodata is not None:
            # handling no data values in the new image based on value given by users
            out_band.SetNoDataValue(nodata)
        # write the new image
        out_band.WriteArray(data)
        # making sure that all data has been written on disk
        out_band.FlushCache()
        # calculate image statistics
        out_band.ComputeStatistics(False)
        return out_ds


def compute_overview_levels(band):
    """Return an appropriate list of overview levels."""
    max_dim = max(band.XSize, band.YSize)
    overviews = []
    level = 1
    while max_dim > 256:
        level *= 2
        overviews.append(level)
        max_dim /= 2
    return overviews


def make_color_table(ds1, ds2):
    """ make a color table for ds2 based on existing color table in ds1
    :param ds1: dataset that containes a color table
    :param ds2: dataset that will get a color table
    :return: None
    """
    try:
        from osgeo import gdal
    except Exception as ex:
        print(ex)
    else:
        # opening the image
        colored_ds = gdal.Open(ds1)
        # extracting color table of an existing image to be used for the new image
        colors = colored_ds.GetRasterBand(1).GetRasterColorTable()
        # setting the color table for the new image
        ds2.GetRasterBand(1).SetRasterColorTable(colors)
        del colored_ds


def random_forest(sampleCoordinates, images, trees=50, directory_to_save='prediction60.tif'):
    """
    Establishing random forest classifier
    :param sampleCoordinates: a csv file format containing ground truth coordinates
    :param bands: list of satellite bands
    :param trees: number of trees in the model
    :return: classified image
    """
    try:
        from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
        from sklearn.metrics import classification_report, confusion_matrix
        from osgeo import gdal
        import numpy as np
        from sklearn import tree
        from dask.distributed import Client
        # initializing a process-based local client for distributed computations. Change it to False for thread-based.
        client = Client(processes=True)
        from joblib import parallel_backend
        import logging, time
        from dask_ml.wrappers import ParallelPostFit
        from dask_ml.model_selection import train_test_split

        logging.warning('In case your are asked for allowing connection in the local network,'
             ' accept it, otherwise you may face a connection error occurring between the processes!\n')

        logging.warning('No firewall limitations are essential for the multiple processes in the backend!\n')

        logging.warning('In case your have firewall limitations and you do not have right to modify its settings,'
                        ' you must set the parameter named "processes=False",'
                        ' which is located in Client object defined above, '
              'this will change your parallelization mode from processor-based to thread-based.\n')

        time.sleep(1)

    except Exception as ex:
        print(ex)
    else:
        # Consider using thread-based configuration described below if you are using an old machine to run the code.
        # Initializing a thread-based local client for distributed computations.
        # client = Client(processes=False, threads_per_worker=5,
        #        n_workers=1, memory_limit='3GB') # meaning 1 process with 4 threads is used.
        with parallel_backend('dask'):
            # extracting training points and their labels from a CSV file.
            xys, classes = extract_training_samples(sampleCoordinates)
            # converting world coordinates to image coordinate system.
            cols, rows = calculate_image_offsets(images[1], xys)
            # stack the bands on top of each other like a cake layers.
            data = stack_bands(images)
            # Converting offset types from float to int in order to be eligible for slicing operation.
            cols = list(map(int, cols))
            rows = list(map(int, rows))
            # Sample the satellite data at the extracted coordinates from the csv.
            sample = data[rows, cols, :]
            x_train, x_test, y_train, y_test = train_test_split(sample, classes, test_size=0.2, random_state=63)
            # Initialize a random forest instance by wrapping it in a meta-estimator
            model = ParallelPostFit(estimator=RandomForestClassifier(n_estimators=trees))
            # initialize a decision tree classifier.
            #model = tree.DecisionTreeClassifier(max_depth=5)
            # initialize a gradient boosting machine classifier by wrapping it in a meta-estimator
            #model = ParallelPostFit(estimator=GradientBoostingClassifier())
            # Train the classifier
            model.fit(x_train, y_train)
            test_predictions = model.predict(x_test)
            #print(confusion_matrix(y_test, test_predictions))
            print('\n')
            print(classification_report(y_test, test_predictions))
            rows, cols, bands = data.shape
            # Apply the model to the satellite data
            data2d = np.reshape(data, (rows * cols, bands))
            # predicting the image using the trained model
            prediction = model.predict(data2d)
            # reshape the flattened image to 2-D shape
            prediction = np.reshape(prediction, (rows, cols))
            # Set pixels with no values to zero, 2 represents the dimension of summing in the tensor
            prediction[np.sum(data, 2) == 0] = 0
            # opening the input image to get its meta data for the new image
            ds = gdal.Open(images[1])
            # generating the new image using predicted data
            predict_ds = make_raster(ds, directory_to_save, prediction, gdal.GDT_Byte, 0)
            # making sure that all data has been written on the disk
            predict_ds.FlushCache()
            # calculating overviews values for the new image like [2, 4, 8, 16] automatically
            levels = compute_overview_levels(predict_ds.GetRasterBand(1))
            # building the overviews using Nearest neighbor interpolation since the image has discrete values
            predict_ds.BuildOverviews('NEAREST', levels)
            del ds
            return predict_ds


if __name__ == '__main__':
    samples = 'xys.txt'
    bands = ['Sentinel/T35VMH_20180811T095031_B02_10m.jp2', 'Sentinel/T35VMH_20180811T095031_B03_10m.jp2',
             'Sentinel/T35VMH_20180811T095031_B04_10m.jp2', 'Sentinel/T35VMH_20180811T095031_B08_10m.jp2']
    #bands = ['Landsat/Utah/LE70380322000181EDC02_60m.tif', 'Landsat/Utah/LE70380322000181EDC02_TIR_60m.tif']
    #landCover = 'Landsat/Utah/landcover60.tif' # the image that containes a color table
    classified_image = random_forest(samples, images=bands, trees=20)
    #make_color_table(landCover, classified_image)
