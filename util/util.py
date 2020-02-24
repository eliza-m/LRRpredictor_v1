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

feature_list_seq = "ARNDCQEGHILKMFPSTWYV"

feature_list_str = ['ssH', 'ssE', 'ssC', 'accB', 'accM', 'accE', 'diso']
for aa in feature_list_seq:
	feature_list_str.append( aa )


##########################################################################

def ReadData( File ):
# creates a dictionary from entry data *.input to be further used

    DataDict = {}

    # the distribution is not actually exactly gaussian
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
            print( test_data[it]['name'], test_data[it]['no'], test_data[it]['seq'], test_data[it]['lrr'], test_data[it]['haspred'], '-', '-', '-', '-', '-', '-', '-', '-', '-',  '-', '-', '-', '-',sep='\t', file=restestFile)





##############################################
# Pred LRR motiffs
##############################################

def PrintShortResults(test_data, testset_pred_proba, clfno, restestFile):
    header = "#Protein\tpos\tclf1\tclf2\tclf3\tclf4\tclf5\tclf6\tclf7\tclf8\tLRRpred\t"
    print(header, file=restestFile )
    countpos = 0;
    for it in range(len(test_data)):
        if test_data[it]['haspred'] == 1:
                if testset_pred_proba[clfno][countpos][1] >= 0.50 :
                    print( test_data[it]['name'], test_data[it]['no'], sep='\t', end='\t', file=restestFile )
                    for c in range( clfno + 1 ):
                        print( round( testset_pred_proba[c][countpos][1], 4), end='\t', file=restestFile )
                    for it2 in range(-1*windleft, 0):
                        print( test_data[it + it2]['seq'], end=' ', file=restestFile )
                    print(end='\t', file=restestFile)
                    for it2 in range(0, 6):
                        print( test_data[it + it2]['seq'], end=' ', file=restestFile )
                    print(end='\t', file=restestFile)
                    for it2 in range(6, windright + 1):
                        print( test_data[it + it2]['seq'], end=' ', file=restestFile )
                    print('', file=restestFile)

                countpos += 1




