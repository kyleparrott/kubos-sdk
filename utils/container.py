import sys
import docker
from docker import Client


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
