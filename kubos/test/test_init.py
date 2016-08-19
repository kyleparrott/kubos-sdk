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
import sys
import unittest

from kubos.test.utils import get_arg_list, KubosTestCase

class KubosInitTest(KubosTestCase):
    def setUp(self):
        super(KubosInitTest, self).setUp()
        self.test_command = 'init'
        self.test_arg = 'test-project'
        sys.argv.append(self.test_command)
        sys.argv.append(self.test_arg)


    def test_init(self):
        search_args = {'proj_name' : [self.test_arg],
                       'subcommand_name' : self.test_command}
        kubos.utils.container.pass_through = mock.MagicMock()
        kubos.main()
        arg_list  = get_arg_list(kubos.utils.container.pass_through.call_args_list)
        self.assertTrue(self.test_command in arg_list)
        self.assertTrue(self.test_arg in arg_list)


    def tearDown(self):
        super(KubosInitTest, self).tearDown()


if __name__ == '__main__':
    unittest.main()
