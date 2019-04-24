# Manage Pouta images
You may need to upload or download images to Pouta.

Make sure that you have your *openstack* tools activated and that you have logged in to your Pouta project.

## Uploading images to Pouta
It is important to note that Pouta can use images in *qcow2* and *raw* formats so if your original image is in a different format, you should first convert it. The *qcow2* format is compressed and should be prefered.

If you have downloaded an ISO or VDI image, you can convert it to *qcow2* with the **qemu-img** tool:
```shell
# Convert ISO to qcow2
 qemu-img convert -f iso -O qcow2 <your-image>.iso <output-image>.qcow2

 # Convert vdi to qcow2
 qemu-img convert -f vdi -O qcow2 <your-image>.vdi <output-image>.qcow2
```

You can see more details about converting image from https://docs.openstack.org/image-guide/convert-images.html.

To upload that image to your Pouta project:
```shell
openstack image create "<your-pouta-image" --file <your-image>.qcow2 --disk-format qcow2 --container-format bare --private
```

## Downloading images from Pouta
In case you want to locally run your Pouta images, you could download it from Pouta, then convert it to a suitable format.

(make sure that you select the correct format for your downloaded file, see what is the format of the image Pouta):
```shell
# Get list of images in your project
openstack image list
# Get info about your image (specially the disk_format)
openstack image show <your-pouta-image>
```

Download your Pouta image with:
```shell
openstack image save --file <your-image-file>.<format> <your-pouta-image>
```

Convert an image to for example VDI format with:
```shell
qemu-img convert -f qcow2 <your-image-file>.<format> -O vdi <your-image-file>.vdi
```

## Sharing a Pouta image with other Pouta projects
In case you need to share your Pouta images with other projects, see **5.3 Sharing images between Pouta projects** from [5. Creating, Uploading & Sharing virtual machine images](https://research.csc.fi/pouta-adding-images).
