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

import json
import os

module_file_name = 'module.json'
k_lib_path = 'KUBOS_LIB_PATH'

#keys for link json data
module_key = 'modules'
target_key = 'targets'
target_mount_dir = os.path.join('/', 'usr', 'lib', 'yotta_targets')

def get_project_name():
    module_file_path = os.path.join(os.getcwd(), module_file_name)
    if os.path.isfile(module_file_path):
         with open(module_file_path, 'r') as module_file:
            data = json.load(module_file)
            name = data['name']
            return name
    else:
        return None


def get_global_link_file():
    home_dir = os.path.expanduser('~')
    kubos_file_path = os.path.join(home_dir, '.kubos-link-global.json')
    return kubos_file_path


def get_local_link_file():
    this_dir = os.getcwd()
    path = os.path.join(this_dir, '.kubos-link.json')
    return path


def add_env_var(var_name, value):
    if not hasattr(os.environ, var_name):
        os.environ[var_name] = value
    else:
        os.environ[var_name] += ':%s' % value

def add_kubos_lib_path(value):
    add_env_var(k_lib_path, value)

