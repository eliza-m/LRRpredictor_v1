
fastaFile=$1
fastaFileRoot=$2
outputFolder=$3


bash ${RaptorX_HOME}/oneline_command.sh ${fastaFile} 4 1

mkdir ${outputFolder}/${fastaFileRoot}
mkdir ${outputFolder}/${fastaFileRoot}/RaptorX-Property/

mv -i ${RaptorX_HOME}/tmp/${fastaFileRoot}/* ${outputFolder}/${fastaFileRoot}/RaptorX-Property/

awk 'BEGIN{ok=0;}{if($2 == "Original" && $3 =="PSP"){ l=NR; ok=1;} if(ok==1 && NR>=l+2 && length($0)>=20 ){print $0;} if(ok==1 && NR>=l+2 && length($0)<20){exit;} }' ${outputFolder}/${fastaFileRoot}/RaptorX-Property/${fastaFileRoot}.tgt2 > ${outputFolder}/${fastaFileRoot}/${fastaFileRoot}.pssm


python3 ${LRRpredictor_HOME}/util/getInputData.py ${outputFolder} ${fastaFileRoot} > ${outputFolder}/${fastaFileRoot}/${fastaFileRoot}.input






