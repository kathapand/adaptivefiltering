#!/bin/bash

# Deploy to ssc-jupyter.iwr.uni-heidelberg.de

set -e

# Push the built images to our JupyterHub instance
docker login ssc-jupyter.iwr.uni-heidelberg.de:5000
docker push ssc-jupyter.iwr.uni-heidelberg.de:5000/filter-library-free:latest
docker push ssc-jupyter.iwr.uni-heidelberg.de:5000/filter-library-proprietary:latest
docker logout

# Retag the public image and push it to DockerHub
docker tag ssc-jupyter.iwr.uni-heidelberg.de:5000/filter-library-free:latest ssciwr/adaptivefiltering:latest
docker login
docker push ssciwr/adaptivefiltering:latest
docker logout
