## Installing OpenDroneMap

Docker applications can be used in different ways often depending on how the application has been constructed.

In the case of OpenDronemap, it is implemented so that you can run the application directly from the docker container's starting command for which you simply need to havwe docker installed, an internet connection,  the input dataset and know the OpenDroneMap parameters you want to use.

So the following command will download the OpenDroneMap application (only the first time you call for this docker image), calculate a mosaic and save it to the output folder. When the computation is finished it will delete the container application freeing resources in the virtual machine:
```bash
# Download the opendronemap docker image
sudo docker pull opendronemap/opendronemap

# Check that the image has been added to your Docker
sudo docker images

#Run the opendronemap process:
# go to your dataset folder so that you are one level below the images/ folder
cd odm_data_aukerman/

# Use the **screen** command to start a detachable terminal (= you can close the terminal and the process keeps running)
screen –S running\_odm

# Finally run the opendronemap command (use the **time** command to get info on how long it run):
time sudo docker run -it --rm \
    -v "$(pwd)/images:/code/images" \
    -v "$(pwd)/odm_orthophoto:/code/odm_orthophoto" \
    -v "$(pwd)/odm_georeferencing:/code/odm_georeferencing" \
    opendronemap/opendronemap \
    --mesh-size 100000
```

You can see more information about running the OpenDroneMap application as a docker application from:

[https://github.com/OpenDroneMap/ODM/wiki/Docker](https://github.com/OpenDroneMap/ODM/wiki/Docker)

See the OpenDroneMap official documentation to learn about the parameters and how to use the docker application: [https://docs.opendronemap.org/using.html#docker](https://docs.opendronemap.org/using.html#docker)
