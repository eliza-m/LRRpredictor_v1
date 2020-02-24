import sys
import numpy as np




##########################################################################
#   Set some variables
##########################################################################
# 16 postions motif:
# XXXXX LXXLXL XXXXX
# -5    0         10

windleft = 5 ;
windright = 10 ;

# the distribution is not actually exactly gaussian
# we don't want to loose the meaning of value 0 - no correlation
pssm_rescale_factor = 10;


feature_list_seq = "ARNDCQEGHILKMFPSTWYV"

feature_list_str = ['ssH', 'ssE', 'ssC', 'accB', 'accM', 'accE', 'diso']
for aa in feature_list_seq:
	feature_list_str.append( aa )

categories = [ 'seq', 'no', 'lrr' ] + feature_list_str


##########################################################################

def ReadData( File ):
# creates a dictionary from entry data *.input to be further used

    DataDict = {}

    lines = File.readlines()
    for i in range(len(lines)):
         l = lines[i].split()

         if l[0] not in DataDict:
             DataDict[l[0]]  = { feat : [] for feat in categories }

         DataDict[l[0]]['seq'].append(l[2])
         DataDict[l[0]]['no'].append(int(l[1]))
         DataDict[l[0]]['lrr'].append(l[3])

         #  These are probabilieties -> scaling from [0, 1] to [-1, 1] range
         for i in range(3, 10):
             DataDict[l[0]][ categories[i] ].append( ( float(l[ i + 1 ]) * 2 ) -1 )

		 # PSSM rescaling
         for i in range(10, 30):
             DataDict[l[0]][ categories[i] ].append( float(l[ i + 1 ]) / pssm_rescale_factor  )

    return DataDict




def PrepareData_2feat( DataDict, feature_list_seq, feature_list_seqstr, windleft, windright ):
# returns an array with Features, Observation, Data

    data = []
    hasLRR = {}
    set_obs = []
    set_obs_detail = []
    set_features_seq = []
    set_features_seqstr = []

    #  get features and observations
    for prot in DataDict:
        hasLRR[prot] = "nonLRR"
        size = len( DataDict[prot]['seq'] )

        for it in range(size):

            data.append({'name': prot,  'no': DataDict[prot]['no'][it], 'seq': DataDict[prot]['seq'][it], 'lrr': DataDict[prot]['lrr'][it], 'haspred':0 })

            if it >= windleft and it < size - windright :

                data[-1]['haspred'] = 1

                if DataDict[prot]['lrr'][it] in 'LNCP':
                    set_obs.append(1)
                    hasLRR[prot] = "LRR"
                else:
                    set_obs.append(0)

                set_obs_detail.append( [ DataDict[prot]['lrr'][it], prot ])

                entry_seq = []
                entry_seqstr = []

                for wint in range( windleft*(-1), windright + 1 ):
                   for feat in range( len(feature_list_seq) ):
                       entry_seq.append( DataDict[ prot ][ feature_list_seq[feat] ][ it + wint ] )
                   for feat in range( len(feature_list_seqstr) ):
                       entry_seqstr.append( DataDict[ prot ][ feature_list_seqstr[feat] ][ it + wint ] )

                set_features_seq.append(entry_seq)
                set_features_seqstr.append(entry_seqstr)


    return set_features_seq, set_features_seqstr, set_obs, set_obs_detail, data




def PrintDetailedPredVoter(test_data, testset_pred_proba, restestFile):

    countpos = 0;
    for it in range(len(test_data)):
        if test_data[it]['haspred'] == 1:

            print( test_data[it]['name'], test_data[it]['no'], test_data[it]['seq'], test_data[it]['lrr'], test_data[it]['haspred'], sep='\t', end='\t', file=restestFile )
            for c in range( len(testset_pred_proba) ):
                print( round( testset_pred_proba[c][countpos][1], 4), end='\t', file=restestFile )
            print('', file=restestFile)

            countpos += 1
        else:
            print( test_data[it]['name'], test_data[it]['no'], test_data[it]['seq'], test_data[it]['lrr'], test_data[it]['haspred'], '-', '-', '-', '-', '-', '-', '-', '-', '-', sep='\t', file=restestFile)





