## Setting up your Taito's home directory

For this exercise you need to have an account in CSC's Taito supercluster. You may also have a temporary student account of the type *student0xx*.

You can mount a Taito folder to your VM using a SSH file system mount. Follow these steps:

- Connect to your VM using **Putty** / **ssh** as you did before (or continue using the terminal via the Pouta web interface).
- See instructions here: [https://research.csc.fi/csc-guide-remote-disk-mounts](https://research.csc.fi/csc-guide-remote-disk-mounts)

```bash
# Make a local directory in your VM where you will mount your Taito folder
mkdir ~/taito-home

# Install sshfs and mount your Taito folder (use your training credentials ( **student0xx** ):
sudo apt install sshfs
sshfs student0xx@taito.csc.fi:/homeappl/home/student0xx  ~/taito-home

# To unmount a folder run
#fusermount -u ~/taito-home
```
