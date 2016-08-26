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
from utils.project import get_global_link_file, get_local_link_file, module_key, target_key

def addOptions(parser):
    parser.add_argument('module_or_path', nargs='?', help='symlink a module to be used in another module')


def execCommand(args, following_args):
    module_or_path = args.module_or_path
    if module_or_path:
        if os.sep in module_or_path:
            #since the argument is a path do a 2 step link (first global then to the local module)
            module_or_path = os.path.abspath(module_or_path)
            module_name = link_global(module_or_path)
            link_global_to_local(module_name)
        else:
            #since the argument is a target name, link it from the global file to the local project
            link_global_to_local(module_or_path)
    else:
        #no argument was given, so link the target in the current directory to the global file
        link_global(os.getcwd())


def link_global(target_path):
    target_path = os.path.abspath(target_path)
    target_json = os.path.join(target_path, 'target.json')
    if os.path.isfile(target_json):
        with open(target_json, 'r') as targ_json:
            try:
                target_data = json.load(targ_json)
                target_name = target_data['name']
            except ValueError:
                print >>sys.stderr, 'Error parsing data from: %s \nAre you sure it contains Vailid JSON data?' % target_json
                sys.exit(1)
    else:
        print >>sys.stderr, 'Error, unable to link %s does not contain a target.json' % target_path
        sys.exit(1)

    global_link_file = get_global_link_file()
    if os.path.isfile(global_link_file):
        with open(global_link_file, 'r') as meta_file:
            link_data = json.load(meta_file)
            link_data[target_key][target_name] = target_path
    else:
        link_data = {
                        target_key : {target_name : target_path},
                        module_key : {}
                    }

    #write the updated changes back to the global file
    with open(global_link_file, 'w') as meta_file:
        str_link_data = json.dumps(link_data)
        meta_file.write(str_link_data)
        print 'Successfully Linked %s: %s' % (target_name, target_path)
    return target_name


def link_global_to_local(target_name):
    local_link_file = get_local_link_file()
    global_link_file = get_global_link_file()

    if os.path.isfile(global_link_file):
        with open(global_link_file, 'r') as global_file:
            global_links = json.load(global_file)
        if target_name in global_links[target_key]:
            if os.path.isfile(local_link_file):
                with open(local_link_file, 'r') as link_file:
                    link_data = json.load(link_file)
            else:
                link_data = {
                                target_key: {},
                                module_key: {}
                            }
            target_path = global_links[target_key][target_name]
            link_data[target_key][target_name] = target_path

            with open(local_link_file, 'w') as link_file:
                links = json.dumps(link_data)
                link_file.write(links)
        else:
            print >>sys.stderr, 'Error module %s not linked globally' % target_name
            sys.exit(1)
    else:
        print >>sys.stderr, 'No modules are currently linked globally'
        sys.exit(1)

    print 'Successfully Linked %s: %s Locally' % (target_name, target_path)

