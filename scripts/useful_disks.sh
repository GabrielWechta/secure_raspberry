#!bin/bash

# list devices all, even not mounted
sudo fdisk -l

# another way to list
df -h

# cloning SD card can be done with
sudo dd if=path/to/sd/card of=path/to/output/file.img conv=fsync

## Fixing corrupted SD Card ##
# unomout SD Card when pluged to laptop
sudo umount /dev/sdc1
sudo umount /dev/sdc2

# fix corruption with log
fsck -fy /dev/sdc1
fsck -fy /dev/sdc2
## ##