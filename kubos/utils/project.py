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


def add_ld_library_path(path):
    ld_lib_path = 'LD_LIBRARY_PATH'
    if not hasattr(os.environ, ld_lib_path):
        os.environ[ld_lib_path] = path
    else:
        os.environ[ld_lib_path] += ':%s' % path


