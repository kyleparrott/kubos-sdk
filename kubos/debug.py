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

import logging
import os
import subprocess
import sys
import thread

from . import server
from options import parser
from pkg_resources import resource_filename
from utils import container, target, project

gdb_command_file = '.gdb_commands'

gdb_commands = '''\
target remote %s:3333
file %s
load
'''

def addOptions(parser):
    '''
    This is a required function that's called from main when this module is imported
    '''
    pass


def execCommand(args, following_args):
    current_target = target.get_current_target()
    if not current_target:
        print >>sys.stderr, 'Set a target and build your project before debugging'
        sys.exit(1)
    generate_gdb_commands(current_target)
    if server.get_server_status() == server.server_stopped:
        print 'Kubos GDB server not running...\nStarting GDB Server...'
        server.start_server()
    gdb_file_path = os.path.join(os.getcwd(), gdb_command_file)
    if current_target.startswith('stm32') or current_target.startswith('na'):
        command = ['arm-none-eabi-gdb', '-x', gdb_file_path]
    elif current_target.startswith('msp430'):
        command = ['msp430-gdb', '-x', gdb_file_path]
    container.debug(command)


def generate_gdb_commands(current_target):
    proj_name = project.get_project_name()
    exe_path  = os.path.join(os.getcwd(), 'build', current_target, 'source', proj_name)
    commands  = gdb_commands % (get_host_ip(), exe_path)
    if not os.path.isfile(exe_path):
        print >>sys.stderr, 'Error, the binary %s does not exist. Run `kubos build` to build your project before debugging'
        sys.exit(1)
    with open(gdb_command_file, 'w') as gdb_file:
        gdb_file.write(commands)


def get_host_ip():
    if sys.platform.startswith('linux'):
        return 'localhost'
    if sys.platform.startswith('darwin'):
        kubos_dir = get_kubos_dir()
        machine_name = os.getenv('DOCKER_MACHINE_NAME')
        script_path = os.path.join(kubos_dir, 'utils', 'getip.sh')
        try:
            ip = subprocess.check_output(['/bin/bash', script_path])
            return ip.strip()
        except subprocess.CalledProcessError as e:
            print >>sys.stderr, 'There was an error getting your docker-machine configuration. You might need to re-run the `docker-machine env` command'
            sys.exit(1)


def get_kubos_dir():
    kubos_dir = resource_filename(__name__, '')
    return kubos_dir

