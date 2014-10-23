#!/usr/bin/env python

import sys
import os
import shutil
import sys
import argparse
import vk_common

VK_COMMITS_DIR = '.vk-commits/'
GIT_POST_COMMIT = ".git/hooks/post-commit"
GIT_GITIGNORE = ".gitignore"

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print dir_name, "directory have been created."
        return True
    else:
        print "'" + dir_name + "'", "directory have been found."
        return False


def check_dir(dir_name):
    if not os.path.exists(dir_name) or not os.path.isdir(dir_name):
        return False
    else:
        return True

def copy_with_mode(src, dst):
    shutil.copyfile(src, dst)
    shutil.copymode(src, dst)


def print_help():
    print "Type 'vk-commits init', to init vk-commits in cwd"
    print "Type 'vk-commits setup', to setup vk-commits in cwd"


def init_vk_commits():
    print "vk-commits initialization started..."

    home = os.path.expanduser("~") + "/"
    MAIN_DIR = home + VK_COMMITS_DIR
    DIST_DIR = MAIN_DIR + 'dist/'

    create_dir(VK_COMMITS_DIR)

    if not check_dir(DIST_DIR):
        print "dist dir ('" + DIST_DIR + "') not found"
        exit()
    else:
        print "dist dir found, starting installation..."
        files = [
            "post-commit.py",
            "vk_auth.py",
            "vk_common.py"
        ]
        for filename in files:
            copy_with_mode(
                DIST_DIR + filename,
                VK_COMMITS_DIR + filename
            )
        if os.path.exists(GIT_POST_COMMIT):
            answer = query_yes_no(
                "file '.git/hooks/post-commit' already exists, overwrite?"
            )
            if answer is True:
                os.remove(GIT_POST_COMMIT)
            else:
                print "not overwriting post-commit, so terminating installation"
                exit()

        os.symlink(
            "../../" + VK_COMMITS_DIR + "post-commit.py",
            ".git/hooks/post-commit"
        )
        configs = vk_common.no_configs(VK_COMMITS_DIR + 'configs.json')

    GITIGNORE_TEXT = ".vk-commits\n.lastcommit"

    if os.path.exists(GIT_GITIGNORE):
        f = open(GIT_GITIGNORE, 'a')
    else:
        f = open(GIT_GITIGNORE, 'w')
    f.write(GITIGNORE_TEXT)


def setup_vk_commits():
    if not check_dir(VK_COMMITS_DIR):
        print "no .vk-commits dir found, run 'vk-commits init'"
    vk_common.no_configs(VK_COMMITS_DIR + 'configs.json')


if __name__ == "__main__":
    args = [
        "init",
        "login",
        "setup"
    ]

    if len(sys.argv) != 2:
        print_help()
        exit()
    if sys.argv[1] not in args:
        print "wrong args!"
        print_help()
        exit()
    if not os.path.exists('.git') or not os.path.isdir('.git'):
        print "Not a git repository"
        exit()

    if sys.argv[1] == "init":
        init_vk_commits()
    if sys.argv[1] == "setup":
        setup_vk_commits()
