# Automatizing GIS-processes course notebook Rahti files

### creating_csc_notebooks_image.md
  * The documentation for building, modifying and deploying the notebooks image. Read this!
  
### autogis-part1.dockerfile, autogis-part2.dockerfile
  * The docker build files that pull the jupyter notebook docker images
  * Installs python libraries and the jupyter lab git extension with conda 

### build.sh
  * A simple bash script that just tags and builds the dockerfile. Run this locally before pushing to image registry
  * sudo sh build.sh <dockerfile name without extension>

### instance_start_script.sh
  * A simple bash script that runs when the docker container runs
  * Enables Jupyter lab GUI and changes the thread number to 2
  * Downloads the start up script from env variable AUTODOWNLOAD_URL and runs it
