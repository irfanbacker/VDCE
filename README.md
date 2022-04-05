# VDCE

Virtual data center embedding problem (ESP-VDCE) using alib-py3.

Build docker image using: `sudo docker build . -t "alib-py3"`\
Start docker container using: `sudo docker run --privileged -it --mount type=bind,source="$(pwd)",target=/home/vne_input alib-py3`

Note: Add gurobi.lic file (Gurobi web license) in root folder for docker container to work
