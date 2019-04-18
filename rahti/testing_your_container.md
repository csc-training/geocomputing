# Testing custom CSC's Notebook's docker images for Notebooks and Rahti

 To get more control over the docker image you will be deploying in Rahti, you may want to create the image in your computer and upload the tested image to Rahti manually.

 This is specially important when you consider that creating a Rahti compatible docker image has a step that may take quite long (the part starting with `RUN chgrp -R root /home/...`). Running the whole script everytime you do little modifications to the dockerfile would require long waiting between tests.

 Rather, you could build the docker image once.
```shell
sh build.sh <dockerfile-name-without-extension>
```

 Then create the container:
 ```shell
 # For a jupyter docker container
 sudo docker run -d -p 8888:8888 <container-name>
 # See your container at http://<vm-ip>:8888
 # (maker sure that your VM security groups/firewalls allow connection to port 8888)
 ```

Next test your installation steps manually by loggin to your container:
```shell
# to login as root
docker exec -u root -it <container-name> /bin/bash     
# to login as the default "jovyan" user
docker exec -it <container-name> /bin/bash
# do your installations, note that the underlying system in Jupyter Notebooks is an Ubuntu system

# Make a record of the installations that you have been doing, you can use "history" command (note that for jovyan and roon the history is different)
```

Once you have tested your installations (without having to rebuild your docker image), replicate the installation steps into the dockerfile you are customizing (put your edits before `RUN chgrp -R root /home/...`). When you are done, build the new docker image with the `build.sh` script as earlier. Create a new container and test that the installation is working as expected.
