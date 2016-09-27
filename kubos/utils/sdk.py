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
import sys
from pkg_resources import resource_filename

'''
This supports using a default kubos source tree location ~/.kubos or you can specify
a non-default location by adding the mount_point key in the module.json file.

example module.json file:
{
  "name": "kubos-sdk",
  "version": "0.1.3",
  "edition": "preview",
  "description": "Kubos SDK",
  "author": "Kubos",
  "author_email": "kyle@kubos.co",
  "url": "http://github.com/kubostech/kubos-sdk",
  "mount_point": "/Users/username/..."
}

The mount point should be in the /Users/ directory if on mac or else docker will not be able
to mount the source into the container without additional manual configuration.

The mount point should also be an absolute path to avoid any weird behavior in creating 
the path if it does not exist.
'''
def get_sdk_attribute(attr):
    sdk_data = json.load(open(SDK_MODULE_JSON, 'r'))
    if attr in sdk_data:
        return sdk_data[attr]
    else:
        return None


KUBOS_RESOURCE_DIR = os.path.join(resource_filename('kubos', ''), '..')

prod_path = os.path.abspath(resource_filename('kubos', 'module.json'))
dev_path = os.path.join(os.path.abspath(__file__), '..', '..', '..', 'module.json')
SDK_MODULE_JSON = prod_path if os.path.isfile(prod_path) else dev_path

home_dir = os.path.expanduser('~')
KUBOS_DIR = os.path.join(home_dir, '.kubos')
mnt = get_sdk_attribute('mount_point')
if mnt:
    _KUBOS_DIR = os.path.join(mnt, '.kubos')
    if not os.path.isdir(_KUBOS_DIR):
        try:
            os.makedirs(_KUBOS_DIR)
        except:
            print 'there was a problem creating the custom mount point %s' % _KUBOS_DIR
            print 'Using default location %s' % KUBOS_DIR
            _KUBOS_DIR = KUBOS_DIR
    KUBOS_DIR = _KUBOS_DIR
    print 'Using custom source mount point %s'% KUBOS_DIR


prod_path = os.path.abspath(resource_filename('kubos.container', 'kubos-sdk.py'))
dev_path = os.path.join(os.path.abspath(__file__), '..', '..', 'container', 'kubos-sdk.py')
# Global scripts are installed inside the python module at /usr/local/lib...
GLOBAL_CONTAINER_SCRIPT = prod_path if os.path.isfile(prod_path) else dev_path
GLOBAL_CONTAINER_DIR = os.path.dirname(GLOBAL_CONTAINER_SCRIPT)
# Container script exists at ~/.kubos/container/ becuase non-user directories ie /usr/... are not
# by default mounted into docker containers on mac os.
CONTAINER_DIR= os.path.join(KUBOS_DIR, 'container')
CONTAINER_SCRIPT = os.path.join(CONTAINER_DIR, 'kubos-sdk.py')

KUBOS_MODULES = os.path.join(KUBOS_DIR, 'yotta_modules')
KUBOS_TARGETS = os.path.join(KUBOS_DIR, 'yotta_targets')
KUBOS_EXAMPLES = os.path.join(KUBOS_DIR, 'examples')


