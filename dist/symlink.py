#!/usr/bin/env python

# Kubos SDK
# Copyright (C) 2016 Kubos Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# This is the kubos-sdk "target" script that is executed inside the kubostech/kubos-sdk 
# docker container image. The project directory on the host is mounted
# into a container instance, then this script executed commands such as: build, init and target
# against the project directory.

import argparse
import os

from yotta import link, link_target

# This script sets up the symlinks for the global yotta modules and targets when 
# building the kubos-sdk docker container

def main():
    module_dirs = []
    target_dirs=[]
    root_module_path = os.path.join('/', 'usr', 'lib', 'yotta_modules')
    root_target_path = os.path.join('/', 'usr', 'lib', 'yotta_targets')
    
    for subdir in os.listdir(root_module_path):
        module_dir = os.path.join(root_module_path, subdir)
        # to only set up half of the symlink, the cwd must be the module directory
        # the second half of the symlink is currently created before building the project
        os.chdir(module_dir)   
        print 'Linking: %s' % module_dir
        _link()

    for subdir in os.listdir(root_target_path):
        target_dir = os.path.join(root_target_path, subdir)
        os.chdir(target_dir)   
        print 'Linking Target: %s' % target_dir
        _link_target()


def _link():
    link_args = argparse.Namespace(module_or_path=None,
                                   config=None,
                                   target=None)
    link.execCommand(link_args, None)

def _link_target():
    link_target_args = argparse.Namespace(target_or_path=None,
                                   config=None,
                                   target=None)
    link_target.execCommand(link_target_args, None)


if __name__ == '__main__':
    main()
