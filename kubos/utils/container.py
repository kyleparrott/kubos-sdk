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

import docker
import dockerpty
import json
import os
import subprocess
import sys
import time
import threading

from . import status_spinner
from docker import Client
from pip.utils import ensure_dir, get_installed_version
from project import get_local_link_file, module_key, target_key, target_mount_dir

container_repo = 'kubostech/kubos-sdk'

def container_tag():
    # Today our container version is linked to the version of the pip module kubos-sdk.
    return get_installed_version('kubos-sdk')

def get_cli():
    if sys.platform.startswith('linux'):
        c = Client(base_url='unix://var/run/docker.sock') #use with docker-engine
    elif sys.platform.startswith('darwin'):
        c = docker.from_env(assert_hostname=False) #use with docker-machine

    check_docker_status(c)
    return c


def check_docker_status(client):
    try:
        client.ping()
    except:
        print >>sys.stderr, 'Error: Unable to communicate with the Docker service. Please ensure this service is running and you have permission to access it.'
        sys.exit(1)


def pass_through(*args):
    python = '/usr/bin/python'
    sdk_script = '/kubos-sdk/kubos-sdk.py'
    arg_list = list(args)
    arg_list.insert(0, python)
    arg_list.insert(1, sdk_script)
    try:
        run_container(arg_list)
        if sys.platform.startswith('linux'):
            fix_permissions()
    except docker.errors.NotFound:
        print "The correct container was not found"
        print "Please run `kubos update` and try again"


def fix_permissions():
    cwd = os.getcwd()
    userstr = "%s:%s" % (os.getuid(), os.getgid())
    arg_list = list()
    arg_list.insert(0, "chown")
    arg_list.insert(1, userstr)
    arg_list.insert(2, cwd)
    arg_list.insert(3, "-R")
    run_container(arg_list)


def run_container(arg_list):
    cwd = os.getcwd()
    cli = get_cli()

    image_name = "%s:%s" % (container_repo, container_tag())
    host_config = cli.create_host_config(binds=mount_volumes())
    container_data = cli.create_container(image=image_name,
                                          command=arg_list,
                                          host_config=host_config,
                                          working_dir=cwd,
                                          tty=True)
    container_id = container_data['Id'].encode('utf8')
    if container_data['Warnings']:
        print "Warnings: ", container_data['Warnings']
    stdout_lock = threading.Lock()
    spinner = status_spinner.start_spinner(stdout_lock)
    cli.start(container_id)

    container_output = cli.attach(container=container_id, stream=True)
    for entry in container_output:
        with stdout_lock:
            sys.stdout.write(entry)
    cli.stop(container_id)
    cli.remove_container(container_id)
    status_spinner.stop_spinner(spinner)


def get_uid():
    '''This returns an array with the current user id in a single element string array
    This is used in the container so that the user in the container has the same uid
    as the user on the host to avoid permission errors after container commands run'''
    uid = os.getuid()
    return ['LOCAL_USER_ID=%s' % uid]

def json_events(iter):
    # docker-py inconsistently streams json data through the iterator interface,
    # sometimes as a single line, multiple lines, or even partial lines.
    # this function noramlizes that behavior by keeping a running buffer when
    # json parsing fails, and only yielding on json parse success. see KUBOS-125

    lines = []
    for data in iter:
        new_lines = data.splitlines()
        if len(lines) > 0:
            lines[0] += new_lines.pop(0)
        lines.extend(new_lines)

        while len(lines) > 0:
            line = lines.pop(0)
            try:
                yield json.loads(line)
            except:
                lines.append(line)
                break

def update_container():
    print "Checking for latest KubOS-SDK.."
    cli = get_cli()
    stdout_lock = threading.Lock()
    spinner = status_spinner.start_spinner(stdout_lock)
    for event in json_events(cli.pull(repository=container_repo,
                                      tag=container_tag(), stream=True)):
        with stdout_lock:
            if 'error' in event:
                print event['error'].encode('utf8')
            elif 'progress' in event:
                sys.stdout.write('\r%s' % event['progress'].encode('utf8'))
                sys.stdout.flush()
                time.sleep(0.1)
            elif 'status' in event:
                print event['status'].encode('utf8')

    print "All up to date!\n"
    status_spinner.stop_spinner(spinner)

def debug(arg_list):
    cwd = os.getcwd()
    cli = get_cli()
    image_name = "%s:%s" % (container_repo, container_tag())
    bind_dirs = mount_volumes()

    container_data = cli.create_container(image=image_name,
                                          command=arg_list,
                                          host_config=cli.create_host_config(
                                              port_bindings={3333:3333},
                                              network_mode='host',
                                              binds=bind_dirs
                                          ),
                                          working_dir=cwd,
                                          tty=True,
                                          stdin_open=True,
                                          ports=[3333])

    container_id = container_data['Id'].encode('utf8')

    if container_data['Warnings']:
        print "Warnings: ", container_data['Warnings']
    if sys.platform.startswith('darwin'):
        darwin_debug(arg_list, bind_dirs)
    else:
        dockerpty.start(cli, container_id)
        cli.stop(container_id)
        cli.remove_container(container_id)


def mount_volumes():
    #mount configuration for linked modules
    cwd = os.getcwd()
    bind_dirs = []
    local_link_file = get_local_link_file()
    if os.path.isfile(local_link_file):
        with open(local_link_file, 'r') as link_file:
            link_data = json.load(link_file)
            module_links = link_data[module_key]
            target_links = link_data[target_key]
        for key in module_links:
            # in the container modules are mounted at their absolute path on the host
            path_spec = '%s:%s' % (module_links[key], module_links[key])
            bind_dirs.append(path_spec)
        for key in target_links:
            target_dir_name = os.path.basename(target_links[key])
            target_path = os.path.join(target_mount_dir, target_dir_name)
            path_spec = '%s:%s' % (target_links[key], target_links[key])
            bind_dirs.append(path_spec)
    cwd_bind = '%s:%s' % (cwd, cwd)
    bind_dirs.append(cwd_bind)
    return bind_dirs


def darwin_debug(command, bind_dirs):
    '''
    Currently docker-py does not correctly support running pseudo terminals into docker containers on mac or linux.
    Dockerpty correctly implements this functionality but only on Linux. For now this builds the full docker CLI 
    command for all mounted volumes and runs the command directly. This is not a long term solution.
    '''
    args = ['docker', 'run', '--rm', '-it']
    volume_fmt = '-v'
    for directory in bind_dirs:
        args.append(volume_fmt)
        args.append(directory)
    image_name = "%s:%s" % (container_repo, container_tag())
    args.append(image_name)
    args = args + command
    subprocess.call(args)

