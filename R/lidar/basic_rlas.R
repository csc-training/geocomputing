library(rlas)
library(foreach)
source("get_lidar_files_function.R")

#####################
#### Some basic rlas functions
#####################

# Get lidar file names 
lidar_files <- lidar_files_taito(f_poly="area_of_interest.shp")
print (lidar_files)

# Get basic information for the files
headers <- vector("list")
for (file in lidar_files){
  headers[[file]] <- readlasheader(file)
}
names(headers)

# View a file data
ex_lidar_data <- readlasdata(lidar_files[1]) # this is a data.frame
tail(ex_lidar_data)
summary(ex_lidar_data)

# Merge files
i <- 1:length(lidar_files)
merged_lidar_data <- foreach(i, .combine='rbind') %do% {
  readlasdata(lidar_files[i])}
