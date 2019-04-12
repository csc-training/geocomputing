# Custom docker images in Rahti

## Building your custom docker images
Build your docker images by modifying the example dockerfiles to your needs and by following [notebook-images repository's instructions](https://github.com/CSCfi/notebook-images/blob/master/builds/build.sh). For example:
  1. for Notebook backend, use builds/build.sh
  2. for Rahti backend, use build_and_upload_to_openshift.bash


## Connecting to CSC's Rahti from command line
You will need to first get an account from Rahti platform, apply from rahti-support@csc.fi.

Log in to your Rahti project at https://rahti.csc.fi and copy you access token (from upper right menu).

To log in to CSC's Rahti from your command line:
```
# Set Rahti's docker registry name and your project as variables
export OSO_REGISTRY=docker-registry.rahti.csc.fi
export OSO_PROJECT=your_project_name

# Login to Rahti from the terminal...
oc login https://rahti.csc.fi:8443 --token=AshbpkLpAhagk76fVDX0dh4LFAasd99+asdV4

# Check that you are logged in to Rahti
oc whoami -t

# Login to Rahti from docker
docker login -u ignored -p $(oc whoami -t) $OSO_REGISTRY

# Activate your project
oc project $OSO_PROJECT
```

To upload your image to Rahti:
```
./build_and_upload_to_openshift.bash pb-jupyter-minimal
```

### Uploading a modified container as image
To upload an image created from a container:
```
# Save your container as an image in docker
docker commit container_name csc/container_name_img

# Set the Rahti registry name as a variable
export oso_registry_base="$OSO_REGISTRY/$OSO_PROJECT"
echo $oso_registry_base

# Set the tag of your image to the Rahti registry name
docker tag csc/container_name_img $oso_registry_base/container_name_img

# Push the image to rahti
docker push $oso_registry_base/container_name_img
```

Your image should be visible in your Rahti web interface. You ready to create applications from it.
