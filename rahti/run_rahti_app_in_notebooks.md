# Running containers in CSC's Notebooks platform
One way of distributing a Docker container application for example for a course, is using CSC's Notebooks platform to launch your Rahti containers.

## Get Group Owner rights for Notebooks
To be able to set up your Rahti application in Notebooks you need:
- **First of all, apply for group owner rights** by sending a free from email to *sevicedesk@csc.fi*
- See the [Group Owner's Guide documentation](http://cscfi.github.io/pebbles/group_owners_guide.html) for Pebbles platform (CSC's Notebooks is an implemetation of [Pebbles](https://github.com/CSCfi/pebbles))

## Create a Rahti Blueprint
Create a `blueprint` in Notebooks using a template that uses Rahti. This allows you to give the name of the Raht's image that will be used to create the instances.

The format of the Rahti's image link is:
```
docker-registry.rahti.csc.fi/<your-project-name>/<your-image-name>:latest
```
Use this link in the `Image` field when creating the blueprint.

## Using large Docker images
If your images are several Gb in size, you should consider wa

The first time that an image is used in the Rahti platform, the image needs to be copied to the specific node where the application will be run. This is true for every node of Rahti's platform (the images are not copied by default to all possible nodes). For this reason, the first time you deploy an application from a large image, it will take several minutes to start.

When you start a container from Notebooks, a deployment is done in Rahti and the above mentioned delay will be noticeable. If you want to overcome this issue, you will need to "warm up" Rahti by forcing the upload of your image to Rahti's nodes.
Also, if your image is large enough you will need to modify the timeout setting of your deployment in Rahti (default is 600 seconds):
- create a new app in Rahti (Deploy Image) and while it is starting click in the name of the deployment and then in `Configuration`. Set the timeout parameter to for ex. 6000
- "warm up" Rahti: set also the number of `Replicas` to 20.

Go back to History and click on the newest deployment version for ex. `#1`. There you can inspect the creation of your apps.

**Remember to delete your replicas** once they have started (and effectively uploaded the image to Rahti´s nodes). Simply change the number of replicas to 1 (or even 0). You can keep the deployment active in Rahti in case you need to repeat the warm up.
