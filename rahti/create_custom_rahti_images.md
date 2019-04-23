# Custom CSC's Notebook's docker images for Notebooks and Rahti
By custom docker images, we mean customized versions of the existing docker images in CSC's [notebook-images repository](https://github.com/CSCfi/notebook-images).

The safest way to get a working custom Rahti/Notebook image is to  start from the available templates in CSC's base images (see `builds` directory).

If you need to customize also your favorite docker images, you can learn from these instructions and apply to your dockerfile. In that case, note that the Notebooks-images dockerfiles contain different commands that make the output images compatible with Rahti and/or Notebooks backends. Make sure that you include those commands in your dockerfile in the correct positions.

**Note** That you should have a docker environment where you are building and testing your the docker images you create from your dockerfiles. See [How to set up a Docker environment](./pouta_docker_factory.md) and [how to test your docker images](./testing_your_container.md).

##  Connecting to CSC's Rahti from command line
In order to be able to upload images and run them as applications in Rahti, you will need to first get an account from Rahti platform, apply from rahti-support@csc.fi.

Run the following commands to set up your project name and the Rahti registry as variable (these are used by the notebooks-images scripts).
```shell
# Set your project as variable
export OSO_PROJECT=<your-project-name>
# Set Rahti's docker registry name and your project as variables
export OSO_REGISTRY=docker-registry.rahti.csc.fi
```

To use Rahti from the command line with the `oc` tools,  you will need to get your API credentials. For that, log in to your Rahti project at https://rahti.csc.fi and copy your access token (from upper right menu). Connect to Rahti and its registry with:
```
# Login to Rahti from the terminal...
oc login https://rahti.csc.fi:8443 --token=Askfhjf-this-is-an-arbitrary-example-key-hbpkLpAhagk76fVDX0dh4LFAasd99+asdV4

# Check that you are logged in to Rahti
oc whoami -t

# Activate your project
oc project $OSO_PROJECT

# Login to Rahti's registry from docker
docker login -u ignored -p $(oc whoami -t) $OSO_REGISTRY
```

## Building your custom docker images using the readilly available scripts
Build your docker images by modifying the template dockerfiles in [notebook-images repository's](https://github.com/CSCfi/notebook-images/tree/master/builds) to your needs.

After you have gotten your dockerfile ready, you will need to build the image locally, test it and upload to Rahti:
* to build your image, use the `build.sh` script. It will build locally your docker image:
```shell
cd builds
sh build.sh <dockerfile-name-without-extension>
```

You can run and test this image in your local Docker environment. See some instructions in [test your docker container](testing_your_container.md).

## Manually upload your image to Rahti
To upload your image to Rahti, it is necessary that you tag your image with Rahti:
```shell
docker tag csc/<your-image-name>:latest docker-registry.rahti.csc.fi/<your-rahti-project-name>/<your-image-name>:latest
```
Then push your image to Rahti's registry with:
```shell
docker push docker-registry.rahti.csc.fi/<your-rahti-project-name>/<your-image-name>:latest
```

After your custom image has been uploaded, you can start your application from the Rahti paltform and check that your custom container is running as expected as a Rahti application.

## Using the Notebooks' scripts to upload your image to Rahti
You may need to modify the scripts for them to work with your specific docker images' naming:

* If you need to upload it to the Rahti platform, use the `build_and_upload_to_openshift.bash` script. It will build your image locally and upload it to Rahti when ready:
```shell
cd builds
./build_and_upload_to_openshift.bash <dockerfile-name-without-extension>
```

* Alternatively, you could send your dockerfile to the Rahti platform for the image to be built directly to the platform (no local build at all). That will free  your computer resources but you will need to make all tests inside the Rahti platform which requires that you know how to use it and has limitations for testing (no `sudo` rights):
```shell
cd builds
./build_openshift.bash <dockerfile-name-without-extension>
```

See more instructions at [notebook-images repository](https://github.com/CSCfi/notebook-images/tree/master/builds).
