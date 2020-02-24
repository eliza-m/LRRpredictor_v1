# LRRpredictor v1.0

LRRpredictor is an open-source tool for detecting LRR motifs within leucine rich repeats proteins.

# Warning ! Currently the github project is being uploaded... Please return in a few days...

# Instalation & Usage

## A. Docker 
(in progress...)

## B. Build from source - Ubuntu 14.04 and newer
### Prerequisites:
* gcc 5.4 and higher
* Cmake 3.1 and higher
* Python 3.6 and higher
* scikit-learn v0.22
* imbalanced-learn v0.6.1
* Numpy v1.17 and higher

You can install them by:

	sudo apt-get install build-essential, cmake
	sudo apt-get install python3.6, python3-pip
	

If you have Ubuntu 14.04 or 16.04, additional steps might be required to install Python3.6. Please see [link1](http://ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/) and [link2](http://devopspy.com/python/install-python-3-6-ubuntu-lts/)

Before continuing please check that you are using Python 3.6 or higher by typing:
	
	python3
	exit()
	
Futher you can install Scikit-learn and Imbalanced-learn libraries using pip :

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

Setup the number of threads you would like to be used by Make tool when building the project. This variable will not be further used.

	export MakeNoOfThreads=4
	
Setup the path where Uniprot20 database will be stored. Please be sure that you have ~50 GB disk space available. This can be downloaded anywhere on your computer as further on symbolic links will be set for the exact path to this database.

	echo "export UNIPROT20_PATH=/***replace_with_your_path***/" >> ~/.bashrc
	
If you want just to use LRRPredictor, let the bellow variable to "FALSE" value. If you want to download additional training data used for cross validation and testing that is not necessary for prediction, set the bellow variable to TRUE value:

	export isFullDownloadSet=FALSE

Update the new environmental variables for current terminal session

	source ~/.bashrc
	

#### Building, installing and setting up the project
	
Make sure that the path set before for Uniprot20 database is still reachable and you see a bunch of files when issueing:
	
A whole setup for HHsuite, RaptorX-Property and LRRpredictor and downloading all needed files will be performed by typing:

	cd ${LRRpredictor_HOME}
	bash setupAll.sh
  
#### Usage

	python3 LRRpred.py <file.fasta> <OuputDirectory>
	
Please test the example provided:

	python3 LRRpred.py gpa2.fasta results
	

