import sys
import numpy as np

from sklearn import svm
from sklearn.neural_network import MLPClassifier
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTETomek
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import mean_squared_error

from sklearn.externals import joblib

sys.path.append('../util/')

from prepareInputData import *
from util import *

#####################################
# Load data
#####################################

# load test set
testFileName = sys.argv[1]
testFile=open(testFileName, "r")
testheader= testFileName

testproteinsDict = ReadData( testFile );
testset_features_seq, testset_features_str, testset_obs, testset_obs_detail, test_data = PrepareData_2feat( testproteinsDict, feature_list_seq, feature_list_str, windleft, windright  )

# output all stats
# statsFile = open(sys.argv[2], "a+")
restestFile = open(sys.argv[2], "w")



################################
#   Classifiers
################################

testset_pred = []
testset_pred_proba = []
classifiers = []

clfnames = [
'retrain_SVC_seq_rbf_1_0.01_bal_',
'retrain_MLP_seq_lbfgs_1.0_300.150.100_none_',
'retrain_MLP_seq_lbfgs_1.0_250.150.100_SMOTETomek_',
'retrain_ada_seq_50_1_SAMME.R_none_',
'retrain_SVC_str_rbf_1_0.001_bal_',
'retrain_MLP_str_adam.es20_0.1_250.125.100_none_',
'retrain_MLP_str_lbfgs_1.0_125.100.10_SMOTETomek_',
'retrain_ada_str_50_1_SAMME.R_none_'
]

clfno = len(clfnames)

for currentClf in range( clfno ):

    filename = clfnames[currentClf] + "learn_" + sys.argv[1].split('_')[1] + '.pkl'
    with open(filename, "rb") as f:
        classifiers.append( joblib.load( f ) )

    if filename.split('_')[1] == "seq":
        features = testset_features_seq
    else:
        features = testset_features_str

    testset_pred.append( classifiers[ currentClf ].predict(features) )
    testset_pred_proba.append( classifiers[ currentClf ].predict_proba(features) )


    PrintProbaHistoStatsLongProba( filename, testset_obs_detail, testset_obs, testset_pred_proba[currentClf], statsFile )


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
PrintProbaHistoStatsLongProba( "LRRpred", testset_obs_detail, testset_obs, testset_pred_proba[currentClf], statsFile )
