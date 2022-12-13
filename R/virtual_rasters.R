# Example scripts for using virtual rasters.
# Here contours are calculated based on a 2m DEM file and saved in GeoPackage format.
# As input 4 different options are used:
# 1) Paituli files, copied to Puhti local disk
# 2) Paituli files, with URLs (from Espoo)
# 3) GeoPortti GeoCubes file (physically in cPouta next to Puhti, in Kajaani)
# 4) FMI STAC file (physically somewhere else in Finland)
# All of these data sources cover all Finland.
# The contours are calculated only on a subset of the data, defined by BBOX.
# BBOX location can be changed to any other location in Finland.

library(terra)
# For measuring computation time
library(tictoc)


# The extent of used data
# bbox_vrt <- ext(489000, 490000, 7333000, 7334000)
# Bigger BBOX
bbox_vrt <- ext(480000, 490000, 7330000, 7340000)


# Paituli files in Puhti locally
puhti_dem2m_vrt <- "/appl/data/geo/mml/dem2m/dem2m_direct.vrt"
puhti_result_file <- 'Puhti_vrt_contours.gpkg'

# Paituli files (URL)
# Link from here: https://www.nic.funet.fi/index/geodata/mml/dem2m/2008_latest/
paituli_dem2m_vrt <- "/vsicurl/https://www.nic.funet.fi/index/geodata/mml/dem2m/2008_latest/dem2m.vrt"
paituli_result_file <- 'Paituli_vrt_contours.gpkg'


# GeoPortti GeoCubes files
# Link from here: https://vm0160.kaj.pouta.csc.fi/geocubes/fileaccess/
geocubes_dem2m_vrt <- "/vsicurl/https://vm0160.kaj.pouta.csc.fi/mml/korkeusmalli/km2/2022/km2_2022_2m.vrt"
geocubes_result_file <- 'Geocubes_vrt_contours.gpkg'

# FMI STAC files
# Link from here: https://pta.data.lit.fmi.fi/stac/items/MML-DTM-2m/MML-DTM-2m_2020.json
fmi_dem2m_vrt <- '/vsicurl/https://pta.data.lit.fmi.fi/dem/etrs-tm35fin-n2000/MML-DTM-2020-2m-height.vrt'
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
tic("Paituli files, in Puhti locally")
contours_from_vrt(puhti_dem2m_vrt, bbox_vrt, puhti_result_file)
toc()

tic("Paituli files, URL")
contours_from_vrt(geocubes_dem2m_vrt, bbox_vrt, geocubes_result_file)
toc()

tic("GeoCubes in cPouta")
contours_from_vrt(geocubes_dem2m_vrt, bbox_vrt, geocubes_result_file)
toc()

tic("FMI")
contours_from_vrt(fmi_dem2m_vrt, bbox_vrt, fmi_result_file)
toc()