# LRRpredictor v1.0

LRRpredictor is an open-source tool for detecting LRR motifs within leucine rich repeats proteins.

# Warning ! Currently the github project is being uploaded... Please return in a few days...

# Instalation & Usage

## A. Docker 
(in progress...)

## B. Build from source - Ubuntu 
### Prerequisites:
* gcc 5.4 and higher
* Cmake 3.1 and higher
* Python 3.6 and higher

You can install them by:

	sudo apt-get install ....
	
	pip3 install ...

### Cloning the project
Please be sure you are cloning the project in a location where you have write permissions and at least 5 GB available.

	git clone --recursive https://github.com/eliza-m/LRRpredictor_v1
	
### Setting up environment variables

	echo "export LRRpredictor_HOME=($pwd)/LRRpredictor_v1" >> ~/.bashrc
	echo "export RaptorX_HOME=($pwd)/LRRpredictor_v1/RaptorX_Property_Fast" >> ~/.bashrc
	echo "export HHSUITE_HOME=($pwd)/LRRpredictor_v1/hh-suite" >> ~/.bashrc
	
	export HHSUITE_INSTALL_BASE_DIR=${HHSUITE_HOME} 	# you can change the installation folder if desired
	echo "export HHLIB=${HHSUITE_INSTALL_BASE_DIR}
	echo "export PATH=${PATH}:${HHSUITE_INSTALL_BASE_DIR}/bin:${HHSUITE_INSTALL_BASE_DIR}/scripts
	
	export MakeNoOfThreads=4	# number of threads used when running make

	source ~/.bashrc	# updating the settings for current terminal session
	
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
 
  
#### Building, installing and setting up the project

	cd ${LRRpredictor_HOME}
	
Make sure that the path set before for Uniprot20 database is still reachable and you see a bunch of files when issueing:

	ls ${UNIPROT20_PATH}/uniprot20_2016_02/
	
A whole setup for HHsuite, RaptorX-Property and LRRpredictor will be performed by typing:

	./setupAll.sh
  
#### Usage

	python3 LRRpred.py gpa2.fasta
	

