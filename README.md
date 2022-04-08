# VDCE

Virtual data center embedding problem ([ESP-VDCE](https://ieeexplore.ieee.org/document/9148838)) using alib-py3.

## Dependencies

- python3
- alib-py3

In order to make dependency setup easier, you can use the Dockerfile available in this repository and follow the following steps:

1. Build docker image using: `sudo docker build . -t "alib-py3"`\
2. Start docker container using: `sudo docker run --privileged -it --mount type=bind,source="$(pwd)",target=/home/vdce alib-py3`

Note: Add [Gurobi Web License Service (WLS)](https://www.gurobi.com/documentation/9.5/quickstart_linux/retrieving_a_web_license_s.html#subsection:clientlicenseWLS) file (Named as gurobi.lic) in root folder for docker container to work

## Usage

1. After setting up the dependecies, goto the repository root (Do this inside the container if using docker).
2. Run `python3 run.py`
