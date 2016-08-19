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
import logging
import os
import sys

from options import parser
from utils import container
from utils.project import get_local_link_file, module_key, target_key

def addOptions(parser):
    parser.add_argument('module_name', nargs=1, help='remove a previously linked module from the local build')


def execCommand(args, following_args):
    module_or_target = args.module_name[0]
    local_link_file = get_local_link_file()
    if os.path.isfile(local_link_file):
        with open(local_link_file, 'r') as link_file:
            link_data = json.load(link_file)
            module_data = link_data[module_key]
            target_data = link_data[target_key]
        if module_or_target in module_data:
            remove_link(module_or_target, module_key, link_data)
            print "Successfully removed linked module %s" % module_or_target
        elif module_or_target in target_data:
            remove_link(module_or_target, target_key, link_data)
            print "Successfully removed linked target %s" % module_or_target
        else:
            print >>sys.stderr, 'Module or target %s is not currently linked' % module_or_target
            sys.exit(1)
    else:
        print >>sys.stderr, 'No modules or targets are currently linked. Nothing to unlink.'
        sys.exit(1)

def remove_link(module_or_target, json_key, json_data):
    json_data[json_key].pop(module_or_target)
    local_link_file = get_local_link_file()
    with open(local_link_file, 'w') as link_file:
        link_file.write(json.dumps(json_data))

