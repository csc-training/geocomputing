FROM jupyter/scipy-notebook

MAINTAINER Johannes Nyman <johannes.nyman@csc.fi>

WORKDIR /opt/app
USER 1000

### Installing the GIS libraries and jupyter lab extensions. Modify this and make sure the conda spell is working
RUN echo "Upgrading conda" \
&& conda update --yes -n base conda  \
&& conda install --yes -c conda-forge -c patrikhlobil \
	python=3.7 \
	pandas \
	geopandas \
	matplotlib \
	pysal \
	mapclassify \
	geojson \
	rasterio \
	contextily \
	folium \
	mplleaflet \
	osmnx \
	patrikhlobil::pandas-bokeh \
	imageio \
	nose \
        pip \
	jupyterlab \
	jupyterlab-git

RUN jupyter lab build

RUN conda clean -afy

USER root

# OpenShift allocates the UID for the process, but GID is 0
# Based on an example by Graham Dumpleton
RUN chgrp -R root /home/jovyan \
    && find /home/jovyan -type d -exec chmod g+rwx,o+rx {} \; \
    && find /home/jovyan -type f -exec chmod g+rw {} \; \
    && chgrp -R root /opt/conda \
    && find /opt/conda -type d -exec chmod g+rwx,o+rx {} \; \
    && find /opt/conda -type f -exec chmod g+rw {} \;

RUN ln -s /usr/bin/env /bin/env

ENV HOME /home/jovyan

COPY ./instance_start_script.sh /usr/local/bin/instance_start_script.sh
RUN chmod a+x /usr/local/bin/instance_start_script.sh

# compatibility with old blueprints, remove when not needed
RUN ln -s /usr/local/bin/instance_start_script.sh /usr/local/bin/bootstrap_and_start.bash

USER 1000

WORKDIR /home/jovyan/work

CMD ["/usr/local/bin/instance_start_script.sh"]

