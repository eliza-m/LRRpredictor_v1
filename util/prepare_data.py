import sys
import numpy as np




# creates a dictionary from entry data *.all to be further used
def ReadData( File ):
    DataDict = {}

    # the distribution is not actually gaussian
    # we don't want to loose the meaning of value 0 - no correlation
    pssm_rescale_factor = 10;

    lines = File.readlines()
    for i in range(len(lines)):
         l = lines[i].split()

         if l[0] not in DataDict:
             DataDict[l[0]]  = {
                                'seq':[],
                                'no':[],
                                'lrr':[],

                                'ssH':[],
                                'ssE':[],
                                'ssC':[],

                                'accB':[],
                                'accM':[],
                                'accE':[],

                                'diso':[],

                                'A':[],
                                'R':[],
                                'N':[],
                                'D':[],
                                'C':[],
                                'Q':[],
                                'E':[],
                                'G':[],
                                'H':[],
                                'I':[],
                                'L':[],
                                'K':[],
                                'M':[],
                                'F':[],
                                'P':[],
                                'S':[],
                                'T':[],
                                'W':[],
                                'Y':[],
                                'V':[]
                                }

         DataDict[l[0]]['seq'].append(l[2])
         DataDict[l[0]]['no'].append(int(l[1]))
         DataDict[l[0]]['lrr'].append(l[3])

         #  These are probabilieties -> scaling from [0, 1] to [-1, 1] range
         DataDict[l[0]]['ssH'].append( ( float(l[4]) * 2 ) -1 )
         DataDict[l[0]]['ssE'].append( ( float(l[5]) * 2 ) -1 )
         DataDict[l[0]]['ssC'].append( ( float(l[6]) * 2 ) -1 )

         DataDict[l[0]]['accB'].append( ( float(l[7]) * 2 ) -1 )
         DataDict[l[0]]['accM'].append( ( float(l[8]) * 2 ) -1 )
         DataDict[l[0]]['accE'].append( ( float(l[9]) * 2 ) -1 )

         DataDict[l[0]]['diso'].append( ( float(l[10]) * 2 ) -1 )


         DataDict[l[0]]['A'].append( float( l[11] )  / pssm_rescale_factor  )
         DataDict[l[0]]['R'].append( float( l[12] )  / pssm_rescale_factor  )
         DataDict[l[0]]['N'].append( float( l[13] )  / pssm_rescale_factor  )
         DataDict[l[0]]['D'].append( float( l[14] )  / pssm_rescale_factor  )
         DataDict[l[0]]['C'].append( float( l[15] )  / pssm_rescale_factor  )
         DataDict[l[0]]['Q'].append( float( l[16] )  / pssm_rescale_factor  )
         DataDict[l[0]]['E'].append( float( l[17] )  / pssm_rescale_factor  )
         DataDict[l[0]]['G'].append( float( l[18] )  / pssm_rescale_factor  )
         DataDict[l[0]]['H'].append( float( l[19] )  / pssm_rescale_factor  )
         DataDict[l[0]]['I'].append( float( l[20] )  / pssm_rescale_factor  )
         DataDict[l[0]]['L'].append( float( l[21] )  / pssm_rescale_factor  )
         DataDict[l[0]]['K'].append( float( l[22] )  / pssm_rescale_factor  )
         DataDict[l[0]]['M'].append( float( l[23] )  / pssm_rescale_factor  )
         DataDict[l[0]]['F'].append( float( l[24] )  / pssm_rescale_factor  )
         DataDict[l[0]]['P'].append( float( l[25] )  / pssm_rescale_factor  )
         DataDict[l[0]]['S'].append( float( l[26] )  / pssm_rescale_factor  )
         DataDict[l[0]]['T'].append( float( l[27] )  / pssm_rescale_factor  )
         DataDict[l[0]]['W'].append( float( l[28] )  / pssm_rescale_factor  )
         DataDict[l[0]]['Y'].append( float( l[29] )  / pssm_rescale_factor  )
         DataDict[l[0]]['V'].append( float( l[30] )  / pssm_rescale_factor  )

    return DataDict



# returns an array with Features, Observation, Data
def PrepareData( DataDict, feature_list, windleft, windright ):

    data = []
    hasLRR = {}
    set_obs = []
    set_features = []


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

                entry = []

                for wint in range( windleft*(-1), windright + 1 ):
                   for feat in range( len(feature_list) ):
                       entry.append( DataDict[ prot ][ feature_list[feat] ][ it + wint ] )

                set_features.append(entry)


    return set_features, set_obs, data



# returns an array with Features, Observation, Data
def PrepareData_2feat( DataDict, feature_list_seq, feature_list_seqstr, windleft, windright ):

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


def PrintDetailedPred(test_data, testset_pred_proba, restestFile):

    # PRINT HEADER
    # print("#", names, file=restestFile)
    # print( "# Window size from -", windleft, "to", windright, file=restestFile)
    # print( "# No. features :", len(testset_features[0]), file=restestFile)
    # print( "# Features :", feature_list[:], file=restestFile)
    # print("\n\n", file=restestFile)

    countpos = 0;
    for it in range(len(test_data)):
        if test_data[it]['haspred'] == 1:
            print( test_data[it]['name'], test_data[it]['no'], test_data[it]['seq'], test_data[it]['lrr'], test_data[it]['haspred'], round( testset_pred_proba[countpos][1], 4), sep='\t', file=restestFile)
            countpos += 1
        else:
            print( test_data[it]['name'], test_data[it]['no'], test_data[it]['seq'], test_data[it]['lrr'], test_data[it]['haspred'], '-', sep='\t', file=restestFile)




