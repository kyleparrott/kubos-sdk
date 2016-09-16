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

import os
import sys
import subprocess

from pkg_resources import resource_filename
from options import parser
from utils import target, project


def addOptions(parser):
    pass


def execCommand(args, following_args):
    current_target = target.get_current_target()
    if current_target:
        project_name = project.get_project_name()

        if not project_name:
            print >>sys.stderr, 'Error: No module.json file found. Run "kubos init" to create a new project'
            sys.exit(1)
        proj_exe_path =  os.path.join(os.getcwd(), 'build', current_target, 'source', project_name)
        kubos_dir = resource_filename(__name__, '')

        if current_target.startswith('stm32f407') or current_target.startswith('na'):
            flash_openocd(proj_exe_path, kubos_dir)
        elif current_target.startswith('pyboard'):
            flash_dfu_util(proj_exe_path, kubos_dir)
        elif current_target.startswith('msp430'):
            flash_mspdebug(proj_exe_path, kubos_dir)

    else:
        print >>sys.stderr, 'Error: No target currently selected. Select a target and build before flashing'


def flash_openocd(proj_exe_path, kubos_dir):
    if sys.platform.startswith('linux'):
        openocd_exe = os.path.join(kubos_dir, 'bin', 'linux', 'openocd')
        lib_path = os.path.join(kubos_dir, 'lib', 'linux')
    elif sys.platform.startswith('darwin'):
        openocd_exe = os.path.join(kubos_dir, 'bin', 'osx', 'openocd')
        lib_path = os.path.join(kubos_dir, 'lib', 'osx')

    project.add_kubos_lib_path(lib_path)
    openocd_dir = os.path.join(kubos_dir, 'flash', 'openocd')
    flash_script_path = os.path.join(openocd_dir, 'flash.sh')
    argument = 'stm32f4_flash %s' % proj_exe_path
    try:
        subprocess.check_call(['/bin/bash', flash_script_path, openocd_exe, argument, openocd_dir])
    except subprocess.CalledProcessError:
        pass


def flash_dfu_util(proj_exe_path, kubos_dir):
    if sys.platform.startswith('linux'):
        dfu_util_exe = os.path.join(kubos_dir, 'bin', 'linux', 'dfu-util')
        lib_path = os.path.join(kubos_dir, 'lib', 'linux')
    elif sys.platform.startswith('darwin'):
        dfu_util_exe = os.path.join(kubos_dir, 'bin', 'osx', 'dfu-util')
        lib_path = os.path.join(kubos_dir, 'lib', 'osx')

    project.add_kubos_lib_path(lib_path)
    dfu_util_dir = os.path.join(kubos_dir, 'flash', 'dfu_util')
    flash_script_path = os.path.join(dfu_util_dir, 'flash.sh')
    try:
        subprocess.check_call(['/bin/bash', flash_script_path, dfu_util_exe, proj_exe_path])
    except subprocess.CalledProcessError:
        pass


def flash_mspdebug(proj_exe_path, kubos_dir):
    if sys.platform.startswith('linux'):
        mspdebug_exe = os.path.join(kubos_dir, 'bin', 'linux', 'mspdebug')
        lib_path = os.path.join(kubos_dir, 'lib', 'linux')

    elif sys.platform.startswith('darwin'):
        mspdebug_exe = os.path.join(kubos_dir, 'bin', 'osx', 'mspdebug')
        lib_path = os.path.join(kubos_dir, 'lib', 'osx')

    project.add_kubos_lib_path(lib_path)
    flash_script_path = os.path.join(kubos_dir, 'flash', 'mspdebug', 'flash.sh')
    argument = 'prog %s' % proj_exe_path
    try:
        subprocess.check_call(['/bin/bash', flash_script_path, mspdebug_exe, argument])
    except subprocess.CalledProcessError:
        pass

