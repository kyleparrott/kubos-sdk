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
import os
import unittest
import sys

from kubos.test.utils import get_arg_dict

class KubosLinkTest(unittest.TestCase):
    def setUp(self):
        arg1 = sys.argv[0]
        sys.argv = list()
        sys.argv.append(arg1)
        sys.argv.append('link')
        kubos.utils.container.pass_through = mock.MagicMock()
        #These test intentionally cause warnings output to stderr
        #These warnings aren't relevant to the test so this hides the warnings
        sys.stderr = open(os.devnull, 'wb')


    def test_link(self):
        search_dict = {'subcommand_name' : 'link'}
        with self.assertRaises(SystemExit):
            kubos.main()
            arg_list  = get_arg_dict(kubos.utils.link.execCommand.call_args_list)
            self.assertTrue(search_dict.viewitems() <= arg_list.viewitems())


    def tearDown(self):
        sys.argv.remove('link')


if __name__ == '__main__':
    unittest.main()

