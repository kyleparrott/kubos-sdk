#!/usr/bin/env python
import argparse
import json
import os
import sys

from docker import Client
import docker

container_name = 'kubostech/kubos-sdk'

def main():
	parser = argparse.ArgumentParser('kubos-host script for Kubos SDK')
	parser.add_argument('--update', action='store_true', help='pull latest sdk container')
	args, unknown_args = parser.parse_known_args()

	if args.update:
		update()
	elif unknown_args:
		pass_through(*unknown_args)
	else:
		parser.print_help()
		pass_through('--help')

def update():
	print "updating"
	cli = get_cli()
	for line in cli.pull(container_name, stream=True):
	   print json.dumps(json.loads(line), indent=4)

def pass_through(*args):
	cwd = os.getcwd() 
	cli = get_cli()
	python = '/usr/bin/python'
	sdk_script = '/kubos-sdk/kubos-sdk.py' 
	kubos_sdk_cmd =  ' '.join([python, sdk_script])
	arg_list = list(args)
	arg_list.insert(0, kubos_sdk_cmd)

	command = ' '.join(arg_list)

	container_data = cli.create_container(image=container_name, command=command, working_dir=cwd, tty=True)
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