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
import json
import os
import subprocess
import sys
import urllib2 
import xml.etree.ElementTree as ET

from yotta import build, init, target
from yotta.lib import component, globalconf

kubos_rt = 'kubos-rt'
kubos_rt_branch = '~0.0.1'
org_name = 'openkosmosorg'
kubos_rt_full_path = '%s@%s/%s#%s' % (kubos_rt, org_name, kubos_rt, kubos_rt_branch)

yotta_meta_file = '.yotta.json'
yotta_install_path = '/usr/local/bin/yotta'

target_const = '_show_current_target_'

original_check_value = argparse.ArgumentParser._check_value

def main():    
    argparse.ArgumentParser._check_value = kubos_check_value
    parser    = argparse.ArgumentParser('kubos-sdk')
    subparser = parser.add_subparsers(dest='command')
    
    init_parser   = subparser.add_parser('init')
    target_parser = subparser.add_parser('target')
    build_parser  = subparser.add_parser('build')

    init_parser.add_argument('proj_name', type=str, nargs=1)
    target_parser.add_argument('target', nargs='?', type=str)

    args, unknown_args = parser.parse_known_args()
    provided_args = vars(args)

    globalconf.set('interactive', False)

    command = provided_args['command'] 
    if command == 'init':
        proj_name = provided_args['proj_name'][0]
        _init(proj_name)
    elif command == 'target':
        provided_target = provided_args['target']
        if provided_target:
            set_target(provided_target)
        else:
            show_target()
    elif command == 'build':
        _build(unknown_args)


def _init(name):
    print 'Initializing project: %s ...' % name
    kubos_rt_repo_path = "".join([org_name, '/', kubos_rt, '#', kubos_rt_branch])
    c = component.Component(os.getcwd())
    c.description['name'] = name
    c.description['bin'] = './source'
    c.description['dependencies'] = {
        'kubos-rt' : kubos_rt_repo_path
    }
    c.description['homepage'] = 'https://<homepage>'
    init.initNonInteractive(None, c)


def _build(unknown_args):
    globalconf.set('plain', False)
    current_target = get_current_target()

    if target:
        args = argparse.Namespace(config=None,
                                  cmake_generator='Ninja',
                                  debug=None,
                                  generate_only=False,
                                  interactive=False,
                                  target=current_target,
                                  plain=False,
                                  release_build=True,
                                  registry=None)
    
    build_status = build.installAndBuild(args, unknown_args)
    
    if all(value == 0 for value in build_status.values()):
        print '\nBuild Succeeded'
    else:
        print '\nBuild Failed'


def show_target(): 
    current_target = get_current_target()
    if current_target:
        target_args = argparse.Namespace(plain=False,
                                         set_target=None,
                                         target=current_target)
        target.displayCurrentTarget(target_args)
    else:
        print 'No target currently set'


def set_target(new_target):
    print 'Setting Target: %s' % new_target.split('@')[0]
    globalconf.set('plain', False)
    target_args = argparse.Namespace(set_target=new_target,
                                     save_global=True,
                                     no_install=False)
    target.execCommand(target_args, '') 


def get_current_target():
    meta_file_path = os.path.join(os.getcwd(), yotta_meta_file)
    if os.path.isfile(meta_file_path):
        with open(meta_file_path, 'r') as meta_file:
            data = json.load(meta_file)
            target_str = str(data['build']['target'])
            return target_str.split(',')[0]
    else:
        return None
        

def cmd(*args, **kwargs):
    try:
        subprocess.check_call(args, **kwargs)
    except subprocess.CalledProcessError, e:
        print >>sys.stderr, 'Error executing command, giving up'
        sys.exit(1)

# Temporarily override the argparse error handler that deals with undefined subcommands
# to allow these subcommands to be passed to yotta. Before calling yotta
# the error handler is set back to the standard argparse handler.

def kubos_check_value(self, action, value):
    if action.choices is not None and value not in action.choices:
        argparse.ArgumentParser._check_value = original_check_value
        import yotta
        yotta.main()

if __name__ == '__main__':
    main()

