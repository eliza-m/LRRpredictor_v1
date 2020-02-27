cd /home/test/LRRpredictor_v1/crossValidation/
wget old.biochim.ro/ib/departments/strbiochem/LRRpred/CrossValidation_pkls.tar.gz
tar -xzf CrossValidation_pkls.tar.gz
mv CrossValidation_pkls/* ./
rm CrossValidation_pkls.tar.gz
rmdir CrossValidation_pkls

cd /home/test/LRRpredictor_v1/test/
wget old.biochim.ro/ib/departments/strbiochem/LRRpred/test_pkls.tar.gz
tar -xzf test_pkls.tar.gz
mv test_pkls/* ./
rm test_pkls.tar.gz
rmdir test_pkls
