## Use get_lidar_files_function to get LiDAR files for a area of interest
## and rlas to read and merge the LiDAR data

library(rlas)
library(foreach)
source("get_lidar_files_function.R")

# Get lidar file names
lidar_files <- readLines("las_files.txt")
print(lidar_files)

# Get basic information from the LiDAR files
headers <- vector("list")
for (file in lidar_files){
  headers[[file]] <- read.lasheader(file)
}
names(headers)

# Preview the LiDAR data for the first file in the list
lidar_data <- read.las(lidar_files[1]) # this is a data.frame
tail(lidar_data)
summary(lidar_data)

# Merge the LiDAR files into a single R data frame
i <- 1:length(lidar_files)
merged_lidar_data <- foreach(i, .combine='rbind') %do% {
  read.las(lidar_files[i])}
