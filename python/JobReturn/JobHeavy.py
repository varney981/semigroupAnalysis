from numpy import matrix as mat;
from itertools import product;

#generate all matrices
matSet = set();

for i in range(0,512):
    stringRep = "{0:0>9b}".format(i);
    addMatr   = mat("{0} {1} {2}; {3} {4} {5}; {6} {7} {8}".format(*stringRep))
    matSet.add(addMatr);

aSet = set();
cont = 0;
for i in range(0,512):
    stringRep = "{0:0>9b}".format(i);
    testString = stringRep[2] + stringRep[3] + stringRep[6] + stringRep[7];

    if testString == '0000':
        addMatr   = mat("{0} {1} {2}; {3} {4} {5}; {6} {7} {8}".format(*stringRep))
        print addMatr;
        cont = cont + 1;
    matSet.add(addMatr);

print cont

iternum = 0
for (a,b,c) in product(matSet, repeat=3):
    Scab = set()
    cabS = set()

    cab = (c * a * b) % 2
    for Sterm in matSet:
        newScab = (Sterm * cab) % 2;
        newcabS = (cab * Sterm) % 2;
        
        if not newScab in Scab:
            Scab.add(newScab);

        if not newcabS in cabS:
            cabS.add(newcabS);

    if b in Scab and c in cabS:
        print 'oh boy'
