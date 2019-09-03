# Automatizing GIS-processes course notebook Rahti files

### autogis-part1.dockerfile
  * The docker build file that pulls the jupyter notebook docker image 
  * Installs python libraries and the jupyter lab git extension with conda 

### build.sh
  * A simple bash script that just tags and builds the dockerfile. Run this locally before pushing to image registry
  * sudo sh build.sh <dockerfile name without extension>

### instance_start_script.sh
  * A simple bash script that runs when the docker container runs
  * Enables Jupyter lab GUI and changes the thread number to 2
  * Downloads the start up script from env variable AUTODOWNLOAD_URL and runs it
