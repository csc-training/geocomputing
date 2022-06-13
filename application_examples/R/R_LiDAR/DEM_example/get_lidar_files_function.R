# Function to get LiDAR files from Puhti's GIS datasets for a
# given area of interest

# Make sure that you have Puhti's R spatial environment loaded by using module load r-env or by using interactively 
# GIS RStudio in NoMachine.

lidar_files_puhti <- function(f_poly){

  # f_poly - the path to a polygon layer with polygons covering an area from
  #          you want LiDAR files collected

  library(raster)

  # The LiDAR dataset in Puhti is located at /appl/data/geo/mml/laserkeilaus/2008_latest/2008_latest.shp
  # You should use the lidar_auto_all.shp index file to spatially look for LiDAR files
  f_lidar_index <- "/appl/data/geo/mml/laserkeilaus/2008_latest/2008_latest.shp"
  lidar_index       <<- shapefile(f_lidar_index)

  # Polygon to get lidar datasets from an area
  f_poly <<- "area_of_interest.shp"
  poly <- shapefile(f_poly)

  # What lidar index tiles intersect with our polygon
  inters <- intersect(lidar_index, poly)
  if (is.null(inters)) {
    print("ERROR: LiDAR tiles do not cover the study area!!!!")
    next
  }

  # From the index file, use the "path" attribute to get the file names of
  # the LiDAR tiles intersecting your area
  files <- vector()
  for (i in 1:length(inters@polygons)){
    file <- paste0("/appl/data/geo/",inters$path[i])
    files <- c(files, file)
  }
  print(files)
  return(files)
}

# Test the function with the example area_of_interest.shp file
# lidar_files <- lidar_files_puhti("./area_of_interest.shp")
# print(lidar_files)
