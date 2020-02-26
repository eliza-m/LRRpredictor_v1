
echo "Building HH-suite... "

cd $HHSUITE_HOME

git checkout LRRpredictor

mkdir lib
cd lib

git clone https://github.com/eliza-m/ffindex_soedinglab.git ffindex
cd ffindex
git checkout 360e417

cd ../../
mkdir build
cd build

cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX=${HHSUITE_INSTALL_BASE_DIR} ..
make -j $MakeNoOfThreads

echo "Building HH-suite... DONE "

echo "Installing HH-suite..."

make install

echo "Installing HH-suite... DONE"





echo "Downloading Uniprot20..."

cd ${UNIPROT20_PATH}
	
wget http://wwwuser.gwdg.de/~compbiol/data/hhsuite/databases/hhsuite_dbs/old-releases/uniprot20_2016_02.tgz
	
tar -xvzf uniprot20_2016_02.tgz

rm uniprot20_2016_02.tgz

echo "Downloading Uniprot20... DONE"




echo "Building RaptorX-Property..."

cd ${RaptorX_HOME}
git checkout LRRpredictor

cd source_code
make -j $MakeNoOfThreads

cd ../
./setup.pl

cd databases
rm uniprot20
ln -s ${UNIPROT20_PATH}/uniprot20_2016_02 uniprot20

echo "Building RaptorX-Property... DONE "




echo "Downloading LRRpredictor training data..."

cd $LRRpredictor_HOME/fullTraining/

wget old.biochim.ro/ib/departments/strbiochem/LRRpred/fullTraining_pkls.tar.gz
tar -xzf fullTraining_pkls.tar.gz
mv fullTraining_pkls/* ./
rm fullTraining_pkls.tar.gz
rmdir fullTraining_pkls



if [ "$isFullDownloadSet" == "TRUE" ];
then
	cd $LRRpredictor_HOME/crossValidation/
	wget old.biochim.ro/ib/departments/strbiochem/LRRpred/CrossValidation_pkls.tar.gz
	tar -xzf CrossValidation_pkls.tar.gz
	mv CrossValidation_pkls/* ./
	rm CrossValidation_pkls.tar.gz
	rmdir CrossValidation_pkls

	cd $LRRpredictor_HOME/test/
	wget old.biochim.ro/ib/departments/strbiochem/LRRpred/test_pkls.tar.gz
	tar -xzf test_pkls.tar.gz
	mv test_pkls/* ./
	rm test_pkls.tar.gz
	rmdir test_pkls

fi



echo "Downloading LRRpredictor training data... DONE"

cd $LRRpredictor_HOME
mkdir results






