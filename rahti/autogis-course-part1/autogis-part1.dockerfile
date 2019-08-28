FROM jupyter/datascience-notebook

MAINTAINER Johannes Nyman <johannesnyman@csc.fi>

USER $NB_USER

# Set working directory to /opt/app
WORKDIR /opt/app
USER 1000

### Installing the GIS libraries. Modify this and make sure the conda spell is working
RUN echo "Upgrading conda" \
&& conda update --yes -n base conda  \
&& conda install --yes -c conda-forge \
	python=3.7 \
	pandas \
	geopandas \
	matplotlib \
        pip

### Installing the jupyter lab git extension
RUN echo "Installing jupyter lab Git extension"
RUN jupyter labextension install @jupyterlab/git \
&& pip install --upgrade jupyterlab-git \
&& jupyter serverextension enable --py jupyterlab_git \
&& jupyter lab build

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

### Copy the script that runs when container is launched
COPY ./instance_start_script.sh /usr/local/bin/instance_start_script.sh

### Set starting directory for the jupyter notebook
RUN mkdir -p /home/jovyan/work \
    && sed -i "s/#c.NotebookApp.notebook_dir =.*/c.NotebookApp.notebook_dir = '\/home\/jovyan\/work\/'/g" /home/jovyan/.jupyter/jupyter_notebook_config.py

RUN chmod a+x /usr/local/bin/instance_start_script.sh

USER 1000

# Copy the docker image creation files for reference
COPY . /opt/app

# Go back to student starting folder (e.g. the folder where you would also mount Rahti's persistant folder)
WORKDIR /home/$NB_USER/work

CMD ["/usr/local/bin/instance_start_script.sh"]

