import json
import os
import shutil
import distutils.cmd
from setuptools import setup, find_packages

setup_data = json.load(open("setup.json", "r"))

for ascii_key in ("name", "version"):
    setup_data[ascii_key] = setup_data[ascii_key].encode("ascii")

setup_data["packages"] = find_packages()

setup( data_files = [
		('flash/mspdebug', ['flash/mspdebug/flash.sh']),
		('flash/openocd',  ['flash/openocd/flash.sh',
			                'flash/openocd/osxusb.py',
		                    'flash/openocd/stm32f407g-disc1.cfg', 
		                    'flash/openocd/stm32f407vg.cfg'])
		],
	  **setup_data)