FROM jupyter/minimal-notebook

WORKDIR /opt/app
USER 1000

COPY ./gis_ml_environment.yml /usr/local/etc/gis_ml_environment.yml

### Installing the GIS libraries and jupyter lab extensions. Modify this and make sure the conda spell is working
RUN echo "Upgrading conda" \
&& conda update --yes -n base conda  \
&& conda env update --file /usr/local/etc/gis_ml_environment.yml

RUN jupyter lab build

USER root

# OpenShift allocates the UID for the process, but GID is 0
# Based on an example by Graham Dumpleton
RUN chgrp -R root /home/jovyan \
    && find /home/jovyan -type d -exec chmod g+rwx,o+rx {} \; \
    && find /home/jovyan -type f -exec chmod g+rw {} \; \
    && chgrp -R root /opt/conda \
    && find /opt/conda -type d -exec chmod g+rwx,o+rx {} \; \
    && find /opt/conda -type f -exec chmod g+rw {} \;

ENV HOME /home/jovyan

COPY ./instance_start_script.sh /usr/local/bin/instance_start_script.sh
RUN chmod a+x /usr/local/bin/instance_start_script.sh

USER 1000

WORKDIR /home/jovyan/work

CMD ["/usr/local/bin/instance_start_script.sh"]

