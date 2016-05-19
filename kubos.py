#!/usr/bin/env python
import argparse
import json
import os
import sys
import subprocess
import time

from docker import Client
import docker

container_name = 'kubostech/kubos-sdk'
yotta_meta_file = '.yotta.json'
module_file_name = 'module.json'

def main():
    parser = argparse.ArgumentParser('Kubos SDK')
    subparser = parser.add_subparsers(dest='command', help='Available Kubos-sdk commands')

    build_parser  = subparser.add_parser('build', help='build the project in the current directory')
    flash_parser  = subparser.add_parser('flash', help='launch the built executable')
    init_parser   = subparser.add_parser('init', help='initialize a new kubos project in the current directory')
    target_parser = subparser.add_parser('target', help='set or display the current target hardware platform')
    update_parser = subparser.add_parser('update', help='pull latest kubos-sdk docker container')

    build_parser.add_argument('--verbose', action='store_true', default=False)
    init_parser.add_argument('proj_name', nargs=1, type=str)
    target_parser.add_argument('target', nargs='?', type=str)
    
    build_parser.set_defaults(func=pass_through)
    init_parser.set_defaults(func=pass_through)
    target_parser.set_defaults(func=pass_through)
    update_parser.set_defaults(func=update)

    args, unknown_args = parser.parse_known_args()
    provided_args = vars(args)

    command = provided_args['command']
    if command == 'init':
        proj_name = provided_args['proj_name'][0]
        pass_through(command, proj_name)
    elif command == 'target':
        target = provided_args['target'] 
        if target:
            pass_through(command, target)
        else:
            pass_through(command)
    elif command == 'update':
        update()
    elif command == 'build':
        if provided_args['verbose']:
            pass_through(command, '--verbose')
        else:
            pass_through(command)
    elif command == 'flash':
        flash()


def update():
    cli = get_cli()
    for line in cli.pull(container_name, stream=True):
       json_data = json.loads(line)
       if 'error' in json_data:
            print json_data['error'].encode('utf8')
       elif 'progress' in json_data:
            sys.stdout.write('\r%s' % json_data['progress'].encode('utf8'))
            time.sleep(0.1)
            sys.stdout.flush()
       elif 'status' in json_data:
            print json_data['status'].encode('utf8')


def pass_through(*args):
    cwd = os.getcwd() 
    cli = get_cli()
    python = '/usr/bin/python'
    sdk_script = '/kubos-sdk/kubos-sdk.py' 
    arg_list = list(args)
    arg_list.insert(0, python)
    arg_list.insert(1, sdk_script)

    container_data = cli.create_container(image=container_name, command=arg_list, working_dir=cwd, tty=True)
    container_id = container_data['Id'].encode('utf8')
    if container_data['Warnings']:
        print "Warnings: ", container_data['Warnings']

    cli.start(container_id, binds={
        cwd : {
            'bind': cwd,
            'ro': False
        }   
    })
    container_output = cli.logs(container=container_id, stream=True)
    for entry in container_output:
        sys.stdout.write(entry)

    cli.stop(container_id)
    cli.remove_container(container_id)


def flash():
    current_target = get_current_target()
    if current_target:
        project_name = get_project_name()

        if not project_name:
            print >>sys.stderr, 'Error: No module.json file found. Run "kubos build" in the root directory of your project'
            sys.exit(1)

        install_dir = os.path.dirname(os.path.realpath(__file__))
        exe_path =  os.path.join(os.getcwd(), 'build', current_target, 'source', project_name)

        if current_target.startswith('stm32'):
            flash_script_path = str(os.path.join(install_dir, 'flash', 'openocd', 'flash.sh'))
            argument = 'stm32f4_flash %s' % exe_path
            subprocess.check_call(['/bin/sh', flash_script_path, argument])
        
        elif current_target.startswith('msp430'):
            flash_script_path = str(os.path.join(install_dir, 'flash', 'mspdebug', 'flash.sh'))
            argument = 'prog %s' % exe_path
            subprocess.check_call(['/bin/sh', flash_script_path, argument])
    else:
        print >>sys.stderr, 'Error: No target currently selected. Select a target and build before flashing'

def get_cli():
    if sys.platform.startswith('linux'):
        return Client(base_url='unix://var/run/docker.sock') #use with docker-engine
    elif sys.platform.startswith('darwin'):
        return docker.from_env(assert_hostname=False) #use with docker-machine

def get_project_name():
    module_file_path = os.path.join(os.getcwd(), module_file_name)
    if os.path.isfile(module_file_path):
         with open(module_file_path, 'r') as module_file:
            data = json.load(module_file)
            name = str(data['name'])
            return name
    else:
        return None

def get_current_target():
    meta_file_path = os.path.join(os.getcwd(), yotta_meta_file)
    if os.path.isfile(meta_file_path):
        with open(meta_file_path, 'r') as meta_file:
            data = json.load(meta_file)
            target_str = str(data['build']['target'])
            return target_str.split(',')[0]
    else:
        return None

if __name__ == '__main__':
    main()