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
import sys
import time
from options import parser
from utils import container, status_spinner

def addOptions(parser):
    pass

def execCommand(args, following_args):
    print "Checking for latest KubOS-SDK.."
    cli = container.get_cli()
    spinner = status_spinner.start_spinner()
    for data in cli.pull(repository=container.container_repo,
                         tag=container.container_tag, stream=True):
        for line in data.splitlines():
            json_data = json.loads(line)
            if 'error' in json_data:
                print json_data['error'].encode('utf8')
            elif 'progress' in json_data:
                sys.stdout.write('\r%s' % json_data['progress'].encode('utf8'))
                time.sleep(0.1)
                sys.stdout.flush()
            elif 'status' in json_data:
                print json_data['status'].encode('utf8')
    print "All up to date!\n"
    status_spinner.stop_spinner(spinner)

