#!/bin/bash

set -ev

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker manifest push dullage/gunicorn-python:3.8
docker manifest push dullage/gunicorn-python:3.8-alpine
docker manifest push dullage/gunicorn-python:latest
