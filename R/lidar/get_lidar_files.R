library(raster)

# The lidar_index to be used, in this case only year 2013
f_lidar_index <- "/wrk/project_ogiir-csc/mml/laser/Automaattisen luokittelu 2008 - 2016/Automaattinen_luokittelu_indeksi/2013/Export_AUTO_PISTEPILVITIEDOSTO_2013.shp"
lidar_index       <<- shapefile(f_lidar_index)

# Polygon to get lidar datasets from
f_poly <<- "area_of_interest.shp"
poly <- shapefile(f_poly)

# What lidar index tiles intersect with our polygon
inters <- intersect(lidar_index, poly)
if (is.null(inters)) {
  print("ERROR: LiDAR tiles do not cover the study area!!!!")
  next
}

# Query file names are intersecting
files <- vector()
for (i in 1:length(inters@polygons)){
  file <- paste0(inters$TUNNUS[i],".laz")
  files <- c(files, file)
}
print(files)

# Transform to current Taito path
files_taito <- gsub("laser/automaattinen/",
                    "/wrk/project_ogiir-csc/mml/laser/Automaattisen luokittelu 2008 - 2016/", files)
print(files_taito)
