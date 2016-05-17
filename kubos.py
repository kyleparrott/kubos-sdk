#!/usr/bin/env python
import argparse
import json
import os
import sys
import time

from docker import Client
import docker

container_name = 'kubostech/kubos-sdk'

def main():
	parser = argparse.ArgumentParser('Kubos SDK')
	subparser = parser.add_subparsers(dest='command', help='Available Kubos-sdk commands')
	
	init_parser   = subparser.add_parser('init', help='initialize a new kubos project in the current directory')
	update_parser = subparser.add_parser('update', help='pull latest kubos-sdk docker container')
	target_parser = subparser.add_parser('target', help='set or display the current target hardware platform')

	init_parser.add_argument('proj_name', nargs=1, type=str)
	target_parser.add_argument('target', nargs='?', type=str)
	
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
	

def get_cli():
	if sys.platform.startswith('linux'):
		return Client(base_url='unix://var/run/docker.sock') #use with docker-engine
	elif sys.platform.startswith('darwin'):
		return docker.from_env(assert_hostname=False) #use with docker-machine


if __name__ == '__main__':
	main()
