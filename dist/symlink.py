#!/usr/bin/env python

import os
import subprocess

# This scrit sets up the symlinks for the global yotta modules and targets when 
# building the kubos-sdk docker container

def main():
    module_dirs = []
    target_dirs=[]
    root_module_path = os.path.join('/', 'usr', 'lib', 'yotta_modules')
    root_target_path = os.path.join('/', 'usr', 'lib', 'yotta_targets')
    
    for subdir in os.listdir(root_module_path):
        module_dirs.append(os.path.join(root_module_path, subdir))

    for subdir in os.listdir(root_target_path):
        target_dirs.append(os.path.join(root_target_path, subdir))

    link('link', module_dirs)
    link('link-target', target_dirs)


def link(link_cmd, dir_list):
    for directory in dir_list:
        cmd('yotta', link_cmd, cwd=directory)


def cmd(*args, **kwargs):
    try:
        subprocess.check_call(args, **kwargs)
    except subprocess.CalledProcessError, e:
        print >>sys.stderr, 'Error executing command, giving up'
        sys.exit(1)


if __name__ == '__main__':
    main()
