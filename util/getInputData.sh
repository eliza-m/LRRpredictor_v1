
fastaFile=$1
fastaFileRoot=$2
outputFolder=$3


bash ${LRRpredictor_HOME}/RaptorX_Property_Fast/oneline_command.sh ${fastaFile} 4 1

mkdir ${outputFolder}/${fastaFileRoot}
mkdir ${outputFolder}/${fastaFileRoot}/RaptorX-Property/

mv -i ${LRRpredictor_HOME}/RaptorX_Property_Fast/tmp/${fastaFileRoot}/* ${outputFolder}/${fastaFileRoot}/RaptorX-Property/
rm -r ${LRRpredictor_HOME}/RaptorX_Property_Fast/tmp/${fastaFileRoot}


if [ -s "${outputFolder}/${fastaFileRoot}/RaptorX-Property/${fastaFileRoot}.tgt2" ]; then
	echo "RaptorX prediction is succesfull";
else echo "RaptorX prediction Failed !! Please see the log files in " ${outputFolder}/${fastaFileRoot}/RaptorX-Property/;
fi

awk 'BEGIN{ok=0;}{if($2 == "Original" && $3 =="PSP"){ l=NR; ok=1;} if(ok==1 && NR>=l+2 && length($0)>=20 ){print $0;} if(ok==1 && NR>=l+2 && length($0)<20){exit;} }' ${outputFolder}/${fastaFileRoot}/RaptorX-Property/${fastaFileRoot}.tgt2 > ${outputFolder}/${fastaFileRoot}/${fastaFileRoot}.pssm


python3 ${LRRpredictor_HOME}/util/getInputData.py ${outputFolder} ${fastaFileRoot} > ${outputFolder}/${fastaFileRoot}/${fastaFileRoot}.input




