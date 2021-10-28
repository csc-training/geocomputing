FROM jupyter/minimal-notebook@sha256:48d6dc093011c0a93b436f328cdf6da412c0a89db31b54f475d19140f0b0b466

MAINTAINER Dave Whipp <david.whipp@helsinki.fi>

WORKDIR /opt/app
USER 1000

### Installing the GIS libraries and jupyter lab extensions. Modify this and make sure the conda spell is working
RUN echo "Upgrading conda" \
&& conda update --yes -n base conda  \
&& conda install --yes -c conda-forge -c patrikhlobil \
    python=3.8 \
    pandas \
    matplotlib \
    patrikhlobil::pandas-bokeh \
    imageio \
    nose \
    pip \
    jupyterlab \
    jupyterlab-git \
    ipykernel>=6

#RUN jupyter lab build
RUN jupyter lab build --dev-build=False --minimize=False

USER root

# OpenShift allocates the UID for the process, but GID is 0
# Based on an example by Graham Dumpleton
RUN chgrp -R root /home/jovyan \
    && find /home/jovyan -type d -exec chmod g+rwx,o+rx {} \; \
    && find /home/jovyan -type f -exec chmod g+rw {} \; \
    && chgrp -R root /opt/conda \
    && find /opt/conda -type d -exec chmod g+rwx,o+rx {} \; \
    && find /opt/conda -type f -exec chmod g+rw {} \;

# Create symlink if it does not exist
RUN if [ ! -e /bin/env ];then ln -s /usr/bin/env /bin/env;fi

ENV HOME /home/jovyan

COPY ./instance_start_script.sh /usr/local/bin/instance_start_script.sh
RUN chmod a+x /usr/local/bin/instance_start_script.sh

# compatibility with old blueprints, remove when not needed
RUN ln -s /usr/local/bin/instance_start_script.sh /usr/local/bin/bootstrap_and_start.bash

USER 1000

WORKDIR /home/jovyan/work

CMD ["/usr/local/bin/instance_start_script.sh"]

