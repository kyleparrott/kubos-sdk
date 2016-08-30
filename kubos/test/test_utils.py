import json
import kubos
import os
import sys
import unittest

from kubos.test.utils import get_arg_dict, KubosTestCase, remove_link, check_link, set_link
from kubos.utils.project import get_local_link_file, get_global_link_file, module_key, target_key

class KubosUtilsTest(KubosTestCase):
    test_key = 'test_key'
    test_value = 'lorem ipsum'

    def setUp(self):
        super(KubosUtilsTest, self).setUp()
        self.json_file = os.path.join(self.base_dir, 'test.json')
        self.test_data = { module_key : { self.test_key : self.test_value} }


    def test_check_link(self):
        with open(self.json_file, 'w') as json_file:
            json_file.write(json.dumps(self.test_data))
        #Verify element in the file is True
        self.assertTrue(check_link(self.json_file, module_key, self.test_key))
        #Verify element not in the file is False
        self.assertFalse(check_link(self.json_file, module_key, None))


    def test_set_link(self):
        self.write_json_file(self.test_data)
        set_link(self.json_file, module_key, self.test_value)
        with open(self.json_file, 'r') as json_file:
            link_data = json.load(json_file)
        self.assertTrue(self.test_value in link_data[module_key])


    def test_remove_link(self):
        self.write_json_file(self.test_data)
        with open(self.json_file, 'r') as json_file:
            link_data = json.load(json_file)
        self.assertTrue(self.test_key in link_data[module_key])
        remove_link(self.json_file, module_key, self.test_key)
        with open(self.json_file, 'r') as json_file:
            link_data = json.load(json_file)
        self.assertFalse(self.test_key in link_data[module_key])


    def write_json_file(self, data):
        with open(self.json_file, 'w') as json_file:
            json_file.write(json.dumps(data))


    def tearDown(self):
        super(KubosUtilsTest, self).tearDown()


if __name__ == '__main__':
    unittest.main()
