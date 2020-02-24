import sys


outputFolder = sys.argv[1]
fastaFileRoot = sys.argv[2]



ss3file = open( outputFolder + "/" + fastaFileRoot + "/RaptorX-Property/" + fastaFileRoot + ".ss3", "r")

accfile = open(outputFolder + "/" + fastaFileRoot + "/RaptorX-Property/" + fastaFileRoot + ".acc", "r")

disofile = open(outputFolder + "/" + fastaFileRoot + "/RaptorX-Property/" + fastaFileRoot + ".diso", "r")

pssmfile = open(outputFolder + "/" + fastaFileRoot + "/" + fastaFileRoot + ".pssm", "r")




ss3 = [ [], [], [] ]
seq = []

lines = ss3file.readlines()
for x in range(2, len(lines)):
    l = lines[x].split()
    seq.append( l[1] )
    ss3[0].append( float(l[3]) )
    ss3[1].append( float(l[4]) )
    ss3[2].append( float(l[5]) )

size = len(seq)
acc = [ [], [], [] ]

lines = accfile.readlines()
for x in range(3, len(lines)):
    l = lines[x].split()
    acc[0].append( float(l[3]) )
    acc[1].append( float(l[4]) )
    acc[2].append( float(l[5]) )


diso = []

lines = disofile.readlines()
for x in range(3, len(lines)):
    l = lines[x].split()
    diso.append( float(l[3]) )

pssm = []

lines = pssmfile.readlines()
for x in range(0, len(lines)):
    l = lines[x].split()
    temp = []
    for y in range(20):
        temp.append( int(l[y+2]) )
    pssm.append( temp )


try:
    for x in range(size):
        print(fastaFileRoot, x, seq[x], '-', sep='\t', end='\t')
        print(ss3[0][x], ss3[1][x], ss3[2][x], sep='\t', end='\t')
        print(acc[0][x], acc[1][x], acc[2][x], sep='\t', end='\t')
        print(diso[x], sep='\t', end='\t')
        for y in range(20):
            print(pssm[x][y], sep='\t', end='\t')
        print(end='\n')
except Exception as e:
    print(e)
