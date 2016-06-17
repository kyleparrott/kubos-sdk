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
    kubos_images = cli.images(name='kubostech/kubos-sdk')
    if len(kubos_images) > 0 and 'RepoTags' in kubos_images[0]:
        tag_name = kubos_images[0]['RepoTags'][0]
        return tag_name.replace("kubostech/kubos-sdk:", "")
    return "None Found"

