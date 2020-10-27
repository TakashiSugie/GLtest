FROM nvidia/cudagl:10.1-devel-ubuntu18.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install -U pip

RUN pip3 install matplotlib

WORKDIR /GL

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs
