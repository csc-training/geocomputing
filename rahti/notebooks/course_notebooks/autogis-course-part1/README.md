# Automating GIS processes (and related) course notebook Rahti files

## Documentation

`creating_csc_notebooks_image.md`
- The documentation for building, modifying and deploying the notebooks image. Read this!

## Files for creating Docker images

- The docker build files that pull the jupyter notebook docker images
- Installs python libraries and the jupyter lab git extension with conda 

### Available dockerfiles

- `geo-python.dockerfile`: AutoGIS 1/Geo-Python 2021
- `introqg.dockerfile`: Introduction to Quantitative Geology 2021
- `autogis-part1.dockerfile`: AutoGIS 1/Geo-Python 2020
- `autogis-part2.dockerfile`: AutoGIS 2 2020

## Other build files

`build.sh`

- A simple bash script that just tags and builds the dockerfile. Run this locally before pushing to image registry
- `sudo sh build.sh <dockerfile name without extension>`

`instance_start_script.sh`

- A simple bash script that runs when the docker container runs
- Enables Jupyter lab GUI and changes the thread number to 2
- Downloads the start up script from env variable `AUTODOWNLOAD_URL` and runs it

## Notes

- Building locally on my Mac I did not need to use `sudo` for any of the steps here or in the 
`creating_csc_notebooks_image.md` document
