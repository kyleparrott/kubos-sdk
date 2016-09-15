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

from pip.utils import ensure_dir, get_installed_version
from options import parser
from utils import container

def addOptions(parser):
    pass


def execCommand(args, following_args):
    print "KubOS-SDK:\t\t%s" % (get_kubos_sdk_version())
    print "KubOS-SDK Container:\t%s" % (get_container_tag())


def get_kubos_sdk_version():
    return get_installed_version('kubos-sdk')


def get_container_tag():
    cli = container.get_cli()
    expected_ver = container.container_tag()
    found = False
    kubos_images = cli.images(name='kubostech/kubos-sdk')
    for image in kubos_images:
        if image['RepoTags'] is not None:
            found_ver = image['RepoTags'][0][-5:]
            if expected_ver == found_ver:
                found = True
    if found:
        return expected_ver
    else:
        return "Container %s Not Found - Please run `kubos update`" % expected_ver

