import json
import os
import shutil
import distutils.cmd
from setuptools import setup, find_packages

setup_data = json.load(open("setup.json", "r"))

for ascii_key in ("name", "version"):
    setup_data[ascii_key] = setup_data[ascii_key].encode("ascii")

setup_data["packages"] = find_packages()

setup(classifiers=[
        'Programming Language :: Python :: 2.7'
        ],
        data_files=[
        ('/kubos/utils',                ['kubos/utils/getip.sh']),
        ('/kubos/flash/mspdebug', ['flash/mspdebug/flash.sh']),
        ('/kubos/flash/dfu_util', ['flash/dfu_util/flash.sh']),
        ('/kubos/flash/openocd',  ['flash/openocd/flash.sh',
                                  'flash/openocd/osxusb.py',
                                  'flash/openocd/stm32f407g-disc1.cfg',
                                  'flash/openocd/stm32f407vg.cfg',
                                  'flash/openocd/mem_helper.tcl',
                                  'flash/openocd/stm32f4x_stlink.cfg']),
        ('/kubos/flash/openocd/interface',  ['flash/openocd/interface/stlink-v2.cfg',
                                            'flash/openocd/interface/stlink-v2-1.cfg']),
        ('/kubos/flash/openocd/target',   ['flash/openocd/target/stm32f4x.cfg',
                                            'flash/openocd/target/stm32f4x_stlink.cfg',
                                            'flash/openocd/target/swj-dp.tcl']),

        ('/kubos/bin/linux',      ['bin/linux/mspdebug',
                                  'bin/linux/openocd',
                                  'bin/linux/dfu-util']),
        ('/kubos/bin/osx',        ['bin/osx/openocd',
                                  'bin/osx/mspdebug',
                                  'bin/osx/dfu-util']),
        ('/kubos/lib/linux',      ['lib/linux/libmsp430.so',
                                  'lib/linux/libudev.so.0',
                                  'lib/linux/libusb-1.0.so.0',
                                  'lib/linux/libhidapi-hidraw.so.0']),
        ('/kubos/lib/osx',        ['lib/osx/libmsp430.dylib'])],
        entry_points={
            'console_scripts': [
                'kubos=kubos:main'
            ]
        },
        test_suite='kubos.test',
        **setup_data)
