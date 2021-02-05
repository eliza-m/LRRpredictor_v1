
echo "Building HH-suite... "

cd $HHSUITE_HOME

git checkout master
mkdir build
cd build

# For Mac !!
# CC="$(brew --prefix)/bin/gcc-10" CXX="$(brew --prefix)/bin/g++-10" cmake -DCMAKE_INSTALL_PREFIX=. ..

cmake -DCMAKE_INSTALL_PREFIX=. ..

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




echo "Building RaptorX Predict Property..."

cd ${LRRpredictor_HOME}/Predict_Property

git checkout LRRpredictor

cd source_code
make -j $MakeNoOfThreads

cd databases
rm uniprot20
ln -s ${UNIPROT20_PATH}/uniprot20_2016_02 uniprot20

echo "Building RaptorX-Property... DONE "








echo "Building TGT_Package..."

cd ${LRRpredictor_HOME}/TGT_Package/
git checkout LRRpredictor

cd ${LRRpredictor_HOME}/TGT_Package/RaptorX-SS8/
git checkout LRRpredictor

cd src
make predict

cd {LRRpredictor_HOME}/TGT_Package/source_code/
make -j $MakeNoOfThreads

cd databases
rm uniprot20
ln -s ${UNIPROT20_PATH}/uniprot20_2016_02 uniprot20



echo "Building TGT_Package... DONE "






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






