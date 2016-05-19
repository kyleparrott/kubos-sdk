#!/usr/bin/env python

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
kubos_rt_branch = 'master'
org_name = 'openkosmosorg'
kubos_rt_full_path = '%s@%s/%s#%s' % (kubos_rt, org_name, kubos_rt, kubos_rt_branch)

yotta_meta_file = '.yotta.json'
yotta_install_path = '/usr/local/bin/yotta'

target_const = '_show_current_target_'

def main():    
    parser    = argparse.ArgumentParser('Kubos SDK')
    subparser = parser.add_subparsers(dest='command')
    
    init_parser   = subparser.add_parser('init')
    target_parser = subparser.add_parser('target')
    build_parser  = subparser.add_parser('build')

    init_parser.add_argument('proj_name', type=str, nargs=1)
    target_parser.add_argument('target', nargs='?', type=str)
    build_parser.add_argument('--verbose', action='store_true', default=False)

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
        _build(provided_args['verbose'])


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

def _build(verbose):
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
  
    if verbose:
        build_status = build.installAndBuild(args, ['-v'])
    else: 
        build_status = build.installAndBuild(args, None)
    
    if all(value == 0 for value in build_status.values()):
        print '\nBuild Succeeded'
    else:
        print '\nBuild Failed'


def show_target(): 
    current_target = get_current_target()
    if current_target:
        target_args = argparse.Namespace(plain = False,
                                         set_target = None,
                                         target = current_target)
        target.displayCurrentTarget(target_args)
    else:
        print 'No target currently set'


def set_target(new_target):
    print 'Setting Target: %s' % new_target.split('@')[0]
    globalconf.set('plain', False)
    target_args = argparse.Namespace(set_target=new_target, save_global = False, no_install = False)
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

if __name__ == '__main__':
    main()
