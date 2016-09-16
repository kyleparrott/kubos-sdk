#!/usr/bin/python
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

'''
This is a script to simplfiy building a wheel distribution of the kubos-sdk.
Currently this script assumes that you have already compiled the library. This script then copies the
required dylib to the appropriate location in the kubos-sdk working tree. It also copies
the analytics script into the sdk as well. It will in the future build the
analytics libraries and copy them in as well.
This assumes that your working tree looks like:

kubos
|-- ...
|-- sdk
|    |-- kubos-analytics
|    |-- kubos-sdk

'''

import os
import shutil
import subprocess
import sys

this_dir = os.path.dirname(__file__)

analytics_dir = os.path.join(this_dir, '..', 'kubos-analytics')
build_dir = os.path.join(analytics_dir, 'build')
dylib = os.path.join(build_dir, 'libanalytics.dylib')
analytics = os.path.join(analytics_dir, 'kubos', 'analytics.py')

analytics_dest = os.path.join(this_dir, 'kubos', 'analytics.py')
dylib_dest = os.path.join(this_dir, 'lib', 'osx', 'libanalytics.dylib')
setup_py = os.path.join(this_dir, 'setup.py')

def check_file(_file):
    if not os.path.isfile(_file):
        print >>sys.stderr, 'Error: file %s does not exist' % _file
        sys.exit(1)

def copy(src, dst):
    '''This function exits if there was an error copying the src file to the dest
    if the file already exists at the dst it continues as normal. shutil.copy does not
    have a return value
    '''
    try:
        shutil.copyfile(src, dst)
    except shutil.Error:
        print 'The source and destination files are the same. Nothing to copy'
    except:
        print >>sys.stderr, 'There was an error copying %s to %s.\nAborting..' % (src, dst)
        sys.exit(1)


def run_build():
    check_file(dylib)
    check_file(analytics)

    print 'Copying Dylib...'
    copy(dylib, dylib_dest)

    print 'Copying Analytics.py...'
    copy(analytics, analytics_dest)

    print 'Starting Wheel Build'
    subprocess.call([sys.executable, setup_py, 'bdist_wheel', '--universal'])
    print 'Build Complete'

if __name__ == '__main__':
    run_build()
