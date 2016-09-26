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
import os
import sys
import time
import shutil
import subprocess

from options import parser
from pkg_resources import resource_filename
from utils import container, status_spinner, sdk

version = 'v%s' % sdk.get_sdk_attribute('version')
repo_dir = os.path.join(sdk.KUBOS_DIR, '.repo')
manifest_url = "git://github.com/kubostech/kubos-manifest"
manifest_file_name = 'docker-manifest.xml'
manifest_version_spec = 'refs/tags/%s' % version

def addOptions(parser):
    pass

def execCommand(args, following_args):
    '''
    The new update command does 3 main things to sync the kubos source tree:
    1) First it copies the container directory from the installed location of the kubos-sdk module into ~/.kubos/
          - This is done because on mac OS only the /Users/ Directory is shared with the container by default
          - If the module is installed by root it generally goes into /usr/... or /opt... which aren't shared by default
    2) Repo is copied out of the container to the host ~/.kubos/ directory. Repo has very werid and inconsistent behavior
            when running inside containers in testing on mac OS. Running repo on the host is the only way I have gotten 
            consisten behavior.
    3) It initializes and syncs the kubos source to ~/.kubos
    '''
    start_dir = os.getcwd()
    if not os.path.isdir(sdk.KUBOS_DIR):
        os.makedirs(sdk.KUBOS_DIR)
    os.chdir(sdk.KUBOS_DIR)
    if not os.path.isfile(sdk.CONTAINER_SCRIPT):
        print 'Copying container script to %s' % sdk.CONTAINER_DIR
        try:
            shutil.copytree(sdk.GLOBAL_CONTAINER_DIR, sdk.CONTAINER_DIR)
        except:
            print 'There was an error copying the container script %s to its destination %s' % (sdk.GLOBAL_CONTAINER_DIR, sdk.CONTAINER_DIR)
            sys.exit(1)
    repo_file = os.path.join(sdk.KUBOS_DIR, 'repo')
    if not os.path.isfile(repo_file):
        print 'The repo tool was not found, fetching it now...'
        container.run_container(['cp', '/usr/bin/repo', sdk.KUBOS_DIR], ['%s:%s' % (sdk.KUBOS_DIR, sdk.KUBOS_DIR)])
    try:
        if not os.path.isdir(repo_dir): #Repo only needs to be initialized once
            print 'initializing Kubos Source Directory'
            subprocess.check_call(['./repo', "init", "-u", manifest_url, "-m", manifest_file_name, "-b", manifest_version_spec, '--depth=1'])
        print 'Syncing the Kubos Source Tree. This may take a while...'
        subprocess.check_call(['./repo', "sync"])
    except:
        print 'There was a problem syncing the kubos source tree.'
        sys.exit(1)

    print '\n\nSuccessfully synced Kubos Library Source Code\n\n'
    os.chdir(start_dir)
