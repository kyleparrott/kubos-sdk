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

import argparse
import functools
import json
import logging
import os
import sys
import subprocess
import time
import threading

from docker import Client
import docker

from utils import container
from options import command, parser
import sdk_config

#Analytics are only supported on Mac OS right now
if sys.platform.startswith('darwin'):
    try:
        from kubos import analytics
    except:
        print 'No analytics module found, disabling analytics'
        analytics = None

def splitList(l, at_value):
    r = [[]]
    for x in l:
        if x == at_value:
            r.append(list())
        else:
            r[-1].append(x)
    return r

def main():
    if os.name == 'nt':
        logging.warning('Windows is not currently supported. Many of the features in the Kubos-sdk will most likely not work correctly or at all on computers running Windows')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='kubos - the SDK for working with the KubOS RTOS\n'+
        'For more detailed help on each subcommand, run: kubos <subcommand> --help'
    )

    config = sdk_config.load_config()
    subparser = parser.add_subparsers(dest='subcommand_name', metavar='<subcommand>')

    add_command = functools.partial(command.add_command, config, subparser)
    add_command('build', 'build', 'Build the current project', help='Build the project in the current directory')
    add_command('clean', 'clean', 'Remove files created by kubos builds', help='Remove files generated during the build')
    add_command('config', 'config', 'Display the target configuration info', help='Display the target configuration info')
    add_command('debug', 'debug', 'Debug the current module', help='Flash and launch the debugger for the current module')
    add_command('flash', 'flash', 'Flash the target device', help='Flash and start the built executable on the current target')
    add_command('init', 'init', 'Initialize a new KubOS project', help='Create a new module')
    add_command('licenses', 'licenses', 'Print licenses for dependencies', help='List the licenses of the current module and its dependencies')
    add_command('link', 'link', 'Symlink a module', help='Flash and start the built executable on the current target')
    add_command('link-target', 'link_target', 'Symlink a target', help='Symlink a target into a kubos project')
    add_command('list', 'list', 'List module dependencies', help='List the dependencies of the current module, or the inherited targets of the current target')
    add_command('remove', 'remove', 'remove a symlinked module', help='Remove a symlinked module')
    add_command('search', 'search', 'Search for modules and targets', help='Search for published modules and targets')
    add_command('server', 'server', 'Kubos debug GDB server', help='Interact with the Kubos GDB server')
    add_command('shrinkwrap', 'shrinkwrap', 'Create a yotta-shrinkwrap.json file to freeze dependency versions', help='free dependency versions')
    add_command('target', 'target', 'Set the target device', help='Set or display the current target device')
    add_command('test', 'test', 'Run the tests for the current module on the current target. Requires target support for cross-compiling targets', help='Run the tests for the current module or target')
    add_command('update', 'update', 'Pull the latest kubos-sdk container', help='Pull latest kubos-sdk docker container')
    add_command('version', 'version', 'Show the current kubos-sdk version', help='Display version information')

    short_commands = {
                'up':subparser.choices['update'],
                'ln':subparser.choices['link'],
                 'v':subparser.choices['version'],
                'ls':subparser.choices['list'],
                'rm':subparser.choices['remove'],
            'unlink':subparser.choices['remove'],
     'unlink-target':subparser.choices['remove'],
              'lics':subparser.choices['licenses'],
    }
    subparser.choices.update(short_commands)

    split_args = splitList(sys.argv, '--')
    following_args = reduce(lambda x,y: x + ['--'] + y, split_args[1:], [])[1:]

    args = parser.parse_args(split_args[0][1:])

    if 'command' not in args:
        parser.print_usage()
        sys.exit(0)

    try:
        status = args.command(args, following_args)
    except KeyboardInterrupt:
        logging.warning('interrupted')
        status = -1

        sys.exit(status or 0)

