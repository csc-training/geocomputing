# CSC's Rahti guidelines for custom Notebook's images
Guidelines and examples about using CSC's Rahti platform to provide customized images mainly meant to be served via CSC's Notebooks.

**Note** that to be able to follow these guidelines you will need at least:
- have an active account in [rahti.csc.fi](https://rahti.csc.fi/)
- basics of working with the Rahti platform and using the OpenShift command line tools
- basic skills with [Docker](https://docs.docker.com/) and dockerfiles
- a working environment with the necessary Docker and OpenShift tools (see below)

Guidelines:
- [Docker environment](./pouta_docker_factory.md) - setting up a dedicated Docker environment locally or in a Pouta VM
- [Create a custom container](./create_custom_rahti_images.md) - Basic scripts to create and upload Rahti's and Notebooks images
- [test your container](./testing_your_container.md) - Manually build, test and upload images
- [start an application in Rahti](start_rahti_app.md)
- [Running containers in CSC's Notebooks platform](./run_rahti_app_in_notebooks.md) - if you are granted **group owner rights to [CSC's Notebooks platform](http://notebooks.csc.fi)** you would be able to distribute your rahti applications from its web graphical interface.
