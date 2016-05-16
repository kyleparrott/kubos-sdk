#!/usr/bin/env python

import argparse
import json
import os
import subprocess
import sys
import urllib2 
import xml.etree.ElementTree as ET

from yotta import init, target
from yotta.lib import component, globalconf

kubos_rt = 'kubos-rt'
kubos_rt_branch = 'master'
org_name = 'openkosmosorg'
kubos_rt_full_path = '%s@%s/%s#%s' % (kubos_rt, org_name, kubos_rt, kubos_rt_branch)

KubOS_manifest_url = 'https://raw.githubusercontent.com/openkosmosorg/kubos-manifest/master/default.xml'

yotta_meta_file = '.yotta.json'
yotta_install_path = '/usr/local/bin/yotta'

def main():
    parser = argparse.ArgumentParser(description = 'Kubos SDK')
    parser.add_argument('--init', nargs='?', type=str, help='Create a new module')
    parser.add_argument('--target', nargs='?', type=str, const='_show_current_target_', help='Set target device')

    args, anonymous_args = parser.parse_known_args()
    globalconf.set('interactive', False)
    
    if args.init:
        _init(args.init)
    elif args.target:
        if args.target == '_show_current_target_':
            show_target()
        else:
            set_target(args)
    elif anonymous_args:
        cmd(yotta_install_path, *anonymous_args)
    else: 
        parser.print_help()


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


def show_target():
    current_target = get_current_target()
    target_args = argparse.Namespace(plain = False,
                                     set_target = None,
                                     target = current_target)
    target.displayCurrentTarget(target_args)


def set_target(new_target):
    print 'Setting Target: %s' % new_target.split('@')[0]
    globalconf.set('plain', False)
    target_args = argparse.Namespace(set_target=new_target, save_global = False, no_install = False)
    target.execCommand(target_args, '') 


def get_current_target():    
    with open(yotta_meta_file, 'r') as meta_file:
        data = json.load(meta_file)
        target_str = str(data['build']['target'])
        return target_str.split(',')[0]


def cmd(*args, **kwargs):
    try:
        subprocess.check_call(args , **kwargs)
    except subprocess.CalledProcessError, e:
        print >>sys.stderr, 'Error executing command, giving up'
        sys.exit(1)


if __name__ == '__main__':
    main()
