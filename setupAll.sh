

cd $HHSUITE_HOME

git checkout LRRpredictor

mkdir build
cd build

cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX=${HHSUITE_INSTALL_BASE_DIR} ..
make -j $MakeNoOfThreads
make install


cd ${RaptorX_HOME}/source_code
make -j $MakeNoOfThreads

cd ../
./setup.pl

cd databases
rm uniprot20
ln -s ${UNIPROT20_PATH}/uniprot20_2016_02 uniprot20


cd $LRRpredictor_HOME






