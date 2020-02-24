# LRRpredictor v1.0

LRRpredictor is an open-source tool for detecting LRR motifs within leucine rich repeats proteins.

# Warning ! Currently the github project is being uploaded... Please return in a few days...

# Instalation & Usage

## A. Docker 
(in progress...)

## B. Build from source - Ubuntu 16.04 and newer
### Prerequisites:
* gcc 5.4 and higher
* Cmake 3.1 and higher
* Python 3.6 and higher

You can install them by:

	sudo apt-get install build-essential, cmake
	sudo apt-get install python3.6, python3-pip
	

If you have Ubuntu 14.04 it is also possible to install, but additional steps are required for installing Python3.6. Please see the following links :

ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/

devopspy.com/python/install-python-3-6-ubuntu-lts/

Before continuing please check that you have a functional Python 3.6 version by typing:
	
	python3
	exit()
	
Futher we install some additional libraries:

	pip3 install scikit-learn==0.22 imbalanced-learn==0.6.1



### Cloning the project
Please be sure you are cloning the project in a location where you have write permissions and at least 5 GB available.

	git clone --recursive https://github.com/eliza-m/LRRpredictor_v1
	
### Setting up environment variables

The following variables should not be changed for now :

	echo "export LRRpredictor_HOME="$(pwd)"/LRRpredictor_v1" >> ~/.bashrc
	echo "export RaptorX_HOME="$(pwd)"/LRRpredictor_v1/RaptorX_Property_Fast" >> ~/.bashrc
	echo "export HHSUITE_HOME="$(pwd)"/LRRpredictor_v1/hh-suite" >> ~/.bashrc
	export HHSUITE_INSTALL_BASE_DIR=$(pwd)/LRRpredictor_v1/hh-suite	
	echo "export HHLIB="${HHSUITE_INSTALL_BASE_DIR} >> ~/.bashrc
	echo 'export PATH=${PATH}:'${HHSUITE_INSTALL_BASE_DIR}"/bin:"${HHSUITE_INSTALL_BASE_DIR}"/scripts" >> ~/.bashrc
	
In the follwing update we plan to make the instalation more customisable. 	

Setup the number of threads you would like to be used by Make tool when building the project. 

	export MakeNoOfThreads=4

Update the new settings for current terminal session

	source ~/.bashrc
	
### Downloading Uniprot20 database
Please be sure that you have ~50 GB available. This can be downloaded anywhere on your computer as further on symbolic links will be set for the exact path to this database.

	export UNIPROT20_PATH=/replace_with_your_path/
	
	mkdir ${UNIPROT20_PATH}
	
	cd ${UNIPROT20_PATH}
	
	wget http://wwwuser.gwdg.de/~compbiol/data/hhsuite/databases/hhsuite_dbs/old-releases/uniprot20_2016_02.tgz
	
	tar -xvzf uniprot20_2016_02.tgz
  
As we do not need the archive anymore, we can delete it

	rm uniprot20_2016_02.tgz

### Downloading Training PKL files 

	cd ${LRRpredictor_HOME}/crossValidation
	wget ......
  
	cd ${LRRpredictor_HOME}/test
	wget ...
  
	cd ${LRRpredictor_HOME}/fullTraining
	wget ...
	tar -xzf fullTraining_pkls.tar.gz
	mv fullTraining_pkls/* ./
	rm fullTraining_pkls.tar.gz
	rmdir fullTraining_pkls
 
  
#### Building, installing and setting up the project

	cd ${LRRpredictor_HOME}
	
Make sure that the path set before for Uniprot20 database is still reachable and you see a bunch of files when issueing:

	ls ${UNIPROT20_PATH}/uniprot20_2016_02/
	
A whole setup for HHsuite, RaptorX-Property and LRRpredictor will be performed by typing:

	./setupAll.sh
  
#### Usage

	python3 LRRpred.py gpa2.fasta
	

