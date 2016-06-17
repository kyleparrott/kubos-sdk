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

import logging

from options import parser
from utils import container

def addOptions(parser):
    pass

def execCommand(args, following_args):
    logging.warning('This command is not yet fully implemented by the kubos-sdk. It might not work correctly yet.\n')
    container.pass_through(args.subcommand_name, *following_args)

