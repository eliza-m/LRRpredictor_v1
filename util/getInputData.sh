
fastaFile=$1
fastaFileRoot=$2
outputFolder=$3


mkdir -p ${outputFolder}/${fastaFileRoot}
mkdir -p ${outputFolder}/${fastaFileRoot}/RaptorX-Property
outputpred=${outputFolder}/${fastaFileRoot}/RaptorX-Property


bash ${LRRpredictor_HOME}/TGT_Package/A3M_TGT_Gen.sh -i $fastaFile -o ${outputpred} -d uniprot20_2016_02 -h hhsuite3
bash ${LRRpredictor_HOME}/Predict_Property/Predict_Property.sh -i ${outputpred}/${fastaFileRoot}.tgt -o ${outputpred} 


awk 'BEGIN{ok=0;}{if($2 == "Original" && $3 =="PSP"){ l=NR; ok=1;} if(ok==1 && NR>=l+2 && length($0)>=20 ){print $0;} if(ok==1 && NR>=l+2 && length($0)<20){exit;} }' ${outputpred}/${fastaFileRoot}.tgt2 > ${outputFolder}/${fastaFileRoot}/${fastaFileRoot}.pssm


python3 ${LRRpredictor_HOME}/util/getInputData.py ${outputFolder} ${fastaFileRoot} > ${outputFolder}/${fastaFileRoot}/${fastaFileRoot}.input



