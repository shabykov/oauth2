#!/usr/bin/env bash

sudo docker container prune -f
sudo docker volume prune -f
sudo docker image prune -f
