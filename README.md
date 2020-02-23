# LRRpredictor v1.0

LRRpredictor is an open-source tool for detecting LRR motifs within leucine rich repeats proteins.

Currently the github project is being uploaded... Please return in a few days...

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
Please be sure you are cloning the project in a folder you have write permissions and at least 5 GB available.

  git clone --recursive https://github.com/eliza-m/LRRpredictor_v1
  
### Downloading Uniprot20 database
Please be sure that you have ~50 GB available. This can be downloaded anyware on your computer as symbolic links will be setted for the exact path to this database.

	export UNIPROT20_PATH= *** add you path - example : /storage/uniprot20 ***
	
	mkdir ${UNIPROT20_PATH}
	
	cd ${UNIPROT20_PATH}
	
	wget http://wwwuser.gwdg.de/~compbiol/data/hhsuite/databases/hhsuite_dbs/old-releases/uniprot20_2016_02.tgz
	
	tar -xvzf uniprot20_2016_02.tgz
  
As we do not need the archive anymore, we can delete it

	rm uniprot20_2016_02.tgz

### Downloading Training PKL files 

	cd crossValidation
	wget ......
  
	cd ../test
	wget ...
  
	cd ../fullTraining
	wget ...
  
	cd ../
  
#### Building and setting the project

Be sure you are in LRRpredictor_v1 folder

	./setupAll.sh
  


