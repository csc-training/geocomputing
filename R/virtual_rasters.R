# Example scripts for using virtual rasters.
# Here contours are calculated based on a 2m DEM file and saved in GeoPackage format.
# As input 3 different options are used:
# 1) Puhti local file
# 2) GeoPortti GeoCubes file (physically in cPouta next to Puhti)
# 3) FMI STAC file (physically somwhere else in Finland)
# All of these data sources cover all Finland.
# The contours are calculated only on a subset of the data, defined by BBOX.
# BBOX location can be changed to any other location in Finland.

library(terra)
# For measuring computation time
library(tictoc)


# The extent of used data
bbox_vrt <- ext(269000, 270000, 7662000, 7663000)
# Bigger BBOX
# bbox_vrt <- ext(260000, 270000, 7653000, 7663000)

# Puhti files
puhti_dem2m_vrt <- "/appl/data/geo/mml/dem2m/dem2m_direct.vrt"
puhti_result_file <- 'Puhti_vrt_contours.gpkg'

# GeoPortti GeoCubes files
geocubes_dem2m_vrt <- "https://vm0160.kaj.pouta.csc.fi/mml/korkeusmalli/km2/2022/km2_2022_2m.vrt"
geocubes_result_file <- 'Geocubes_vrt_contours.gpkg'

# FMI STAC files
fmi_dem2m_vrt <- 'https://pta.data.lit.fmi.fi/dem/etrs-tm35fin-n2000/MML-DTM-2020-2m-height.vrt'
fmi_result_file <- 'FMI_vrt_contours.gpkg'

# Function to handle each dataset
contours_from_vrt <- function(vrt_path, bbox, output_file){
  # Create terra SpatRaster object of virtual raster file.
  # Data is not read to R at this phase.
  vrt <- rast(vrt_path)
  # Crop the SpatRaster to our area of interest.
  DEM = crop(vrt, bbox)
  # Calcualte contours.
  contours <- as.contour(DEM)
  # Save result to a file.
  writeVector(contours, output_file, filetype="GPKG", overwrite=TRUE)
}

# Run the function with each data source and see how long it takes.
tic("Puhti local files")
contours_from_vrt(puhti_dem2m_vrt, bbox_vrt, puhti_result_file)
toc()

tic("GeoCubes in Allas")
contours_from_vrt(geocubes_dem2m_vrt, bbox_vrt, geocubes_result_file)
toc()

tic("FMI")
contours_from_vrt(fmi_dem2m_vrt, bbox_vrt, fmi_result_file)
toc()