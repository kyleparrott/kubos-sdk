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
import os
import sys
import unittest

from kubos.test.utils import get_arg_dict, set_link, check_link, remove_link, KubosTestCase
from kubos.utils.project import get_local_link_file, get_global_link_file, module_key, target_key


class KubosRemoveTest(KubosTestCase):
    def setUp(self):
        super(KubosRemoveTest, self).setUp()
        self.test_command = 'remove'
        sys.argv.append(self.test_command)
        #These tests intentionally cause warnings output to stderr
        #These warnings aren't relevant to the test so this hides the warnings
        sys.stderr = open(os.devnull, 'wb')
        self.target_json = os.path.join(self.base_dir, 'target.json')


    def test_remove_nonexistent_link(self):
        with self.assertRaises(SystemExit):
            kubos.main()


    def test_remove_linked_target(self):
        local_link_file = get_local_link_file()
        set_link(local_link_file, target_key, self.test_name)
        self.assertTrue(check_link(local_link_file, target_key, self.test_name))
        sys.argv.append(self.test_name)
        kubos.main()
        self.assertFalse(check_link(local_link_file, target_key, self.test_name))


    def test_remove_linked_module(self):
        local_link_file = get_local_link_file()
        set_link(local_link_file, module_key, self.test_name)
        self.assertTrue(check_link(local_link_file, module_key, self.test_name))
        sys.argv.append(self.test_name)
        kubos.main()
        self.assertFalse(check_link(local_link_file, module_key, self.test_name))


    def tearDown(self):
        super(KubosRemoveTest, self).tearDown()
        if os.path.isfile(self.target_json):
            os.remove(self.target_json)


if __name__ == '__main__':
    unittest.main()
