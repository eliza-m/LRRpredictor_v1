# This branch is currently ongoing work :exclamation:

TODO: there are some differences in prediction (however not major) using the updated RaptorX & HHsuite.
A retraining of the data is currently in progress :exclamation:.
 
 

### Installation & initial setup 
#### Cloning the project

Please be sure you are cloning the project in a location where you have write permissions and at least 5 GB available :exclamation:.
RaptorX-Property path generation mechanism when installing :exclamation: requires the project to be placed anywhere in the home directory - '/home/username/.../'. This limitation will be solved in LRRpredictor v1.1.

	# You can clone the project it anywhere in your home directory. This is only an example...
	cd /home/***replace_with_your_username***/
	
	git clone --recursive https://github.com/eliza-m/LRRpredictor_v1
	
#### Setting up environment variables
Check that you see ` LRRpredictor_v1 ` directory, when issueing :

	ls -l
	
The following variables should not be changed for now. In the following update we plan to make the installation more customisable.

	echo "export LRRpredictor_HOME="$(pwd)"/LRRpredictor_v1" >> ~/.bashrc
	
Setup the number of threads you would like to be used by `make` tool when building the project. This variable will not be further used.

	export MakeNoOfThreads=4
	
Setup the path where Uniprot20 database will be stored. Please be sure that you have ~50 GB disk space available :exclamation:. This can be downloaded anywhere on your computer as further on symbolic links will be set for the exact path to this database.

	echo "export UNIPROT20_PATH=/***replace_with_your_path***/" >> ~/.bashrc
	
If you just want to use LRRPredictor, keep the bellow variable set to `FALSE`. If you want to download additional training data used for cross validation and testing that is not necessary for prediction, set the bellow variable to `TRUE`:

	export isFullDownloadSet=FALSE

Update the new environmental variables for current terminal session

	source ~/.bashrc
	
#### Building, installing and setting up the project
A whole setup workflow for HHsuite, RaptorX-Property and LRRpredictor and also for downloading all the needed files will be performed by typing:

	cd ${LRRpredictor_HOME}
	git checkout update_submodules 
	
	bash setupAll.sh
	
Now the installation is complete. You can use now LRRpredictor. 

  
  
## Usage

LRRpredictor can be used with the following sintax:
	
	cd $LRRpredictor_HOME

	python3 LRRpred.py <file.fasta> <OuputDirectory>
	
An example is provided for testing the installation :

	python3 LRRpred.py gpa2.fasta results_new
	
The provided input file needs to be in fasta format. At the moment only single sequence files can be provided. :exclamation:






