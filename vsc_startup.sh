#! /bin/bash

# create required folders for vsc-server config
mkdir -p ~/.config

# start all containers and give user id
EXAMPLE_UID=${UID} EXAMPLE_GID=${GID} docker-compose -p vsc-tasmotacharger up --build --detach
