# Start from the bitnami minideb image
#FROM bitnami/minideb:stretch
FROM ubuntu:18.04

# Install packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils apt-transport-https openssh-client \
		git build-essential cmake python3 python3-pip \ 
		wget bash

# Install pip packages
RUN pip3 install scikit-learn==0.22 imbalanced-learn==0.6.1

# Clone the repo
RUN git clone --recursive https://github.com/eliza-m/LRRpredictor_v1

# Set environment variables
ENV LRRpredictor_HOME=/LRRpredictor_v1 RaptorX_HOME=/LRRpredictor_v1/RaptorX_Property_Fast HHSUITE_HOME=/LRRpredictor_v1/hh-suite  HHSUITE_INSTALL_BASE_DIR=/LRRpredictor_v1/hh-suite	
ENV HHLIB=${HHSUITE_INSTALL_BASE_DIR} PATH=${PATH}:${HHSUITE_INSTALL_BASE_DIR}/bin:${HHSUITE_INSTALL_BASE_DIR}/scripts
ENV MakeNoOfThreads=4

# Prepare Uniprot Download
RUN mkdir /uniprot20 && \
    mkdir /uniprot20/uniprot20_2016_02
ENV UNIPROT20_PATH /uniprot20
COPY download-uniprot.sh /download-uniprot.sh
COPY download_validation_set.sh /download_validation_set.sh


# Build HHsuite
WORKDIR /LRRpredictor_v1/hh-suite
RUN mkdir build
WORKDIR /LRRpredictor_v1/hh-suite/build
RUN cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX=${HHSUITE_INSTALL_BASE_DIR} ..
RUN make -j $MakeNoOfThreads
RUN make install

# Build RaptorX
WORKDIR /LRRpredictor_v1/RaptorX_Property_Fast/source_code
RUN make -j $MakeNoOfThreads
WORKDIR /LRRpredictor_v1/RaptorX_Property_Fast
RUN perl setup.pl
WORKDIR /LRRpredictor_v1/RaptorX_Property_Fast/databases
RUN rm uniprot20 && \
    ln -s /uniprot20/uniprot20_2016_02 uniprot20

# Download training data
WORKDIR /LRRpredictor_v1/fullTraining
RUN wget old.biochim.ro/ib/departments/strbiochem/LRRpred/fullTraining_pkls.tar.gz && \
	tar -xzf fullTraining_pkls.tar.gz && \
	mv fullTraining_pkls/* ./ && \
	rm fullTraining_pkls.tar.gz && \
	rmdir fullTraining_pkls

# Prepare the results folder
WORKDIR /LRRpredictor_v1
RUN mkdir results

WORKDIR /
