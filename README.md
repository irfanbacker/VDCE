# VDCE

Virtual data center embedding problem ([ESP-VDCE](https://ieeexplore.ieee.org/document/9148838)) using alib-py3.

Build docker image using: `sudo docker build . -t "alib-py3"`\
Start docker container using: `sudo docker run --privileged -it --mount type=bind,source="$(pwd)",target=/home/vdce alib-py3`

Note: Add Gurobi Web License Service (WLS) file (Named as gurobi.lic) in root folder for docker container to work
