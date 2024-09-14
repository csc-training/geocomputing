#!/bin/bash
set -e

# always set this for scripts but don't declare as ENV..
export DEBIAN_FRONTEND=noninteractive

## build ARGs
NCPUS=${NCPUS:--1}

# a function to install apt packages only if they are not installed
function apt_install() {
    if ! dpkg -s "$@" >/dev/null 2>&1; then
        if [ "$(find /var/lib/apt/lists/* | wc -l)" = "0" ]; then
            apt-get update
        fi
        apt-get install -y --no-install-recommends "$@"
    fi
}

apt_install \
    gdal-bin \
    lbzip2 \
    libfftw3-dev \
    libgdal-dev \
    libgeos-dev \
    libgsl0-dev \
    libgl1-mesa-dev \
    libglpk-dev \
    libglu1-mesa-dev \
    libhdf4-alt-dev \
    libhdf5-dev \
    libjq-dev \
    libpq-dev \
    libproj-dev \
    libprotobuf-dev \
    libnetcdf-dev \
    libsqlite3-dev \
    libssl-dev \
    libudunits2-dev \
    libxt-dev \
    netcdf-bin \
    postgis \
    protobuf-compiler \
    sqlite3 \
    tk-dev \
    unixodbc-dev \
    wget
    

install2.r --error --skipmissing --skipinstalled -n "$NCPUS" \
    raster \
    lubridate \
    paletteer \
    sf \
    tidyverse \
    rmapshaper \
    spdep \
    spatstat \
    mapview \
    mapedit \
    fpc \
    GWmodel \
    NbClust \
    osmdata \
    terra \
    patchwork \
    exactextractr \
    fasterize \
    rstac \
    httr \
    gdalcubes \
    ncf \
    inlmisc \
    elsa \
    tmap 
    
#R -e "remotes::install_github('USGS-R/inlmisc', dependencies = TRUE)"

#R -e "BiocManager::install('rhdf5')"

## install wgrib2 for NOAA's NOMADS / rNOMADS forecast files
## This is no longer needed, but we include it for reproducibility
## reasons on earlier base images.
#source /etc/os-release
#if [ "${UBUNTU_CODENAME}" == "focal" ]; then
#    /rocker_scripts/install_wgrib2.sh
#fi

# Clean up
rm -rf /var/lib/apt/lists/*
rm -r /tmp/downloaded_packages

## Strip binary installed lybraries from RSPM
## https://github.com/rocker-org/rocker-versioned2/issues/340
strip /usr/local/lib/R/site-library/*/libs/*.so

