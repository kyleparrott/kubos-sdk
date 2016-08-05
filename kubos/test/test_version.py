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

import mock
import unittest
import sys

from kubos import main, version, utils
from kubos.test.utils import get_arg_dict

class KubosVersionTest(unittest.TestCase):
    def setUp(self):
        self.test_command = 'version'
        arg1 = sys.argv[0]
        sys.argv = list()
        sys.argv.append(arg1)
        sys.argv.append(self.test_command)


    def test_version(self):
        search_dict = {'subcommand_name' : self.test_command}
        version.execCommand = mock.MagicMock()
        main()
        arg_list  = get_arg_dict(version.execCommand.call_args_list)
        self.assertTrue(search_dict.viewitems() <= arg_list.viewitems())


    def tearDown(self):
        sys.argv.remove(self.test_command)


class KubosVTest(unittest.TestCase):
    def setUp(self):
        self.test_command = 'v'
        arg1 = sys.argv[0]
        sys.argv = list()
        sys.argv.append(arg1)
        sys.argv.append(self.test_command)


    def test_version(self):
        search_dict = {'subcommand_name' : self.test_command}
        version.execCommand = mock.MagicMock()
        main()
        arg_list  = get_arg_dict(version.execCommand.call_args_list)
        self.assertTrue(search_dict.viewitems() <= arg_list.viewitems())


    def tearDown(self):
        sys.argv.remove(self.test_command)


if __name__ == '__main__':
    unittest.main()
