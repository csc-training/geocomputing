# Example how to use CSC STAC API from R, with rstac, gdalcubes and terra libraries.

# This example shows how to use CSC STAC (Spatio-Temporal Asset Catalog) from R, with rstac, gdalcubes and terra libraries
# for processing big raster datasets, also with good support for time series. 
# The main idea is to first define the search and processing as process graph. 
# The downloading and processing is done lazily at the end, 
# so that only needed data (good enough cloud-free image, only needed bands and area) is downloaded. 
# The libraries take care of data download, so you do not need to know about file paths. 
# These tools work best when data is provided as Cloud-optimized GeoTiffs (COGs).

# For trying out this example, it is recommended to start interactive RStudio session with Puhti web interface, 
# for example with 1 cores and 8 Gb memory. 

# The main steps:

# * Query STAC catalog, to see which data collections are available
# * Query STAC catalogue to find data from area and time of interest 
# * Plot search results as index map to see their coverage
# * Create datacube, defining required bands and bbox, and time step for aggregation.
# * Finally, calculate the result and plot it or save it to file.
# * Additional example is given, how to get data URLs and use them with terra package.

# CSC STAC catalog is at the moment beta testing phase. 

# This example works with r-env/421 module in Puhti, the required libraries can be seen from imports.
# Currently Puhti r-env does not support JP2000 format, so sentinel2-l2a can not be used with gdalcubes
# Searching all collections works.

# This example is partly based on:
# * https://r-spatial.org/r/2021/04/23/cloud-based-cubes.html
# * https://geocompr.robinlovelace.net/gis.html#cloud
# * https://cran.r-project.org/web/packages/rstac/vignettes/rstac-03-cql2-mpc.html

# Import required libraries.
library(rstac) # For working with STAC catalogs, rstac docs: https://rdrr.io/cran/rstac/
library(httr) # For adding response type to STAC requests
library(gdalcubes) # For 4D spatial data cube in R
library(sf) # For plotting index map
library(tidyverse) # For plotting
library(terra) # For opening single raster datasets

# Set up STAC API endpoint
stac_URL <- "https://paituli.csc.fi/geoserver/ogc/stac"

# Define the center of area of interest, in this case Helsinki.
# For searching STAC always geographic coordinates must be used (EPSG=4326).
hki_wgs_x <- 24.945
hki_wgs_y <- 60.173

# Convert to CQL2 BBOX, used for search. 
bbox <- c(hki_wgs_x-0.1, hki_wgs_y-0.1, hki_wgs_x+0.1, hki_wgs_y+0.1)
area_of_interest <- cql2_bbox_as_geojson(bbox)

# Convert to SF dataframe, used for plotting and later creating data cube
helsinki_wgs <- data.frame(x = hki_wgs_x, y = hki_wgs_y) |>
  st_as_sf(coords = 1:2, crs = 4326)

# Define time period for search
startDate <-"2021-08-01"
endDate <- "2021-09-30"

# STAC BASICS
# Get connection to STAC catalog
stac_gs <- stac(stac_URL, force_version = '1.0.0')

# List all collections
stac_gs |> 
  collections() |>
  get_request()

# Define our the colleciton used in this example
collectionName <- 'sentinel_1_11_days_mosaics_at_fmi'

# Get info about a specific catalog
stac_gs |> 
  collections(collectionName) |>
  get_request()

# What kind of data (=assets) does a collection have?
# CSC STAC provides as default html as result, therefore result type has to manually be added
# to this and several other requests.
stac_gs |>
  stac_search(
    collections = collectionName,
    limit = 1) |> 
  get_request(accept("application/geo+json")) |>
  items_assets()   

# SEARCH ITEMS
# Basic search.  
stac_items <- stac_gs |> 
  stac_search(
    collections = ("sentinel_1_11_days_mosaics_at_fmi"),
    bbox = bbox, 
    datetime = paste(startDate,"/",endDate, sep="")) |>
  get_request(verbose(), accept("application/geo+json")) |>  
  items_fetch(accept("application/geo+json"))

# If modifying the search criteria, it might be better first to exclude the items_fetch part and check first how many items were found.
# Fetching big amounts of items is rather slow.
# You may remove verbose() from above, if you do not want to see what requests are actually done.

items_matched(stac_items)

# ADVANCED SEARCH WITH FILTER
# Basic search supports only limiting by collection name, location and time. 
# sentinel2-l2a collection has also information about cloud coverage.
# This can be searched with filter search
# See https://rdrr.io/cran/rstac/man/ext_filter.html for more options.
stac_items2 <- stac_gs |>
  ext_filter(
    collection == "sentinel2-l2a" &&
      #s_intersects(geometry, {{area_of_interest}}) &&
      datetime >= {{startDate}} &&
      datetime <= {{endDate}} &&      
      `eo:cloud_cover` > 80
  ) |>
  post_request(verbose(), accept("application/geo+json")) |>
  items_fetch(accept("application/geo+json"))

