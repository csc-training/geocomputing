# use jupyter minimal notebook as base for your image
# it has eg conda already installed
FROM jupyter/minimal-notebook

# Set maintainer
LABEL maintainer="Dave Whipp (david.whipp@helsinki.fi)"

#some first setup steps need to be run as root user
USER root

# set home environment variable to point to user directory
ENV HOME /home/$NB_USER

# install needed extra tools, eg ssh-client and less
RUN apt-get update \
    && apt-get install -y ssh-client less \
    && apt-get clean

# the user set here will be the user that students will use 
USER $NB_USER

### Installing the needed conda packages and jupyter lab extensions. 
# Run conda clean afterwards in same layer to keep image size lower
# NOTE: jupyterlab is pinned to 3.6.6 because the jupyterlab-git plugin does
#       not yet work for jupyterlab 4
RUN conda install --yes -c conda-forge \
    python=3.11 \
    numpy \
    scipy \
    xarray \
    pandas \
    matplotlib \
    nose \
    pip \
    jupyterlab=3.6.6 \
    jupyterlab-git \
    ipykernel \
  && conda clean -afy

#RUN jupyter lab build
RUN jupyter lab build --dev-build=False --minimize=False