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
import hashlib
import json
import os
import sys
import time

from appdirs import AppDirs
from pip.utils import get_installed_version
from utils import container

this_dir = os.path.dirname(os.path.abspath(__file__))

def load_config():
    return _config_class()

def load_sdk_version():
    return get_installed_version('kubos-sdk')

def load_container_info():
    cli = container.get_cli()
    kubos_images = cli.images(name='kubostech/kubos-sdk')
    if len(kubos_images) > 0 and 'RepoTags' in kubos_images[0]:
        tag_name = kubos_images[0]['RepoTags'][0]
        tag_name = tag_name.replace('kubostech/kubos-sdk:', '')
        return (kubos_images[0]['Id'], tag_name)
    return (None, None)

class KubosSDKConfig(object):
    def __init__(self):
        self.appdirs = AppDirs('kubos')
        self.config_path = os.path.join(self.appdirs.user_config_dir, 'kubos-sdk.json')
        self.sdk_version = load_sdk_version()
        self.sdk_edition = 'preview'
        self.container_tag, self.container_id = load_container_info()
        self.load_config()

    def load_config(self):
        self.config = {}
        if os.path.isfile(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)

    def save_config(self):
        if not os.path.isdir(self.appdirs.user_config_dir):
            os.makedirs(self.appdirs.user_config_dir)

        with open(self.config_path, 'w') as f:
            f.write(json.dumps(self.config))

_config_class = KubosSDKConfig
