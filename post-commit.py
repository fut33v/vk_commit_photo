#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import urllib2
from urllib import urlencode
import os
import requests
from datetime import datetime
from os.path import expanduser

from vk_common import load_configs
from vk_common import which


API_VERSION = 5.25


def call_api(method, params, token):
    params.append(("access_token", token))
    params.append(("v", API_VERSION))
    url = "https://api.vk.com/method/%s?%s" % (method, urlencode(params))
    response = urllib2.urlopen(url).read()
    if 'response' in response:
        return json.loads(response)['response']
    else:
        print response


def get_albums(user_id, token):
    return call_api("photos.getAlbums", [("uid", user_id)], token)


def create_album(album_title, album_description, token):
    response = call_api(
        "photos.createAlbum",
        [
            ('title', album_title),
            ('description', album_description)
        ],
        token
    )
    return response


def get_album_id_or_create(album_title, album_desc, albums, token):
    album_exists = False
    for album in albums['items']:
        if album['title'] == album_title:
            album_exists = True
            album_id = album['id']
    if not album_exists:
        album_id = create_album(album_title, album_desc, token)['id']
    return album_id


def upload_photo(album_id, filename, description, token):
    upload = call_api(
        'photos.getUploadServer',
        [
            ('album_id', album_id)
        ],
        token
    )
    upload_url = upload['upload_url']
    files = {'file1': (filename, open(filename, 'rb'))}
    res = requests.post(upload_url, files=files)
    res = json.loads(res.text)
    photos_list = res['photos_list']
    server = res['server']
    hash_ = res['hash']
    upload = call_api(
        'photos.save',
        [
            ('album_id', album_id),
            ('photos_list', photos_list),
            ('server', server),
            ('hash', hash_),
            ('caption', description)
        ],
        token
    )


if __name__ == "__main__":

    CONFIGS_DIR = '.vk-commits/'
    VK_COMMITS_DIR = '.vk-commits/'
    CONFIGS_FILE = CONFIGS_DIR + 'configs.json'

    configs = load_configs(CONFIGS_FILE)

    if not configs:
        print "no configs file found, type 'vk-commits setup' to fix it"
        exit()

    # if 'token' not in configs or 'user_id' not in configs:
    #     print "no token found, type 'vk-commits setup' to fix it"
    #     exit()

    token = configs['token']
    user_id = configs['user_id']
    album_title = configs['album_title']
    album_desc = configs['album_desc']

    home = expanduser("~") + "/"
    PHOTOS_DIR = home + VK_COMMITS_DIR + "photos/"

    if not os.path.exists(PHOTOS_DIR):
        os.makedirs(PHOTOS_DIR)

    now = datetime.now()
    now = now.strftime('%Y%m%d%H%M%S')
    filename = PHOTOS_DIR + now + ".jpg"

    if which('fswebcam') is None:
        print (
            "seems like fswebcam is not installed," +
            "on debian/ubuntu you can run sudo apt-get install fswebcam" +
            "for fixing the problem"
        )
    else:
        os.system('fswebcam -r 640x480 ' + filename)

    albums = get_albums(user_id, token)

    album_id = get_album_id_or_create(album_title, album_desc, albums, token)

    os.system('git log -1 HEAD > .lastcommit')
    commit = open('.lastcommit', 'r').read()

    upload_photo(album_id, filename, commit, token)
