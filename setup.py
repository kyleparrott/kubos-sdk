import distutils.cmd
import os
import shutil
import yaml
from setuptools import setup, find_packages

'''Distutils requires all strings/objects to be ascii encoded. By default json.load
unicode encodes strings. Rather than manually go through and ascii encode each
object (setup_data is a complex object) using yaml ascii encodes everything by default'''

module_data = yaml.safe_load(open("module.json", "r"))
setup_data = yaml.safe_load(open("setup.json", "r"))


for key in module_data:
    setup_data[key] = module_data[key]

setup_data["packages"] = find_packages()

setup(**setup_data)
