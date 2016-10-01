from numpy import matrix as mat;
import numpy;
from itertools import product;

#generate all matrices
matList = list();

for i in range(0,512):
    stringRep = "{0:0>9b}".format(i);
    matRep = mat("{0} {1} {2}; {3} {4} {5}; {6} {7} {8}".format(*stringRep))
    if numpy.linalg.matrix_rank(matRep) == 1:
        matList.append(stringRep);
print matList

aList = list();
for i in range(0,512):
    stringRep = "{0:0>9b}".format(i);
    testString = stringRep[2] + stringRep[3] + stringRep[6] + stringRep[7];

    if testString == '0000':
        aList.append(stringRep);

iternum = 0
for (bStr,cStr) in product(matList, repeat=2):
    for aStr in aList:
        print iternum
        iternum = iternum + 1
        Scab = set()
        cabS = set()
        a = mat("{0} {1} {2}; {3} {4} {5}; {6} {7} {8}".format(*aStr))
        b = mat("{0} {1} {2}; {3} {4} {5}; {6} {7} {8}".format(*bStr))
        c = mat("{0} {1} {2}; {3} {4} {5}; {6} {7} {8}".format(*cStr))

        cab = (c * a * b) % 2
        for Sterm in matList:
            Smat = mat("{0} {1} {2}; {3} {4} {5}; {6} {7} {8}".format(*Sterm))

            newScab = (Smat * cab) % 2;
            newcabS = (cab * Smat) % 2;

            newScabString = "{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(newScab[0,0], newScab[0,1], newScab[0,2], newScab[1,0], newScab[1,1], newScab[1,2], newScab[2,0], newScab[2,1], newScab[2,2]);
            newcabSString = "{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(newcabS[0,0], newcabS[0,1], newcabS[0,2], newcabS[1,0], newcabS[1,1], newcabS[1,2], newcabS[2,0], newcabS[2,1], newcabS[2,2]);
            
            Scab.add(newScabString);
            cabS.add(newcabSString);

        if bStr in Scab and cStr in cabS:
            print 'oh boy'
