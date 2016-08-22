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
import sys
import unittest

from kubos import main, version, utils
from kubos.test.utils import get_arg_dict, KubosTestCase

class KubosVersionTest(KubosTestCase):
    def setUp(self):
        super(KubosVersionTest, self).setUp()
        self.test_command = 'version'
        sys.argv.append(self.test_command)
        version.execCommand = mock.MagicMock()


    def test_version(self):
        search_dict = {'subcommand_name' : self.test_command}
        main()
        arg_list  = get_arg_dict(version.execCommand.call_args_list)
        self.assertTrue(search_dict.viewitems() <= arg_list.viewitems())


    def tearDown(self):
        super(KubosVersionTest, self).tearDown()


class KubosVTest(KubosTestCase):
    def setUp(self):
        super(KubosVTest, self).setUp()
        self.test_command = 'v'
        sys.argv.append(self.test_command)
        version.execCommand = mock.MagicMock()


    def test_v(self):
        search_dict = {'subcommand_name' : self.test_command}
        main()
        arg_list  = get_arg_dict(version.execCommand.call_args_list)
        self.assertTrue(search_dict.viewitems() <= arg_list.viewitems())


    def tearDown(self):
        super(KubosVTest, self).tearDown()


if __name__ == '__main__':
    unittest.main()
