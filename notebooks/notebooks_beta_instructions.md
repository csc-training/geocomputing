# Custom notebooks image for Notebooks beta

Requirements: 
* own CSC user account with Rahti access
* docker

## Step-by-step

1. Become a workspace owner
Send your CSC user account name to `notebooks@csc.fi` to request Notebooks workspace owner rights.

2. Login to https://notebooks-beta.rahtiapp.fi/welcome

3. Check that you got workspace ower rights
It worked, if you see 'Manage workspaces' tab in the left panel

4. Create custom notebooks image
If you cannot use any of the [provided images](https://github.com/CSCfi/notebook-images/tree/master/builds) but want to use your own notebooks image, you will need to create an image using Docker and host it on Rahti. 
4.1 Create Docker file

For Jupyter Lab with some conda packages use the following as minimal example:

```text xxcourse.dockerfile
# use jupyter minimal notebook as base for your image, it has eg conda already installed
FROM jupyter/minimal-notebook

# add your name as maintainer, with your email address for future questions
MAINTAINER your-name-here

#some first setup steps need to be run as root user
USER root

# OpenShift allocates the UID for the process, but GID is 0
# Based on an example by Graham Dumpleton
# and test that it worked
RUN chgrp -R root /home/$NB_USER \
    && find /home/$NB_USER -type d -exec chmod g+rwx,o+rx {} \; \
    && find /home/$NB_USER -type f -exec chmod g+rw {} \; \
    && chgrp -R root /opt/conda \
    && find /opt/conda -type d -exec chmod g+rwx,o+rx {} \; \
    && find /opt/conda -type f -exec chmod g+rw {} \;

RUN test -f /bin/env || ln -s /usr/bin/env /bin/env

# set home environment variable to point to user directory
ENV HOME /home/$NB_USER

# copy separate script to do needed setups into environment (can be found: https://raw.githubusercontent.com/CSCfi/notebook-images/master/builds/scripts/jupyter/autodownload_and_start.sh) and make executable
COPY scripts/jupyter/autodownload_and_start.sh /usr/local/bin/autodownload_and_start.sh
RUN chmod a+x /usr/local/bin/autodownload_and_start.sh

# install needed extra tools, eg ssh-client and less
RUN apt-get update \
    && apt-get install -y ssh-client less \
    && apt-get clean

# make sure conda is up-to-date
RUN conda update --yes -n base conda  

# the user set here will be the user that students will use when working in the notebook
USER $NB_USER

# conda installations should go in /opt/app, which is set as workdir here
WORKDIR /opt/app

### Installing the needed conda packages and jupyter lab extensions. And run conda clean afterwards in same layer 
RUN conda install --yes -c conda-forge \
  && conda clean -afy

#jupyter lab build
RUN jupyter lab build --dev-build=False --minimize=False

# the directory set here will be the home folder within jupyter lab 
WORKDIR $HOME

# execute separate script to do needed setups
CMD ["/usr/local/bin/autodownload_and_start.sh"]
```

4.2 Build the image from dockerfile to current directory (.)
`docker build -t "<yourimagename>" -f <yourimagename>.dockerfile .`

4.3 Send your image to Rahti registry
4.3.1 Login to https://registry-console.rahti.csc.fi/ 
4.3.2 Find the `login commands` on the `Overview` page and use one of them to login to Rahti registry from command line
4.3.3 Create a new project on Rahti webpage (or re-use one that you already have)
4.3.4 Tag your docker image, eg based on versions (here: v0.1)
`sudo docker tag <yourimagename> docker-registry.rahti.csc.fi/<yourrahtiproject>/<yourimagename>:v0.1`
4.3.5 Push your docker image to Rahti registry
`sudo docker push docker-registry.rahti.csc.fi/<yourrahtiproject>/<yourimagename>`

4.4 In Notebooks: Create a workspace and within that, create new application
Notebooks > Manage workspaces using the `Application wizard` or `Application form`

4.4.1 Choose any `Application template` (check for different basic settings (lifetime and memory))
4.4.2 Give a meaningful `Application name` , eg `Geospatial Python course 2022`, this is the name under which participants will see the notebook in the list of notebooks
4.4.3 Add a short `Description`
4.4.4 Add/remove `Category labels` that fit with your notebook
4.4.5 Choose if you want Jupyter Lab or Jupyter Notebooks interface
4.4.6 Fill in the link to your image on Rahti under `Container image` ( You can find the link from Rahti web interface > projectname > imagename > Pulling repository, e.g. `docker-registry.rahti.csc.fi/<yourprojectname>/<yourimagename>:<tagyouwanttouse>`
4.4.7 Choose a `download method` if you want to download files at notebook startup directly into students home directory, e.g. code used during the course that is available on github
4.4.8 Choose if you want to have a persistent my-work folder for each student (nice for multiday courses, when students create files during the course)
4.4.9 Choose if you want to publish or save as draft for testing. Publish means that everyone with a join code could find it, but it will never appear for every notebooks user on the home page.

4.5 Test your application
4.6 Share the join code (Notebooks > Manage Workspaces > Join code) with course participants




