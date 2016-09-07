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
from options import parser


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
    subparser = parser.add_subparsers(dest='subcommand_name', metavar='<subcommand>')

    def add_parser(name, module_name, description, help=None):
        if help is None:
            help = description
        def onParserAdded(parser):
            import importlib
            module = importlib.import_module('.' + module_name, 'kubos')
            module.addOptions(parser)
            parser.set_defaults(command=module.execCommand)
        subparser.add_parser_async(
            name, description=description, help=help,
            formatter_class=argparse.RawTextHelpFormatter,
            callback=onParserAdded
        )

    add_parser('build', 'build', 'Build the current project', help='Build the project in the current directory')
    add_parser('clean', 'clean', 'Remove files created by kubos builds', help='Remove files generated during the build')
    add_parser('config', 'config', 'Display the target configuration info', help='Display the target configuration info')
    add_parser('debug', 'debug', 'Debug the current module', help='Flash and launch the debugger for the current module')
    add_parser('flash', 'flash', 'Flash the target device', help='Flash and start the built executable on the current target')
    add_parser('init', 'init', 'Initialize a new KubOS project', help='Create a new module')
    add_parser('licenses', 'licenses', 'Print licenses for dependencies', help='List the licenses of the current module and its dependencies')
    add_parser('link', 'link', 'Symlink a module', help='Symlink a module to be used in the build of another module')
    add_parser('link-target', 'link_target', 'Symlink a target', help='Symlink a target into a kubos project')
    add_parser('list', 'list', 'List module dependencies', help='List the dependencies of the current module, or the inherited targets of the current target')
    add_parser('remove', 'remove', 'remove a symlinked module', help='Remove a symlinked module')
    add_parser('search', 'search', 'Search for modules and targets', help='Search for published modules and targets')
    add_parser('server', 'server', 'Kubos debug GDB server', help='Interact with the Kubos GDB server')
    add_parser('shrinkwrap', 'shrinkwrap', 'Create a yotta-shrinkwrap.json file to freeze dependency versions', help='free dependency versions')
    add_parser('target', 'target', 'Set the target device', help='Set or display the current target device')
    add_parser('test', 'test', 'Run the tests for the current module on the current target. Requires target support for cross-compiling targets', help='Run the tests for the current module or target')
    add_parser('update', 'update', 'Pull the latest kubos-sdk container', help='Pull latest kubos-sdk docker container')
    add_parser('version', 'version', 'Show the current kubos-sdk version', help='Display version information')

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

