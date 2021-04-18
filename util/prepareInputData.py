import sys
import os
import subprocess


def checkFastaFile( fastaFileName ):
# Checks if the provided file is in fasta format
	#print( "Checking fasta file... ", end='')
	#fastaFile = open(fastaFileName, "r")

        # TODO: to be implemented

	#print( "OK")
	return 1



def checkEnvVar():
# check if environmental variables are reachable...
	print( "\nChecking environment variables... ", end='')
	try:
		LRRpredictor_HOME = os.environ["LRRpredictor_HOME"]
	except KeyError:
   		print("Please set the environment variables for LRRpredictor_HOME")
   		sys.exit(1)

	print( "OK")
	return 1
	# more checks needed... to be continued...




def checkUniprot20():
    # check if Uniprot20 is reachable...
        print( "Checking Uniprot20... ", end='')
        isthere = os.path.isfile( os.environ["LRRpredictor_HOME"] + "/RaptorX_Property_Fast/databases/uniprot20/uniprot20_2016_02_hhm.ffdata" );
        if not isthere:
            print("Please set the $LRRpredictor_HOME/RaptorX_Property_Fast/databases/uniprot20 symbolic link to point towards the Uniprot20 database location on your computer" )
            sys.exit(1)

        print( "OK")
        return 1

                                                                                                        
def getInputData( fastaFileName, outputDir ):
# get the pssm and RaptorX-Property prediction and generates the input file
# for LRRpredictor.

	checkEnvVar()
	checkUniprot20()

	checkFastaFile( fastaFileName )

	temp = fastaFileName.split("/")[-1]
	fastaFileRoot = temp.split(".")[0]

	print( "Runing HHsuite and RaptorX-Property : \n<<" )

	try:
		subprocess.call(["bash", os.environ["LRRpredictor_HOME"] + "/util/getInputData.sh", fastaFileName, fastaFileRoot, outputDir ])
	except Exception as e:
		print(e)
		sys.exit(1)

	try:
		inputFile = open( outputDir + "/" + fastaFileRoot + "/" + fastaFileRoot + ".input" , "r")
	except Exception as e:
		print("\n>>\nInput data was NOT generated")
		print(e)
		sys.exit(1)

	return inputFile
