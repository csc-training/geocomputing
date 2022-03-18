# Notebooks & Rahti

[(Old) CSC Notebooks](https://notebooks.csc.fi) and the new [CSC Notebooks 5 beta](https://notebooks-beta.rahtiapp.fi/welcome) is a service where you can launch notebooks instances that are hosted in Rahti. You can either use existing [notebooks containers](https://github.com/CSCfi/notebook-images/tree/master/builds) or, if you have special requirements, you can also create the docker containers yourself and upload them to the Rahti container registry.

For hosting your own notebook container in notebooks.csc.fi, you need at least

- a CSC project and a Rahti project (create them in my.csc.fi and rahti.csc.fi)
- Group ownership rights on notebooks.csc.fi (e-mail to servicedesk@csc.fi)
- docker and openshift command line tools installed to your computer 

## Windows machine

Installing Docker to a Windows machine can be cumbersome and you need admin priviledges. If this is not possible, a good option is to [launch a small Linux cPouta virtual machine](https://github.com/csc-training/geocomputing/tree/master/pouta/docker-applications) and build the containers there.

## Creating a notebooks image

Detailed tutorial how to create a notebooks docker image for old Notebooks can be found in the [notebooks_old folder](./notebooks_old/creating_autogis_notebooks_image.md).
A tutorial for the new Notebooks 5 can be found in [ notebooks_5_instructions](./notebooks_5_instructions.md) with an exmaple [dockerfile](./example.dockerfile).
