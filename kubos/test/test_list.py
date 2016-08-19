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

from kubos.utils import target, container
from kubos.test.utils import get_arg_list, KubosTestCase


class KubosListTest(KubosTestCase):
    def setUp(self):
        super(KubosListTest, self).setUp()
        self.test_command = 'list'
        sys.argv.append(self.test_command)

    def test_list_without_target(self):
        target.get_current_target = mock.MagicMock(return_value=None)
        with self.assertRaises(SystemExit):
            kubos.main()


    def test_list_with_target(self):
        target.get_current_target = mock.MagicMock(return_value='stm32f407-disco-gcc')
        kubos.main()
        arg_list = get_arg_list(kubos.utils.container.pass_through.call_args_list)
        self.assertTrue(self.test_command in arg_list)


    def tearDown(self):
        super(KubosListTest, self).tearDown()


if __name__ == '__main__':
    unittest.main()

