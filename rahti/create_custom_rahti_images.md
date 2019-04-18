# Custom CSC's Notebook's docker images for Notebooks and Rahti
By custom docker images, we mean customized versions of the existing docker images in CSC's [notebook-images repository](https://github.com/CSCfi/notebook-images).

The safest way to get a working custom Rahti/Notebook image is to  start from the available templates in CSC's base images (see `builds` directory).

If you need to customize also your favorite docker images, you can learn from these instructions and apply to your dockerfile. In that case, note that the Notebooks-images dockerfiles contain different commands that make the output images compatible with Rahti and/or Notebooks backends. Make sure that you include those commands in your dockerfile in the correct positions.


##  Connecting to CSC's Rahti from command line
IN order to be able to upload images and run them as applications in Rahti, you will need to first get an account from Rahti platform, apply from rahti-support@csc.fi.

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

After you have gotten your dockerfile ready, you will need to build the images or/and upload to Rahti:
* for Notebook backend, use builds/build.sh -> will build locally your docker image
```shell
cd builds
sh build.sh <dockerfile-name-without-extension>
```
You can run and test this image in your local Docker environment. See some instructions in [test your docker container](testing_your_container.md).

* for Rahti backend, use build_and_upload_to_openshift.bash -> will upload your dockerfile to Rahti and build the image directly in the platform:
```shell
cd builds
./build_and_upload_to_openshift.bash <dockerfile-name-without-extension>
```
 See more instructions at [notebook-images repository](https://github.com/CSCfi/notebook-images/tree/master/builds).


 After your custom image has been uploaded, you can start your application from the Rahti paltform and check that your custom container is running as expected as a Rahti application.
