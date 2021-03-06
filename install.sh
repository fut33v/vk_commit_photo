#!/bin/bash

if [ ! -d ~/.vk-commits ]; then
    mkdir -p ~/.vk-commits/dist
    echo ~/.vk-commits directory created
fi

cp -r *.py ~/.vk-commits/dist

if [ -a /usr/bin/vk-commits ]; then
    echo link exists, replacing
    rm /usr/bin/vk-commits
fi

ln -sv ~/.vk-commits/dist/vk-commits.py /usr/bin/vk-commits
