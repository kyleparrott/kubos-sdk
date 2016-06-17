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
from utils.project import get_local_link_file

def addOptions(parser):
    parser.add_argument('module_name', nargs=1, help='remove a previously linked module from the local build')


def execCommand(args, following_args):
    module_name = args.module_name[0]
    local_link_file = get_local_link_file()
    if os.path.isfile(local_link_file):
        with open(local_link_file, 'r') as link_file:
            link_data = json.load(link_file)
        if module_name in link_data:
            link_data.pop(module_name)
            with open(local_link_file, 'w') as link_file:
                links = json.dumps(link_data)
                link_file.write(links)
                print 'Successfully unlinked %s' % module_name
        else:
            print >>sys.stderr, 'Module %s is not currently linked' % module_name
            sys.exit(1)
    else:
        print >>sys.stderr, 'No modules are currently linked. Nothing to unlink.'
        sys.exit(1)

