# Notebooks & Rahti

[CSC Notebooks](https://notebooks.csc.fi) is a service where you can launch notebooks instances that are hosted in Rahti. You need to create the docker containers yourself and upload them to the Rahti container registry.

For hosting your own notebook container in notebooks.csc.fi, you need at least

- a CSC project and a Rahti project (create them in my.csc.fi and rahti.csc.fi)
- Group ownership rights on notebooks.csc.fi (e-mail to servicedesk@csc.fi)
- docker and openshift command line tools installed to your computer 

## Windows machine

Installing Docker to a Windows machine can be cumbersome and you need admin priviledges. If this is not possible, a good option is to [launch a small Linux cPouta virtual machine](https://github.com/csc-training/geocomputing/tree/master/pouta/docker-applications) and build the containers there.

## Creating a notebooks image

Detailed tutorial how to create a notebooks docker image can be found in the [course_notebooks folder](course_notebooks/creating_csc_notebooks_image.md)
