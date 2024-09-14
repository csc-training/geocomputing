# Use Rocker RStudio as base for your image
FROM rocker/rstudio:4.2.0

# copy the desired installation script into docker file system, make sure that you have execute rights to the script
COPY install_rspatial_geospatial.sh /rocker_scripts/

# install the custom packages and system dependencies by running the script
RUN /rocker_scripts/install_rspatial_geospatial.sh





   



