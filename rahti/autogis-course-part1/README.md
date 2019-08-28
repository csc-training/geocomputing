# Automatizing GIS-processes course notebook Rahti files

### autogis-part1.dockerfile
  * The docker build file that pulls jupyter notebook docker image 
  * Installs python libraries with conda and the jupyter lab git extension 

### build.sh
  * A simple bash script that just tags and builds the dockerfile. Run this locally before pushing to image registry

### instance_start_script.sh
  * A simple bash script that runs when the docker container runs
  * Enables Jupyter lab GUI
  * Clones the lecture notebooks from https://github.com/geo-python/notebooks.git
