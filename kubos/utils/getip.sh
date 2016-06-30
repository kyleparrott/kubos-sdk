#! /bin/bash
docker-machine ssh "${DOCKER_MACHINE_NAME}" 'echo ${SSH_CONNECTION%% *}'
