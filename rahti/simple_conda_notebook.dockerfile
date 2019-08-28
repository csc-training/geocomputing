FROM jupyter/datascience-notebook

MAINTAINER Olli Tourunen <olli.tourunen@csc.fi>

# Modified from pb-jupyter-datascience.dockerfile

USER $NB_USER

# Set working directory to /opt/app
WORKDIR /opt/app

# GIS env installation

USER 1000
# Set git
#ENV GIT_COMMITTER_NAME=anonymous
#ENV GIT_COMMITTER_EMAIL=anon@localhost
#RUN git clone https://github.com/geo-python/JupyterLab-environment-test.git /home/jovyan/work/#JupyterLab-environment-test


RUN echo "Upgrading pip and conda" \
&& pip --no-cache-dir install --upgrade pip \
&& conda update --yes -n base conda  \
&& conda install --yes \
	pandas \
	geopandas \
	networkx

RUN echo "Libraries installed!"

USER root

# OpenShift allocates the UID for the process, but GID is 0
# Based on an example by Graham Dumpleton
RUN chgrp -R root /home/$NB_USER \
    && find /home/$NB_USER -type d -exec chmod g+rwx,o+rx {} \; \
    && find /home/$NB_USER -type f -exec chmod g+rw {} \; \
    && chgrp -R root /opt/conda \
    && find /opt/conda -type d -exec chmod g+rwx,o+rx {} \; \
    && find /opt/conda -type f -exec chmod g+rw {} \;

RUN ln -s /usr/bin/env /bin/env

ENV HOME /home/$NB_USER

COPY scripts/jupyter/autodownload_and_start.sh /usr/local/bin/autodownload_and_start.sh

# Set starting directory for the jupyter notebook
RUN mkdir -p /home/jovyan/work \
    && sed -i "s/#c.NotebookApp.notebook_dir =.*/c.NotebookApp.notebook_dir = '\/home\/jovyan\/work\/'/g" /home/jovyan/.jupyter/jupyter_notebook_config.py

RUN chmod a+x /usr/local/bin/autodownload_and_start.sh

# compatibility with old blueprints, remove when not needed
RUN ln -s /usr/local/bin/autodownload_and_start.sh /usr/local/bin/bootstrap_and_start.bash

USER 1000

# Copy the docker image creation files for reference
COPY . /opt/app

# Go back to student starting folder (e.g. the folder where you would also mount Rahti's persistant folder)
WORKDIR /home/$NB_USER/work

CMD ["/usr/local/bin/autodownload_and_start.sh"]
