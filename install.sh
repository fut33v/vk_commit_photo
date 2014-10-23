#!/bin/bash

cd ~ 
if [ ! -d ~/.vk-commits ]; then
    mkdir ~/.vk-commits
    echo ~/.vk-commits directory created
fi
cd .vk-commits
git clone https://github.com/fat32nov/vk-commits.git dist
ln -sv ~/.vk-commits/dist/vk-commits.py /usr/bin/vk-commits