##############################################
# Pred LRR motiffs
##############################################

def PrintShortResults(test_data, testset_pred_proba, clfno, restestFile):
    header = "#Prot\tpos\tclf1\tclf2\tclf3\tclf4\tclf5\tclf6\tclf7\tclf8\tLRRpred\t-5\t-4\t-3\t-2\t-1\t\tL\tx\tx\tL\tx\tL\t\t+6\t+7\t+8\t+9\t+10"

    print(header, file=restestFile )

    countpos = 0;

    for it in range(len(test_data)):
        if test_data[it]['haspred'] == 1:
                if testset_pred_proba[clfno][countpos][1] >= 0.50 :

                    print( test_data[it]['name'], test_data[it]['no'], sep='\t', end='\t', file=restestFile )

                    for c in range( clfno + 1 ):
                        print( round( testset_pred_proba[c][countpos][1], 4), end='\t', file=restestFile )

                    for it2 in range(-1*windleft, 0):
                        print( test_data[it + it2]['seq'], end='\t', file=restestFile )

                    print(end='\t', file=restestFile)

                    for it2 in range(0, 6):
                        print( test_data[it + it2]['seq'], end='\t', file=restestFile )

                    print(end='\t', file=restestFile)

                    for it2 in range(6, windright + 1):
                        print( test_data[it + it2]['seq'], end='\t', file=restestFile )
                    print('', file=restestFile)

                countpos += 1




def PrintProbaHistoStatsLongProba( header, testset_obs_detail, testset_obs, testset_pred_proba, statslearnFile ):

    count_test = [ [0, 0], [0, 0] ]
    countall_test = [0, 0]
    countDetail = [ [{}, {'notLRRprot':0, 'LRRprot':0}], [{'L':0, 'N':0, 'C':0, 'P':0, '-':0}, {'L':0, 'N':0, 'C':0, 'P':0, '-':0}] ]

    for it in range(len(testset_obs)):
        if testset_pred_proba[it][1] >= 0.5:
            pred = 1
            if testset_obs[it] == 1:
                countDetail[ testset_obs[it] ][ pred ][ testset_obs_detail[it][0] ] +=1
            else:
                name = testset_obs_detail[it][1]
                if '_' not in name:
                    countDetail[ testset_obs[it] ][ pred ][ 'notLRRprot' ] +=1
                else:
                    countDetail[ testset_obs[it] ][ pred ][ 'LRRprot' ] +=1

        else:
            pred = 0
            if testset_obs[it] == 1:
                countDetail[ testset_obs[it] ][ pred ][ testset_obs_detail[it][0] ] +=1

        count_test[ testset_obs[it] ][ pred ] += 1
        countall_test[ testset_obs[it] ] += 1


    print(header, sep='\t',  end='\t', file=statslearnFile)
    print(count_test[0][0], count_test[0][1], count_test[1][0], count_test[1][1], sep='\t',  end='\t', file=statslearnFile);

    if ( count_test[1][1] > 0 ) :
        recall = round( count_test[1][1] / (count_test[1][1] + count_test[1][0] ) , 4)
        precision = round( count_test[1][1] / (count_test[1][1] + count_test[0][1] ) , 4)
        fscore = round( (2 * precision * recall) / (precision + recall) , 4)
    else:
        precision = 0
        recall = 0
        fscore = 0

    print(precision, recall, fscore, sep='\t',  end='\t', file=statslearnFile);

    print(countDetail[0][1]['notLRRprot'], countDetail[0][1]['LRRprot'], sep='\t',  end='\t', file=statslearnFile);
    print(countDetail[1][0]['L'], countDetail[1][0]['N'], countDetail[1][0]['C'], countDetail[1][0]['P'], sep='\t',  end='\t', file=statslearnFile);
    print(countDetail[1][1]['L'], countDetail[1][1]['N'], countDetail[1][1]['C'], countDetail[1][1]['P'], sep='\t',  end='\t', file=statslearnFile);

    print(file=statslearnFile);
