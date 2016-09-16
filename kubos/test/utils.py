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
import kubos
import mock
import os
import shutil
import sys
import tempfile
import unittest

from kubos.utils.project import module_key, target_key

#Call_list is a tuple of _Call_List instances which holds an argparse.Namespace object
#call_list[0][0] returns the argument list that the function was called with the first time

def get_arg_list(call_list):
    return call_list[0][0]


#call_list[0][0][0] returns the first Namespace object in call_list
#vars(Namespace) returns a dictionary of the arguments the function was called with

def get_arg_dict(call_list):
    return vars(call_list[0][0][0])


class KubosTestCase(unittest.TestCase):
    test_command = None
    test_arg = None
    test_name =  'test_case'
    json_template = '{ "name" : "%s" }' % test_name

    # More generic setUp and tearDown for all tests
    def setUp(self):
        arg1 = sys.argv[0]
        sys.argv = list()
        sys.argv.append(arg1)
        kubos.utils.container.pass_through = mock.MagicMock()
        kubos.utils.container.get_cli = mock.MagicMock()
        self.start_dir = os.getcwd()
        self.base_dir = tempfile.mkdtemp()
        os.chdir(self.base_dir)


    def tearDown(self):
        os.chdir(self.start_dir)
        shutil.rmtree(self.base_dir)
        try:
            sys.argv.remove(self.test_command)
        except ValueError:
            pass
        if self.test_arg in sys.argv: # Not all tests requrire an additional argument
            sys.argv.remove(self.test_arg)


# These are helper functions for unit testing the link and link-target commands
# They have their own tests in test_utils.py

def remove_link(file_path, link_type_key, module_or_target):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as json_file:
            link_data = json.load(json_file)
        if module_or_target in link_data[link_type_key]:
            link_data[link_type_key].pop(module_or_target)
            with open(file_path, 'w') as json_file:
                json_file.write(json.dumps(link_data))
            print 'Removed %s from %s' % (module_or_target, file_path)
        else:
            print '%s is not a valid link in %s.. There\'s nothing to remove' % (module_or_target, file_path)
    else:
        print '%s is not a valid file' % file_path


def set_link(file_path, link_type_key, link_name):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as json_file:
            link_data = json.load(json_file)
        link_data[link_type_key][link_name] = 'test_value'
    else:
        link_data = {target_key: {},
                     module_key: {}}
        link_data[link_type_key][link_name] = 'test_value'
    with open(file_path, 'w') as json_file:
        json_file.write(json.dumps(link_data))


def check_link(file_path, link_type_key, link_name):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as json_file:
            link_data = json.load(json_file)
        if link_name in link_data[link_type_key]:
            return True
        else:
            return False
    else:
        print '%s is not a valid file' % file_path

