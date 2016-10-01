from numpy import matrix as premat;
import numpy;
from itertools import product;
import argparse

class mat(object):
    def __init__(self, matString):
        self.matrix    = premat("{0} {1} {2}; {3} {4} {5}; {6} {7} {8}".format(*matString));
        self.string = matString;

    def __eq__(self, other):
        return self.string == other.string;

    def __mul__(self,other):
        matArg = (self.matrix * other.matrix) % 2
        newString = "{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(matArg[0,0], matArg[0,1], matArg[0,2], matArg[1,0], matArg[1,1], matArg[1,2], matArg[2,0], matArg[2,1], matArg[2,2]);
        return mat(newString);

#generate all matrices
print 'Generating all matrices'
matList = list();
for i in range(0,512):
    stringRep = "{0:0>9b}".format(i);
    matList.append(mat(stringRep));



'''
# function: determine all matrices in a passed list that commute with the given matrix (use string form)
def comm_1(pStr, matList):
    result = list();
    p = stringToMatrix3x3(pStr);
    for qStr in matList:
        q = stringToMatrix3x3(qStr);
        pqStr = matrixToString3x3((p*q) % 2);
        qpStr = matrixToString3x3((q*p) % 2);
        if pqStr == qpStr:
            result.append(qStr);
    return result;

# function: determine all matrices in a passed list that 2nd-commute with the given matrix (use string form)
def comm_2(pStr, matList):
    result = list();
    comm_1_list  = comm_1(pStr, matList);
    if not comm_1_list:
        return

    for rStr in matList:
        r_comm2 = False;
        comm_2_list = comm_1(rStr, comm_1_list);
        if set(comm_2_list) == set(comm_1_list):
            result.append(rStr);
    return result;

# function: determine if two matrices are L-equivalent
def isLEquivalent(bStr, cStr, matList):
    b  = stringToMatrix3x3(bStr);
    c  = stringToMatrix3x3(cStr);
    Sb = set();
    Sb.add(bStr);
    Sc = set();
    Sc.add(cStr)

    for Sstr in matList:
        Sterm = stringToMatrix3x3(Sstr);
        Sb.add(matrixToString3x3(Sterm * b));
        Sc.add(matrixToString3x3(Sterm * c));

    return Sb == Sc;

#process arguments
parser = argparse.ArgumentParser();
parser.add_argument('--bcRank', help='restrict rank of matrices b and c to this integer', type=int, default=-1);
parser.add_argument('--aFilter', help='remove forms of a that do not cause loss of generality', action='store_true');
args = parser.parse_args();

#generate all matrices
print 'Generating all matrices'
matList = list();
for i in range(0,512):
    stringRep = "{0:0>9b}".format(i);
    matList.append(stringRep);

#generate all bc matrices using the given rank (or all if rank unspecified
bcList = list();
bcRank = args.bcRank;
print 'Generating all bc matrices of rank ' + str(bcRank);
if bcRank == -1:
    for i in range(0,512):
        stringRep = "{0:0>9b}".format(i);
        bcList.append(stringRep);
else:
    for i in range(0,512):
        stringRep = "{0:0>9b}".format(i);
        matRep = stringToMatrix3x3(stringRep);
        if numpy.linalg.matrix_rank(matRep) == bcRank:
            bcList.append(stringRep);

#generate all a matrices of appropriate form
print 'generating all a matrices'
aList = list();
for i in range(0,512):
    stringRep = "{0:0>9b}".format(i);
    testString = stringRep[2] + stringRep[3] + stringRep[6] + stringRep[7];

    if testString == '0000' or not args.aFilter:
        aList.append(stringRep);

#begin testing selected matrices
print 'Begin testing'
vStr = '';
yStr = '';
for (bStr,cStr) in product(bcList, repeat=2):
    for aStr in aList:
        print 'a = ' + aStr + ' b = ' + bStr + ' c = ' + cStr;
        a = stringToMatrix3x3(aStr);
        b = stringToMatrix3x3(bStr);
        c = stringToMatrix3x3(cStr);
        cab = (((c * a) % 2) * b) % 2

        #check if b is in Scab and c is in cabS
        b_in_Scab = False;
        c_in_cabS = False;
        for Sterm in matList:
            Smat = stringToMatrix3x3(Sterm)

            Scab_term = (Smat * cab) % 2;
            cabS_term = (cab * Smat) % 2;

            ScabStr = matrixToString3x3(Scab_term);
            cabSStr = matrixToString3x3(cabS_term);

            if not b_in_Scab and ScabStr == bStr:
                b_in_Scab = True;
                vStr = Sterm;

            if not c_in_cabS and cabSStr == cStr:
                c_in_cabS = True;

            if b_in_Scab and c_in_cabS:
                v  = stringToMatrix3x3(vStr);
                y  = (v * c) % 2;
                ya = (y * a) % 2;
                ay = (a * y) % 2;
                ba = (b * a) % 2;
                ab = (a * b) % 2;
                yStr  = matrixToString3x3(y);
                yaStr = matrixToString3x3(ya);
                ayStr = matrixToString3x3(ay);
                baStr = matrixToString3x3(ba);
                abStr = matrixToString3x3(ab);
                break;

        if b_in_Scab and c_in_cabS:
                comm2_ba = comm_2(baStr, matList);
                comm2_ab = comm_2(baStr, matList);
                ya_in_comm2_ba = yaStr in comm2_ba;
                ay_in_comm2_ab = ayStr in comm2_ab;

                if ya_in_comm2_ba and ay_in_comm2_ab and not isLEquivalent(bStr, cStr, matList):
                    print 'woo';
'''