items_matched(stac_items2)

# PLOTTING index map of search results
# Convert search results to sf geodataframe
stac_items_sf <- items_as_sf(stac_items2)

# Plot, also the data search point, just as example.
# Using alpha to visualize overlapping polygons.
ggplot() +
  geom_sf(data = stac_items_sf, fill=alpha("violet",0.1)) +
  geom_sf(data = helsinki_wgs)


# CREATE DATA CUBE AND ANALYZE THE DATA
# gdalcubes is the package to use for 4D spatial data cubes in R.
# It is somewhat different than xarray in Python,
# and it likely has less features (and other users).
# gdalcubes docs: https://rdrr.io/cran/gdalcubes/ 

# First create an image collection of files found with STAC
# The image collection could be saved also to disc, 
# so that it is not necessary to repeat the STAC search again.
# See https://rdrr.io/cran/gdalcubes/man/create_image_collection.html for more options

#assets = c("B04_60m", "B03_60m", "B02_60m")
assets = c("mean_vv")

col <- stac_image_collection(stac_items$features, asset_names = assets)

# Second, create data cube view.

# In what coordinate system you want to have the data?
# It can be different that the original data,
# but using same coordinate system than data has, is fastest.

# You can see data coordinate system for example from this.
# Note, one collection may have data with different coordinate systems.
stac_items_sf <- items_as_sf(stac_items)
stac_items_sf

data_crs <- 3067
#data_crs = 32635

# Used other options:
# * Extent.
# * dx and dy - pixel size, it can be different than original data, for bigger pixel data overviews will be used, if available.
# * dt - time interval, "P1M" means monthly
# * aggregation - how data is aggregated
# More options: https://rdrr.io/cran/gdalcubes/man/cube_view.html

# Extent is given in the same coordinate system as used for data cube.
# Convert Helsinki coordinates data coordinate system.
helsinki_utm <- st_transform(helsinki_wgs, data_crs)
helsinki_utm_x <- st_coordinates(helsinki_utm)[1]
helsinki_utm_y <- st_coordinates(helsinki_utm)[2]
buffer_size <- 10000

v <- cube_view(srs = paste("EPSG:",data_crs, sep=""),  extent = list(t0 = startDate, t1 = endDate,
                                                                     left = helsinki_utm_x - buffer_size, right = helsinki_utm_x + buffer_size,  
                                                                     top = helsinki_utm_y + buffer_size, bottom = helsinki_utm_y - buffer_size),
               dx = 60, dy = 60, dt = "P1M", aggregation = "mean")

# Create data cube with given settings and data from above image collection.
# gdalcubes provides additional functions for analyzing the data.
# Monthly aggregation by mean was defined already in the cube view level, so here we only plot now.
cube <- raster_cube(col, v) 

# Plot data
# More options: https://gdalcubes.github.io/source/reference/ref/plot.cube.html
plot(cube, key.pos=4, zlim=c(-40,30), t = 1:2, ncol = 1)

# Write files, gdalcubes writes automatically each time period to own file.
# More options: https://gdalcubes.github.io/source/reference/ref/write_tif.html
# Set first R working directory.
setwd('/scratch/project_2000XXX/yyy')
write_tif(cube, dir='tifs', prefix='monthly_mean_bbox_')

# The same for whole Finland.
# For big areas or long time series gdalcubes supports parallel processing to some extent.
# In a test with all Finland 8 cores was ~5x times faster than 1 core.
# Set options according to available number of cores.
# This can be run with one core, but it takes a few minutes.
# In Puhti, you need to reserve the cores at the RStudio start-up time.
gdalcubes_options(parallel=1) 

# Create data view with full extent of original data.
# For testing increase pixel size significantly, to first check that results are as expected.
v <- cube_view(srs = paste("EPSG:",data_crs, sep=""),  extent = col,
               dx = 60, dy = 60, dt = "P1M", aggregation = "mean")

# Calculate and save to files.
# With one core this takes a few minutes.
raster_cube(col, v) |>
 write_tif( dir='tifs', prefix='monthly_mean_Finland')


# USING DATA FROM STAC WITH TERRA

# Sometimes it might be useful to open the files with terra or some other R package
# for analysis not supported with gdalcubes.

# Get the URL of data of second asset found.
# Terra does not support time dimension, so handling that must be done manually.
href <- stac_items$features[[2]]$assets$mean_vv$href
# Add vsicurl to URL, so that terra could use it.
href_with_vsicurl <- paste('/vsicurl/',href, sep="")

# Open datasets from URL, note that only some metadata is fetched at this point
data <- rast(href_with_vsicurl)  
# It is possible to read only a subset of data
data_cropped = crop(data , ext(370000, 400000, 6665000, 6685000))

# Plot, now data is fetched and plotted.
plot(data_cropped)