# Custom CSC's Notebook's docker images for Notebooks and Rahti
By custom docker images, we mean customized versions of the existing docker images in CSC's [notebook-images repository](https://github.com/CSCfi/notebook-images/blob/master). You can addapt these instructions to customize your favorite docker images. Note that the custom images in Notebooks-images dockerfiles contain different commands that make the image compatible with Rahti or Notebooks backend. If you want to use other dockerfiles as a starting point, see that these commands are included in your dockerfile in the correct position. Easiest is to start from the mentioned CSC's base images (see /builds directory).

## Building your custom docker images using the readilly available scripts
Build your docker images by modifying the example dockerfiles to your needs and by following [notebook-images repository's instructions](https://github.com/CSCfi/notebook-images/blob/master/builds/build.sh).

After modifying, you will need to build the images or/and upload to Rahti:
  1. for Notebook backend, use builds/build.sh -> will build locally your docker image
  2. for Rahti backend, use build_and_upload_to_openshift.bash -> will upload your dockerfile to Rahti and build the image there