# def PrintProbaHistoStats( header, testset_obs, testset_pred, testset_pred_proba, statslearnFile ):
#
#     # print( "#", names, file=statslearnFile)
#     # print( "# Window size from -", windleft, "to", windright, file=statslearnFile)
#     # print( "# Features :", feature_list[:], file=statslearnFile)
#     # print( "\n\n", file=statslearnFile)
#
#
#     count_test = [ [0, 0], [0, 0] ]
#     countall_test = [0, 0]
#     distr_test = [ [0 for x in range(101)], [0 for x in range(101)] ]
#
#     for it in range(len(testset_obs)):
#         distr_test[ testset_obs[it] ][ int(testset_pred_proba[it][1]*100) ] += 1
#         count_test[ testset_obs[it] ][ testset_pred[it] ] += 1
#         countall_test[ testset_obs[it] ] += 1
#
#     print(header, sep='\t',  end='\t', file=statslearnFile)
#     print(count_test[0][0], count_test[0][1], count_test[1][0], count_test[1][1], sep='\t',  end='\t', file=statslearnFile);
#
#     precision = round( count_test[1][1] / (count_test[1][1] + count_test[1][0] ) , 4)
#     recall = round( count_test[1][1] / (count_test[1][1] + count_test[0][1] ) , 4)
#     fscore = (2 * precision * recall) / (precision + recall)
#     print(precision, recall, fscore, sep='\t',  end='\t', file=statslearnFile);
#
#     print("Class0", sep='\t',  end='\t', file=statslearnFile)
#     for x in range(101):
#         print( distr_test[0][x], sep='\t', end='\t', file=statslearnFile)
#
#     print("Class1", sep='\t',  end='\t', file=statslearnFile)
#     for x in range(101):
#         print( distr_test[1][x], sep='\t', end='\t', file=statslearnFile)
#
#     print(file=statslearnFile);




def PrintProbaHistoStatsShort( header, testset_obs, testset_pred, statslearnFile ):

    count_test = [ [0, 0], [0, 0] ]
    countall_test = [0, 0]

    for it in range(len(testset_obs)):
        count_test[ testset_obs[it] ][ testset_pred[it] ] += 1
        countall_test[ testset_obs[it] ] += 1

    print(header, sep='\t',  end='\t', file=statslearnFile)
    print(count_test[0][0], count_test[0][1], count_test[1][0], count_test[1][1], sep='\t',  end='\t', file=statslearnFile);

    if ( (count_test[1][1] + count_test[1][0] ) > 0 and (count_test[1][1] + count_test[0][1] ) >0 ) :
        recall = round( count_test[1][1] / (count_test[1][1] + count_test[1][0] ) , 4)
        precision = round( count_test[1][1] / (count_test[1][1] + count_test[0][1] ) , 4)
        fscore = round( (2 * precision * recall) / (precision + recall) , 4)
    else:
        precision = 0
        recall = 0
        fscore = 0

    print(precision, recall, fscore, sep='\t',  end='\t', file=statslearnFile);

    print(file=statslearnFile);





# 4 SVM - as the voter will use only the platt proba...

def PrintProbaHistoStatsShortProba( header, testset_obs, testset_pred_proba, statslearnFile ):

    count_test = [ [0, 0], [0, 0] ]
    countall_test = [0, 0]

    for it in range(len(testset_obs)):
        if testset_pred_proba[it][1] >= 0.5:
            pred = 1
        else:
            pred = 0

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

    print(precision, recall, fscore, "proba_0.5", sep='\t',  end='\t', file=statslearnFile);

    print(file=statslearnFile);



def calculate_bic(n, mse, num_params):
	bic = n * log(mse) + num_params * log(n)
	return bic

def calculate_aic(n, mse, num_params):
	aic = n * log(mse) + 2 * num_params
	return aic

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


##############################################
# for voter classifiers
##############################################


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
            print( test_data[it]['name'], test_data[it]['no'], test_data[it]['seq'], test_data[it]['lrr'], test_data[it]['haspred'], '-', '-', '-', '-', '-', '-', '-', '-', '-',  '-', '-', '-', '-',sep='\t', file=restestFile)





##############################################
# Pred LRR motiffs
##############################################

def PrintShortResults(test_data, testset_pred_proba, restestFile):
    header = "#Protein\tpos\tclf1\tclf2\tclf3\tclf4\tclf5\tclf6\tclf7\tclf8\tLRRpred\t"
    print(header, file=restestFile )
    countpos = 0;
    for it in range(len(test_data)):
        if test_data[it]['haspred'] == 1:
                if testset_pred_proba[8][countpos][1] >= 0.50 :
                    print( test_data[it]['name'], test_data[it]['no'], sep='\t', end='\t', file=restestFile )
                    for c in range( 9 ):
                        print( round( testset_pred_proba[c][countpos][1], 4), end='\t', file=restestFile )
                    for it2 in range(-5, 0):
                        print( test_data[it + it2]['seq'], end=' ', file=restestFile )
                    print(end='\t', file=restestFile)
                    for it2 in range(0, 6):
                        print( test_data[it + it2]['seq'], end=' ', file=restestFile )
                    print(end='\t', file=restestFile)
                    for it2 in range(6, 11):
                        print( test_data[it + it2]['seq'], end=' ', file=restestFile )
                    print('', file=restestFile)

                countpos += 1
