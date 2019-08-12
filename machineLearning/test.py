#!/usr/bin/python


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
        xys = []
        classes = []
        with open(csvText) as fp:
            reader = csv.reader(fp)
            next(reader)
            for row in reader:
                xys.append([float(n) for n in row[:2]])
                classes.append(int(row[2]))
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
        ds = gdal.Open(band)
        pixel_trans = gdal.Transformer(ds, None, [])
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
                bands.append(ds.GetRasterBand(i).ReadAsArray())
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
    except Exception as ex:
        print(ex)
    else:
        driver = gdal.GetDriverByName('GTiff')
        out_ds = driver.Create(fn, in_ds.RasterXSize, in_ds.RasterYSize, 1, data_type)
        out_ds.SetProjection(in_ds.GetProjection())
        out_ds.SetGeoTransform(in_ds.GetGeoTransform())
        out_band = out_ds.GetRasterBand(1)
        if nodata is not None:
            out_band.SetNoDataValue(nodata)
        out_band.WriteArray(data)
        out_band.FlushCache()
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
        colored_ds = gdal.Open(ds1)
        colors = colored_ds.GetRasterBand(1).GetRasterColorTable()
        ds2.GetRasterBand(1).SetRasterColorTable(colors)
        del colored_ds


def random_forest(sampleCoordinates, images, trees=100, directory_to_save='prediction60.tif'):
    """
    Establishing random forest classifier
    :param sampleCoordinates: a csv file format containing ground truth coordinates
    :param bands: list of satellite bands
    :param trees: number of trees in the model
    :return: classified image
    """
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report, confusion_matrix
        from osgeo import gdal
        import numpy as np
        from sklearn import tree
    except Exception as ex:
        print(ex)
    else:
        xys, classes = extract_training_samples(sampleCoordinates)
        cols, rows = calculate_image_offsets(images[1], xys) # targeting image with one band
        data = stack_bands(images)
        # Converting offset types from float to int in order to be eligible for slicing
        cols = list(map(int, cols))
        rows = list(map(int, rows))
        # Sample the satellite data at the coordinates from the csv.
        sample = data[rows, cols, :]
        x_train, x_test, y_train, y_test = train_test_split(sample, classes, test_size=0.3, random_state=63)
        # Initialize a random forest instance
        #rf = RandomForestClassifier(n_estimators=trees)
        model = tree.DecisionTreeClassifier(max_depth=5)
        # Train the model
        rf = model.fit(x_train, y_train)
        test_predictions = model.predict(x_test)
        print(confusion_matrix(y_test, test_predictions))
        print('\n')
        print(classification_report(y_test, test_predictions))
        rows, cols, bands = data.shape
        # Apply the model to the satellite data
        data2d = np.reshape(data, (rows * cols, bands))
        prediction = model.predict(data2d)
        prediction = np.reshape(prediction, (rows, cols))
        # Set pixels with no satellite data to zero
        prediction[np.sum(data, 2) == 0] = 0
        ds = gdal.Open(images[1])
        predict_ds = make_raster(ds, directory_to_save, prediction, gdal.GDT_Byte, 0)
        predict_ds.FlushCache()
        levels = compute_overview_levels(predict_ds.GetRasterBand(1))
        predict_ds.BuildOverviews('NEAREST', levels)
        del ds
        return predict_ds


if __name__ == '__main__':
    samples = 'Landsat/Utah/training_data.csv'
    bands = ['Landsat/Utah/LE70380322000181EDC02_60m.tif', 'Landsat/Utah/LE70380322000181EDC02_TIR_60m.tif']
    landCover = 'Landsat/Utah/landcover60.tif' # the image that containes a color table
    classified_image = random_forest(samples, bands, trees=200)
    make_color_table(landCover, classified_image)
