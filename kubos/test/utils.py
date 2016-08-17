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

import kubos
import mock
import unittest
import sys

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

    # More generic setUp and tearDown for all tests
    def setUp(self):
        arg1 = sys.argv[0]
        sys.argv = list()
        sys.argv.append(arg1)
        kubos.utils.container.pass_through = mock.MagicMock()
        self._setUp()


    def tearDown(self):
        sys.argv.remove(self.test_command)
        if self.test_arg in sys.argv: # Not all tests requrire an additional argument
            sys.argv.remove(self.test_arg)
        self._tearDown()

    # These are defined in child classes to implement the spefic setUp and tearDown
    # functions for the specific tests
    def _setUp(self):
        pass

    def _tearDown(self):
        pass

