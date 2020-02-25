echo "Downloading Uniprot20..."

cd ${UNIPROT20_PATH}
	
wget http://wwwuser.gwdg.de/~compbiol/data/hhsuite/databases/hhsuite_dbs/old-releases/uniprot20_2016_02.tgz
	
tar -xvzf uniprot20_2016_02.tgz

rm uniprot20_2016_02.tgz

echo "Downloading Uniprot20... DONE"
