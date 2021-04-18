# LRRpredictor v1.0

Content summary:
* [General Info](#general-info)
* [Project status](#project-status)
* [Installation](#installation)
* [Usage](#usage)
* [Cite LRRpredictor](#citing-lrrpredictor)
* [References](#references)


## General Info
LRRpredictor is an open-source tool for detecting LRR motifs within leucine rich repeats proteins.
It resides on secondary structure, relative solvent accessibility and disorder predictions that are performed using RaptorX-Property [1-4] and sequence variability profiles generated using HH-suite [5,6] on Uniprot20 sequence database.

## Project status 
Future updates planned for version 1.1:
* RaptorX-Property is currently being updated and as this is finished, LRRpredictor will integrate these updates as well as a newer version of HHsuite (currently not compatible with RaptorX-Property).
* The project cannot be installed on Ubuntu WSL (Windows Linux Subsystem) or MacOS. This will be fixed in v1.1.
* LRRpredictor currently accepts only single sequence input in FASTA format. A feature update for other sequence formats, as well as multiple sequence fasta input files is currently being implemented.  


## Installation

## a. Docker 
A docker image containing LRRpredictor readily installed and setup can be pulled from our repository.

0. Install Docker client. 
	* Docker Desktop for Windows or MAC - [click](https://www.docker.com/products/docker-desktop)
	* docker-ce-cli for Linux - [click](docs.docker.com/install/linux/docker-ce/ubuntu/)

1. First you need to download a security SSL certificate. 

For Ubuntu/Debian:
```
	sudo wget old.biochim.ro/ib/departments/strbiochem/LRRpred/193.231.158.8_5000.crt -O /usr/local/share/ca-certificates/193.231.158.8_5000.crt
	sudo update-ca-certificates
	sudo service docker restart
```
2. After the ca-certificate is set, the image can be pulled :
```
	sudo docker pull 193.231.158.8:5000/lrrpredictor:1.0.1
```
You can see the that the image has been pulled by :
```
	sudo docker image ls

REPOSITORY                        TAG                 IMAGE ID            CREATED             SIZE
193.231.158.8:5000/lrrpredictor   1.0.0               24d71f69f21f        4 hours ago         2.61GB
```
	
3. Run the docker image. Now the terminal promt has changed to `root@<IMAGE ID>`.
```
	sudo docker run -it 193.231.158.8:5000/lrrpredictor:1.0.1 bash
```

4. Further we will download Uniprot20 database. Make sure that you have around 50 GB disk space available at the location were the docker image is located ::exclamation:: :
```
	bash download-uniprot.sh
```
Additionally, if you want to download supplemental training data used for cross validation and testing that is not necessary for running LRRpredictor (these are not needed anymore for prediction):
```
	bash download-validation-set.sh
```

Everythong is setup and now you can use LRRpredictor - see [Usage](#usage) section.
	
	

## b. Build from source - only native Ubuntu 14.04 and newer distributions
### Prerequisites:
* gcc 5.4 and higher
* Cmake 3.1 and higher
* Python 3.6 and higher
* scikit-learn v0.22
* imbalanced-learn v0.6.1
* numpy v1.17 and higher

You can install them by:

	sudo apt-get install build-essential, cmake
	sudo apt-get install python3.6, python3-pip
	

If you have Ubuntu 14.04 or 16.04, additional steps might be required to install Python3.6 exclamation:. Please see [link1](http://ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/) and [link2](http://devopspy.com/python/install-python-3-6-ubuntu-lts/)

Before continuing please check that you are using Python 3.6 or higher by typing `python3`.
	
Further you can install Scikit-learn and Imbalanced-learn libraries using pip :

	pip3 install scikit-learn==0.22 imbalanced-learn==0.6.1 numpy


### Installation & initial setup 
#### Cloning the project
Please be sure you are cloning the project in a location where you have write permissions and at least 5 GB available :exclamation:.

	# You can clone the project it anywhere in your computer. This is only an example...
	cd /home/test/
	
	git clone --recursive https://github.com/eliza-m/LRRpredictor_v1
	
#### Setting up environment variables
Check that you see ` LRRpredictor_v1 ` directory, when issueing :

	ls -l
	
The following variables should not be changed for now. In the following update we plan to make the installation more customisable.

	echo "export LRRpredictor_HOME="$(pwd)"/LRRpredictor_v1" >> ~/.bashrc
	source  ~/.bashrc
	
#### Building, installing and setting up the project
A whole setup workflow for HHsuite, RaptorX-Property and LRRpredictor and also for downloading all the needed files will be performed by typing:

	cd ${LRRpredictor_HOME}
	bash setupAll.sh
	
	
#### Setting up the Uniprot20 database	
LRRpredictor requires the Uniprot20 database. The following steps need to be done only once, when LRRpredictor is set up for the first time.

**Case 1:** If you already have the Uniprot20 database in your computer, please run the following:

	UNIPROT20_PATH=/***replace_with_your_path***/"	
	
	# defining a symbolic link to point to your local Uniprot20 copy.
	cd ${LRRpredictor_HOME}/RaptorX_Property_Fast/databases
	rm uniprot20
	ln -s ${UNIPROT20_PATH}/uniprot20_2016_02 uniprot20
	cd ${LRRpredictor_HOME}
	
	
**Case 2:** If you do not have the Uniprot20 database, we will need download it.
Please be sure that you have ~50 GB disk space available :exclamation:. This can be downloaded anywhere on your computer as further on symbolic links will be set up for the exact path to this database.
	
	UNIPROT20_PATH=/***replace with the path where you want to download Uniprot***/"	
	
	# Downloading Uniprot20
	cd ${UNIPROT20_PATH}
	wget http://wwwuser.gwdg.de/~compbiol/data/hhsuite/databases/hhsuite_dbs/old-releases/uniprot20_2016_02.tgz
	tar -xvzf uniprot20_2016_02.tgz
	rm uniprot20_2016_02.tgz
	
	# defining a symbolic link to point to your local Uniprot20 copy.
	cd ${LRRpredictor_HOME}/RaptorX_Property_Fast/databases
	rm uniprot20
	ln -s ${UNIPROT20_PATH}/uniprot20_2016_02 uniprot20
	cd ${LRRpredictor_HOME}

	
Now the installation is complete. You can use now LRRpredictor. 

  
  
## Usage
LRRpredictor can be used with the following sintax:
	
	cd $LRRpredictor_HOME

	python3 LRRpred.py <file.fasta> <OuputDirectory>
	
An example is provided for testing the installation :

	python3 LRRpred.py gpa2.fasta results
	
The provided input file needs to be in fasta format. At the moment only single sequence files can be provided. :exclamation:

Upon running, in the output directory `results`, a folder with the protein file name has been generated `gpa2`. 
```
user@ea846151db35:/home/test/LRRpredictor_v1# ls -l results/gpa2/
total 328
drwxr-xr-x 3 root root   4096 Feb 26 17:51 RaptorX-Property		# Contains RaptorX-Property structural predictions
-rw-r--r-- 1 root root  97165 Feb 26 17:51 gpa2.input			# The data used as input for the 8 classifiers used by LRRpredictor
-rw-r--r-- 1 root root  60378 Feb 26 17:52 gpa2.pred.txt		# Long version of the prediction results
-rw-r--r-- 1 root root   1738 Feb 26 17:52 gpa2.predshort.txt		# Short version of the results
-rw-r--r-- 1 root root 165984 Feb 26 17:51 gpa2.pssm			# variability profile used (also present in input file)
```


#### ProteinName.pred.txt file
The long version of the prediction results contains:
```
#prot	resid	aa	unused	hasPred	clf1	clf2	clf3	clf4	clf5	clf6	clf7	clf8	LRRpredictor
gpa2    0       M       -       0       -       -       -       -       -       -       -       -       -
gpa2    1       A       -       0       -       -       -       -       -       -       -       -       -
gpa2    2       Y       -       0       -       -       -       -       -       -       -       -       -
gpa2    3       A       -       0       -       -       -       -       -       -       -       -       -
gpa2    4       A       -       0       -       -       -       -       -       -       -       -       -
gpa2    5       V       -       1       0.0     0.0     0.0001  0.0002  0.0     0.0     0.0     0.0001  0.0001
gpa2    6       T       -       1       0.0     0.0     0.0002  0.0     0.0     0.0     0.0     0.0     0.0
gpa2    7       S       -       1       0.0001  0.0001  0.0001  0.0004  0.0     0.0     0.0     0.0004  0.0001
gpa2    8       L       -       1       0.0001  0.0     0.0002  0.0     0.0     0.0     0.0     0.0     0.0
gpa2    9       M       -       1       0.0093  0.0007  0.0008  0.0119  0.0001  0.0     0.0     0.0012  0.003
```

Header description:
* prot &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- protein name
* resid &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- residue number
* aa &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- amino acid one letter code
* unused &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- unused field (this field is used only training and testing data and indicates the position where a true LRR motifs starts; these positions were identified from structural files).
* hasPred &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- '1' for positions for which prediction are generated, '0' for margins.
* clf1-8 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Each classifiers predicted probability (min: 0, max 1)
* LRRpred &nbsp;&nbsp;&nbsp;&nbsp;- LRRpredictor probability based on all eight classifiers.


#### ProteinName.predshort.txt file
The short version of the prediction results contains only the detected potential LRR motifs, that yielded a probability value over 0.5.
```
#Prot   pos     clf1    clf2    clf3    clf4    clf5    clf6    clf7    clf8    LRRpred  -5   -4   -3   -2   -1      L    x   x    L    x    L     +6   +7   +8   +9   +10
gpa2    498     0.7261  0.5799  0.8533  0.513   0.602   0.0606  0.8891  0.4282  0.5815    C    S    F    K    S      R    S   R    I    S    I      H    N    E    E    E
gpa2    520     0.716   0.5073  0.9835  0.5105  0.3683  0.0358  0.5765  0.3352  0.5041    S    E    A    H    S      I    I   T    L    C    I      F    K    C    V    T
gpa2    538     0.9436  0.9636  1.0     0.7928  0.9191  0.8902  1.0     0.649   0.8948    L    S    F    K    L      V    R   V    L    D    L      G    L    T    T    C
gpa2    561     0.8005  0.9763  1.0     0.747   0.7626  0.895   1.0     0.8371  0.8773    L    S    L    I    H      L    R   Y    L    S    L      R    F    N    P    R
gpa2    599     0.928   0.976   1.0     0.8087  0.9609  0.9056  1.0     0.8324  0.9264    S    S    L    C    Y      L    Q   T    F    K    L      Y    H    P    F    P
gpa2    626     0.9298  0.9768  1.0     0.5384  0.9491  0.9053  1.0     0.8258  0.8907    L    T    M    P    Q      L    R   K    L    C    M      G    W    N    Y    L
gpa2    651     0.5822  0.3423  0.9926  0.5818  0.3902  0.0031  0.9687  0.5873  0.556     L    V    L    K    S      L    Q   C    L    N    E      L    N    P    R    Y
gpa2    654     0.7745  0.5717  1.0     0.7384  0.9009  0.5866  0.996   0.5031  0.7589    K    S    L    Q    C      L    N   E    L    N    P      R    Y    C    T    G
gpa2    676     0.8824  0.8095  1.0     0.7785  0.9525  0.8812  0.9969  0.7421  0.8804    P    N    L    K    K      L    E   V    F    G    V      K    E    D    F    R
```

Header description:
* prot 	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- protein name
* pos 	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- residue number where a detected LRR motif starts (i.e first `L` from `LxxLxL` minimalistic motif)
* clf1-8	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Each classifiers predicted probability (min: 0, max 1)
* LRRpred	&nbsp;&nbsp;&nbsp;- LRRpredictor probability based on all eight classifiers.

Starting from columns 12 until the end, the amino acid sequence of the detected LRR motif is shown: 5 positions upstream the motif (-5 to -1), the minimalistic motif LxxLxL and 5 positions downstream (6 to 10).  

#### Troubleshooting

If these files were not generated when runing the provided example, something went wrong during installation. 
Most likely reasons could be:

* Environment variables are not set. Try the following and see if you get simillar paths.
```
root@ea846151db35:/home/test/LRRpredictor_v1# echo -e $LRRpredictor_HOME '\n'$RaptorX_HOME'\n'$HHSUITE_HOME'\n'$HHSUITE_INSTALL_BASE_DIR
/home/test/LRRpredictor_v1
/home/test/LRRpredictor_v1/RaptorX_Property_Fast
/home/test/LRRpredictor_v1/hh-suite
/home/test/LRRpredictor_v1/hh-suite
```
* The folder where the project was build is not in `/home/user/...`. See if the above paths start with `/home/user/`

* Uniprot20 was not downloaded. Check the following
```
root@ea846151db35:/home/test/LRRpredictor_v1# ls -lh $RaptorX_HOME/databases/uniprot20/
total 39G
-rw------- 1 1001 1001  637 Feb 26  2016 md5sum
-rw------- 1 1001 1001 1.9G Feb 26  2016 uniprot20_2016_02.cs219
-rw------- 1 1001 1001   18 Feb 26  2016 uniprot20_2016_02.cs219.sizes
-rw------- 1 1001 1001  29G Feb 26  2016 uniprot20_2016_02_a3m.ffdata
-rw------- 1 1001 1001 190M Feb 26  2016 uniprot20_2016_02_a3m.ffindex
lrwxrwxrwx 1 1001 1001   28 Feb 26  2016 uniprot20_2016_02_a3m_db -> uniprot20_2016_02_a3m.ffdata
-rw------- 1 1001 1001 222M Feb 26  2016 uniprot20_2016_02_a3m_db.index
-rw------- 1 1001 1001 1.8G Feb 25  2016 uniprot20_2016_02_cs219.ffdata
-rw------- 1 1001 1001 181M Feb 25  2016 uniprot20_2016_02_cs219.ffindex
-rw------- 1 1001 1001 5.1G Feb 26  2016 uniprot20_2016_02_hhm.ffdata
-rw------- 1 1001 1001 2.9M Feb 26  2016 uniprot20_2016_02_hhm.ffindex
lrwxrwxrwx 1 1001 1001   28 Feb 26  2016 uniprot20_2016_02_hhm_db -> uniprot20_2016_02_hhm.ffdata
-rw------- 1 1001 1001 3.4M Feb 26  2016 uniprot20_2016_02_hhm_db.index
```

* RaptorX-Property or HH-suite encountered a problem with your sequence. Check if you have a folder named - `TMP_proteinName_*` that is generated only if something went wrong.

```
root@ea846151db35:/home/test/LRRpredictor_v1# ls -l $RaptorX_HOME/TMP_gpa2_*
total 16
-rw-rw-r-- 1 eliza eliza  891 Jan 12 23:03 gpa2.fasta_raw
-rw-rw-r-- 1 eliza eliza  891 Jan 12 23:03 gpa2.seq
-rw-rw-r-- 1 eliza eliza  285 Jan 12 23:08 gpa2.tgt_log1
-rw-rw-r-- 1 eliza eliza 6897 Jan 12 23:08 gpa2.tgt_log2
```

Additional information that could indicate the problem can be found in `gpa2.tgt_log1` and `gpa2.tgt_log2` files.



## Citing LRRpredictor

If you use LRRpredictor please cite:

[Eliza C. Martin, Octavina C. A. Sukarta, Laurentiu Spiridon, Laurentiu G. Grigore, Vlad Constantinescu, Robi Tacutu, Aska Goverse, Andrei-Jose Petrescu. LRRpredictor - a new LRR motif detection method for irregular motifs of plant NLR proteins using ensemble of classifiers. Genes 2020, 11, 286.](https://www.mdpi.com/2073-4425/11/3/286)


## References

[1] Wang, S.; Li, W.; Liu, S.; Xu, J. RaptorX-Property: a web server for protein structure property prediction. Nucleic Acids Res. 2016, 44, W430–W435.

[2] Wang, S.; Peng, J.; Ma, J.; Xu, J. Protein Secondary Structure Prediction Using Deep Convolutional Neural Fields. Sci. Rep. 2016, 6, 1–11.

[3] Wang, S.; Ma, J.; Xu, J. AUCpreD: Proteome-level protein disorder prediction by AUC-maximized deep convolutional neural fields. In Proceedings of the Bioinformatics; Oxford University Press, 2016; Vol. 32, pp. i672–i679.

[4] Wang, S.; Sun, S.; Xu, J. AUC-maximized deep convolutional neural fields for protein sequence labeling. In Proceedings of the Lecture Notes in Computer Science (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics); Springer Verlag, 2016; Vol. 9852 LNAI, pp. 1–16.
					
[5] Remmert, M.; Biegert, A.; Hauser, A.; Söding, J. HHblits: Lightning-fast iterative protein sequence searching by HMM-HMM alignment. Nat. Methods 2012, 9, 173–175.

[6] Steinegger, M., Meier, M., Mirdita, M., Vöhringer, H., Haunsberger, S. J., Söding, J. HH-suite3 for fast remote homology detection and deep protein annotation. BMC Bioinformatics 2019, 473. doi: 10.1186/s12859-019-3019-7


