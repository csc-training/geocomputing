# Custom CSC's Notebook's docker images for Notebooks and Rahti
By custom docker images, we mean customized versions of the existing docker images in CSC's [notebook-images repository](https://github.com/CSCfi/notebook-images).

The safest way to get a working custom Rahti/Notebook image is to  start from the available templates in CSC's base images (see `builds` directory).

If you need to customize also your favorite docker images, you can learn from these instructions and apply to your dockerfile. In that case, note that the Notebooks-images dockerfiles contain different commands that make the output images compatible with Rahti and/or Notebooks backends. Make sure that you include those commands in your dockerfile in the correct positions.

## Building your custom docker images using the readilly available scripts
Build your docker images by modifying the template dockerfiles in [notebook-images repository's](https://github.com/CSCfi/notebook-images/tree/master/builds) to your needs.

After you have gotten your dockerfile ready, you will need to build the images or/and upload to Rahti:
  1. for Notebook backend, use builds/build.sh -> will build locally your docker image
  2. for Rahti backend, use build_and_upload_to_openshift.bash -> will upload your dockerfile to Rahti and build the image there

 See more instructions at [notebook-images repository](https://github.com/CSCfi/notebook-images/tree/master/builds).
