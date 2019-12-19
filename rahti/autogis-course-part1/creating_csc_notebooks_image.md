# An Example how a notebooks environment was setup for a GIS course held by the university of Helsinki autumn 2019

## First you should have docker and openshift command line tools (oc) installed

https://docs.docker.com/v17.09/engine/installation/
https://docs.openshift.com/container-platform/3.11/cli_reference/get_started_cli.html

## Clone the course docker files 

`git clone https://github.com/csc-training/geocomputing.git`
`cd rahti/autogis-course-part1`

## Make changes to the .dockerfile

* e.g. add/remove python libraries to the conda install command

## Now that we made changes we need to build the docker container again

* Run the build.sh script with 
`sudo sh build.sh`

## The docker container now lives on your local docker registry

* You can check all built local docker containers with
`sudo docker image ls`

* Remember to delete images now an then if you use docker a lot. They take a lot of space! 
`sudo docker prune`

* You can test your container locally with 
`sudo docker run -p 8888:8888 csc/autogis-part1`

* Now you can open up browser and navigate to localhost:8888 and jupyter lab should open

## Now that we know the docker image runs succesfully we can send it anywhere where docker is installed and it should work as well

### Send it to Rahti image registry:

* First declare some environment variables that tell the system where to send the image (Rahti specific)
`export OSO_PROJECT=geo-python-course`
`export OSO_REGISTRY=docker-registry.rahti.csc.fi`

* Login to https://registry-console.rahti.csc.fi/ and copy the token text visible on the front page under Login commands
* Login to the Rahti docker image registry from docker and oc (openshift command line tools)
`sudo docker login -p <token_from_rahti_registry_website> -u unused docker-registry.rahti.csc.fi`
`oc login --token <token_from_rahti_registry_website> rahti.csc.fi:8443`

* Tag the image your sending to the registry. This tag would make it possible to have different images for the same service. "latest" is the default tag

`sudo docker tag csc/autogis-part1 docker-registry.rahti.csc.fi/geo-python-course/autogis-part1:latest`

* Push (send) the image to the image registry

`sudo docker push docker-registry.rahti.csc.fi/geo-python-course/autogis-part1:latest`

### Deploy the uploaded image in Rahti and attach the route (url address)

* Go to rahti.csc.fi -> Web user interface -> Choose your project

* "Add to project" (top right) -> Deploy image -> Choose your image -> Deploy

### Add route for the object 

* Applications (left) -> Routes -> Create Route (top right) -> Fill only "Name" and "Service"

### (optional) Add persistent storage (note, the glusterfs file system is in review! It has had some issues)

* Create persistent storage and attach it to the deployment

* Storage (left) -> Create Storage (top right) -> Storage Class: glusterfs, Name: unique name, Access Mode: RWO, Size: 500mb-1GB
    
* Attach it to the deployment. Applications -> deployment -> click the name of the deployment -> Configuration -> Under "Volumes" Add Storage -> Choose the storage you created and add the mounting point (path) where this storage is to be added. In the CSC notebooks it should be /home/jovyan/work

### Making the notebooks container load faster for students

* It is possible to speed up the loading of a notebooks instance by preloading the image to Rahti pods
* This is done by increasing the pod replicas temporarily to the max number of simultaneous instances (number of students)
* In Rahti web console: Applications -> Deployments -> The version number of your current deployment (e.g #28) -> Replicas -> Edit (pen symbol) -> increase to the number of students -> After the pods have started succesfully, bring them down again to 1

### Updating notebooks image

* You only need to do the deployment the first time manually. After that every time you send a new image to the registry Rahti deploys it automatically
* So if you want to e.g add a Python library to your environment, you can just make changes to the .dockerfile, build the container again locally and send it to Rahti image registry and the notebooks instance will update automatically