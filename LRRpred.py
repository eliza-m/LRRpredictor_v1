

import sys
import numpy as np

from sklearn import svm
from sklearn.neural_network import MLPClassifier
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTETomek
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib

sys.path.append('util/')

from prepareInputData import *
from util import *


##########################################################################
# Generate input data - RaptorX predictions and PSSMs
##########################################################################

# open fasta file
fastaFileName = sys.argv[1]
outputDir = sys.argv[2]

try:
    inputFile = getInputData( fastaFileName, outputDir )
    testproteinsDict = ReadData( inputFile )

except Exception as e:
    print("There where problems in generating the input for LRRpredictor. Please see the error messages above or within RaptorX log files located at results/protname/RaptorX-Property/ \n")
    sys.exit(1)



testset_features_seq, testset_features_str, testset_obs, testset_obs_detail, test_data = PrepareData_2feat( testproteinsDict, feature_list_seq, feature_list_str, windleft, windright  )



# Create output files
temp = fastaFileName.split("/")[-1]
fastaFileRoot = temp.split(".")[0]

try:
	restestFile = open( outputDir + "/" + fastaFileRoot + "/" + fastaFileRoot + ".pred.txt" , "w")
	restestshortFile = open( outputDir + "/" + fastaFileRoot + "/" + fastaFileRoot + ".predshort.txt" , "w")

except Exception as e:
	print(e)
	sys.exit(1)


################################
#  Predict LRR motifs
################################

testset_pred = []
testset_pred_proba = []
classifiers = []

clfnames = [
'SVC_seq_rbf_1_0.01_bal_',
'MLP_seq_lbfgs_1.0_300.150.100_none_',
'MLP_seq_lbfgs_1.0_250.150.100_SMOTETomek_',
'ada_seq_50_1_SAMME.R_none_',
'SVC_str_rbf_1_0.001_bal_',
'MLP_str_adam.es20_0.1_250.125.100_none_',
'MLP_str_lbfgs_1.0_125.100.10_SMOTETomek_',
'ada_str_50_1_SAMME.R_none_'
]

clfno = len(clfnames)

for currentClf in range( clfno ):
    print( "LRRpredictor - classifer ", currentClf + 1, "/", clfno, "..." )

    filename = os.environ["LRRpredictor_HOME"] + "/fullTraining/" + clfnames[currentClf] + 'fullTraining.pkl'
    with open(filename, "rb") as f:
        classifiers.append( joblib.load( f ) )

    if clfnames[currentClf].split('_')[1] == "seq":
        features = testset_features_seq
    else:
        features = testset_features_str

    testset_pred.append( classifiers[ currentClf ].predict(features) )
    testset_pred_proba.append( classifiers[ currentClf ].predict_proba(features) )


currentClf +=1
testset_pred.append([])
testset_pred_proba.append([])

for it in range( len( testset_pred_proba[0] ) ):
    vote = 0;
    for c in range( currentClf ):
        vote += testset_pred_proba[c][it][1]
    vote /= currentClf

    testset_pred_proba[ currentClf ].append( [ 1-vote, vote] )
    if vote >= 0.50:
        testset_pred[ currentClf ].append(1)
    else:
        testset_pred[ currentClf ].append(0)


PrintDetailedPredVoter(test_data, testset_pred_proba, restestFile )
PrintShortResults(test_data, testset_pred_proba, clfno, restestshortFile)

print( "LRRpredictor output results were written at : \n", outputDir + "/" + fastaFileRoot )
