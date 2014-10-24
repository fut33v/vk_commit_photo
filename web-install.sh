#!/bin/bash


if [ ! -d ~/.vk-commits ]; then
    mkdir ~/.vk-commits
    echo ~/.vk-commits directory created
fi

if [ -d ~/.vk-commits ]; then
    rm -rf ~/.vk-commits/dist
    echo ~/.vk-commits/dist directory removed
fi

cd ~/.vk-commits
git clone https://github.com/fat32nov/vk-commits.git dist

if [ -a /usr/bin/vk-commits ]; then
    echo link exists, replacing
    rm /usr/bin/vk-commits
fi

ln -sv ~/.vk-commits/dist/vk-commits.py /usr/bin/vk-commits
