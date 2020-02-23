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

sys.path.append('../')
from prepare_data import *

#####################################
#   Setup
#####################################

windleft = 5 ;
windright = 10 ;


feature_list_str = ['ssH', 'ssE', 'ssC', 'accB', 'accM', 'accE', 'diso', 'A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
feature_list_seq = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']


#####################################
# Load data
#####################################

# load learn set
learnFileName = sys.argv[1]
learnFile=open(learnFileName, "r")
learnheader= learnFileName

learnproteinsDict = ReadData( learnFile );
learnset_features_seq, learnset_features_str, learnset_obs, learnset_obs_detail, learn_data = PrepareData_2feat( learnproteinsDict, feature_list_seq, feature_list_str, windleft, windright  )


################################
#   Classifiers
################################

# Clf 1 - SVC seq

ClfHeader = "SVC_seq_rbf_1_0.01_bal_"
svm1 = svm.SVC(kernel='rbf', C=1.0, gamma=0.01, probability=True, cache_size=4000, class_weight="balanced", random_state=11)
svm1.fit(learnset_features_seq, learnset_obs)
clf = CalibratedClassifierCV(svm1, cv=5)

clf.fit(learnset_features_seq, learnset_obs)
pkl_name = ClfHeader + learnheader + ".pkl"
joblib.dump( clf, pkl_name )


# Clf 2 - MLP seq

ClfHeader = "MLP_seq_lbfgs_1.0_300.150.100_none_"
clf = MLPClassifier( hidden_layer_sizes=(300, 150, 100), solver="lbfgs", alpha=1.0, random_state=11 )

clf.fit(learnset_features_seq, learnset_obs)
pkl_name = ClfHeader + learnheader + ".pkl"
joblib.dump( clf, pkl_name )



# Clf 3 - MLP seq resampling

# n_jobs=1 in order to be more reproductible...as multithreading yields in significant differences.
sampler = SMOTETomek(random_state=11, n_jobs=1)
samplerName = "SMOTETomek"

learnset_features_resampled, learnset_obs_resampled = sampler.fit_sample(learnset_features_seq, learnset_obs)
pkl_name = learnheader + "_seq_SMOTETomek.pkl"
joblib.dump( (learnset_features_resampled, learnset_obs_resampled) , pkl_name )

ClfHeader = "MLP_seq_lbfgs_1.0_250.150.100_SMOTETomek_"
clf = MLPClassifier( hidden_layer_sizes=(250, 150, 100), solver="lbfgs", alpha=1.0, random_state=11 )

clf.fit(learnset_features_resampled, learnset_obs_resampled)
pkl_name = ClfHeader + learnheader + ".pkl"
joblib.dump( clf, pkl_name )


# Clf 4 - Adaboost

ClfHeader = "ada_seq_50_1_SAMME.R_none_"
clf = CalibratedClassifierCV( AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=1), n_estimators=50, learning_rate=1.0, algorithm='SAMME.R', random_state=11), cv=5)
clf.fit(learnset_features_seq, learnset_obs)
pkl_name = ClfHeader + learnheader + ".pkl"
joblib.dump( clf, pkl_name )







# Clf 5 - SVC str

ClfHeader = "SVC_str_rbf_1_0.001_bal_"
svm1 = svm.SVC(kernel='rbf', C=1.0, gamma=0.001, probability=True, cache_size=4000, class_weight="balanced", random_state=11)
svm1.fit(learnset_features_str, learnset_obs)
clf = CalibratedClassifierCV(svm1, cv=5)

clf.fit(learnset_features_str, learnset_obs)
pkl_name = ClfHeader + learnheader + ".pkl"
joblib.dump( clf, pkl_name )


# Clf 6 - MLP str

ClfHeader = "MLP_str_adam.es20_0.1_250.125.100_none_"
clf = MLPClassifier( hidden_layer_sizes=(250, 125, 100), solver="adam", early_stopping=True, validation_fraction=0.2, alpha=0.1, random_state=11 )

clf.fit(learnset_features_str, learnset_obs)
pkl_name = ClfHeader + learnheader + ".pkl"
joblib.dump( clf, pkl_name )



# Clf 7 - MLP str resampling

# n_jobs=1 in order to be more reproductible...as multithreading yields in significant differences.
sampler = SMOTETomek(random_state=11, n_jobs=1)
samplerName = "SMOTETomek"

learnset_features_resampled, learnset_obs_resampled = sampler.fit_sample(learnset_features_str, learnset_obs)
pkl_name = learnheader + "_str_SMOTETomek.pkl"
joblib.dump( (learnset_features_resampled, learnset_obs_resampled) , pkl_name )

ClfHeader = "MLP_str_lbfgs_1.0_125.100.10_SMOTETomek_"
clf = MLPClassifier( hidden_layer_sizes=(125, 100, 10), solver="lbfgs", alpha=1.0, random_state=11 )

clf.fit(learnset_features_resampled, learnset_obs_resampled)
pkl_name = ClfHeader + learnheader + ".pkl"
joblib.dump( clf, pkl_name )


# Clf 8 - Adaboost

ClfHeader = "ada_str_50_1_SAMME.R_none_"
clf = CalibratedClassifierCV( AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=1), n_estimators=50, learning_rate=1.0, algorithm='SAMME.R', random_state=11), cv=5)
clf.fit(learnset_features_str, learnset_obs)
pkl_name = ClfHeader + learnheader + ".pkl"
joblib.dump( clf, pkl_name )
