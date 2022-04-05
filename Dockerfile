FROM ubuntu:20.04

RUN apt update
# Install python
RUN apt install -y python3 python3-pip
RUN python3 --version
# Sym link for python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Setup python virtual env
# RUN python -m venv venv
# RUN source venv/bin/activate

# Install python dependencies
RUN pip3 install coverage
RUN pip3 install gitlint
RUN pip3 install pre-commit
RUN pip3 install pylint
RUN pip3 install pytest

#Install alib dependencies
RUN pip3 install gurobipy
RUN pip3 install numpy
RUN pip3 install networkx
RUN pip3 install matplotlib
RUN pip3 install click

#Gurobi setup
WORKDIR /opt/
RUN apt install -y curl
RUN echo "#!/bin/bash" > getGurobi.sh\
    && echo 'fileid="1BXk5RxP8LwsJOCz3HqfW4WsUMfeB9YTj"' >> getGurobi.sh\
    && echo 'filename="gurobi.tar.gz"' >> getGurobi.sh\
    && echo 'html=`curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}"`' >> getGurobi.sh\
    && echo 'curl -Lb ./cookie "https://drive.google.com/uc?export=download&`echo ${html}|grep -Po "(confirm=[a-zA-Z0-9\-_]+)"`&id=${fileid}" -o ${filename}' >> getGurobi.sh\
    && chmod +x getGurobi.sh\
    && ./getGurobi.sh\
    && rm -rf getGurobi.sh\
    && tar -xzf gurobi.tar.gz

ENV GUROBI_HOME=/opt/gurobi951/linux64
ENV PATH=$GUROBI_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=/opt/gurobi951/linux64/lib
WORKDIR /opt/gurobi951/
ADD gurobi.lic gurobi.lic

#alib setup
WORKDIR /home/
RUN apt install -y git
RUN git clone https://github.com/vnep-approx-py3/alib-py3.git
RUN mkdir alib-experiments && cd alib-experiments
RUN mkdir input && mkdir output && mkdir logs
ENV ALIB_EXPERIMENT_HOME=/home/alib-experiments

WORKDIR /home/alib-py3/
RUN pip3 install .

WORKDIR /home/