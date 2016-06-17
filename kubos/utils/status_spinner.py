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

import sys
import threading
import time

class StatusSpinner(threading._Timer):
    def run(self):
        spinner = self.get_spinner()
        while True:
            sys.stdout.write(spinner.next())
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')

    def get_spinner(self):
        while True:
            for symbol in '|/-\\':
                yield symbol


def start_spinner():
    spinner = StatusSpinner(0.1, None)
    spinner.daemon = True
    spinner.start()
    return spinner


def stop_spinner(spinner):
    spinner.cancel()

