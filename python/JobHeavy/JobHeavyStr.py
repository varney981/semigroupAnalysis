from numpy import matrix as premat;
import numpy;
from itertools import product;
import argparse

# matrix class restricting comparison and multiplication
class mat(object):
    def __init__(self, matString):
        self.matrix = premat("{0} {1} {2}; {3} {4} {5}; {6} {7} {8}".format(*matString));
        self.string = matString;

    def __eq__(self, other):
        return self.string == other.string;

    def __mul__(self,other):
        matArg = (self.matrix * other.matrix) % 2
        newString = "{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(matArg[0,0], matArg[0,1], matArg[0,2], matArg[1,0], matArg[1,1], matArg[1,2], matArg[2,0], matArg[2,1], matArg[2,2]);
        return mat(newString);

# function: determine all matrices in a passed list that commute with the given matrix (use string form)
def comm_1(p, matList, termEarly=False):
    result = list();
    for q in matList:
        pq = p * q;
        qp = q * p;
        if pq == qp:
            result.append(q);
        elif termEarly:
            return list();

    return result;

# function: determine all matrices in a passed list that 2nd-commute with the given matrix (use string form)
def comm_2(p, matList):
    result = list();
    comm_1_list  = comm_1(p, matList);
    if not comm_1_list:
        return

    for r in matList:
        comm_2_list = comm_1(r, comm_1_list, termEarly=True);
        if set(comm_2_list) == set(comm_1_list):
            result.append(r);
    return result;


# function: determine if two matrices are L-equivalent
def isLEquivalent(b, c, matList):
    if b == c:
        return True;

    Sb = set();
    Sb.add(b.string);
    Sc = set();
    Sc.add(c.string);

    for Sterm in matList:
        Sb.add((Sterm * b).string);
        Sc.add((Sterm * c).string);

    return b.string in Sc and c.string in Sb;

# function: print results in desired format
def printResults(a ,b ,c ,v ,y, filename):
    f = open(filename, 'a');
    strings = list()
    strings.append('');
    strings.append('');
    strings.append('');
    strings.append('');
    strings.append('');
    strings.append('');
    strings.append('');
    strings.append('');
    strings.append('');
    strings.append('');
    strings.append('');
    strings.append('');
    strings.append('');
    strings.append('');
    strings.append('');


#######################
    firstMat = [a.matrix,b.matrix,c.matrix,v.matrix,y.matrix];
    firstMatNames = ['a', 'b', 'c', 'v', 'y'];
    for curMat in firstMat:
        strings[0] = strings[0] + '     {0} {1} {2} '.format(curMat[0,0], curMat[0,1], curMat[0,2])

    i = 0;
    for curMat in firstMat:
        strings[1] = strings[1] + ' {0} = {1} {2} {3} '.format(firstMatNames[i], curMat[1,0], curMat[1,1], curMat[1,2]);
        i += 1;

    for curMat in firstMat:
        strings[2] = strings[2] + '     {0} {1} {2} '.format(curMat[2,0], curMat[2,1], curMat[2,2])

#######################
    firstMat = [(c*a*b).matrix];
    firstMatNames = ['cab'];
    for curMat in firstMat:
        strings[4] = strings[4] + '       {0} {1} {2} '.format(curMat[0,0], curMat[0,1], curMat[0,2])

    i = 0;
    for curMat in firstMat:
        strings[5] = strings[5] + ' {0} = {1} {2} {3} '.format(firstMatNames[i], curMat[1,0], curMat[1,1], curMat[1,2]);
        i += 1;

    for curMat in firstMat:
        strings[6] = strings[6] + '       {0} {1} {2} '.format(curMat[2,0], curMat[2,1], curMat[2,2])

#######################
    firstMat = [(b*a).matrix, (b*a*b*a).matrix,(a*b).matrix, (a*b*a*b).matrix];
    firstMatNames = ['ba^1', 'ba^2', 'ab^1', 'ab^2'];
    for curMat in firstMat:
        strings[8] = strings[8] + '        {0} {1} {2} '.format(curMat[0,0], curMat[0,1], curMat[0,2])

    i = 0;
    for curMat in firstMat:
        strings[9] = strings[9] + ' {0} = {1} {2} {3} '.format(firstMatNames[i], curMat[1,0], curMat[1,1], curMat[1,2]);
        i += 1;

    for curMat in firstMat:
        strings[10] = strings[10] + '        {0} {1} {2} '.format(curMat[2,0], curMat[2,1], curMat[2,2])

#######################
    firstMat = [(y*a).matrix, (a*y).matrix];
    firstMatNames = ['ya', 'ay'];
    for curMat in firstMat:
        strings[12] = strings[12] + '      {0} {1} {2} '.format(curMat[0,0], curMat[0,1], curMat[0,2])

    i = 0;
    for curMat in firstMat:
        strings[13] = strings[13] + ' {0} = {1} {2} {3} '.format(firstMatNames[i], curMat[1,0], curMat[1,1], curMat[1,2]);
        i += 1;

    for curMat in firstMat:
        strings[14] = strings[14] + '      {0} {1} {2} '.format(curMat[2,0], curMat[2,1], curMat[2,2])


    for i in range(0,15):
        f.write(strings[i]);
        f.write('\r\n');

    f.write('\r\n');
    f.write('-------------------------\r\n');
    f.write('\r\n');

    f.close();
        


#process arguments
parser = argparse.ArgumentParser();
parser.add_argument('--bcRank', help='restrict rank of matrices b and c to this integer', type=int, default=-1);
parser.add_argument('--aFilter', help='remove forms of a that do not cause loss of generality', action='store_true');
parser.add_argument('--output', help='filename for output');
args = parser.parse_args();
filename = args.output;

#generate all matrices
matList = list();
for i in range(0,512):
    stringRep = "{0:0>9b}".format(i);
    matList.append(mat(stringRep));

#generate new file for results
resultFile = open(filename, 'w');
resultFile.close();

#generate all bc matrices using the given rank (or all if rank unspecified)
bcList = list();
bcRank = args.bcRank;
if bcRank == -1:
    for i in range(0,512):
        stringRep = "{0:0>9b}".format(i);
        bcList.append(mat(stringRep));
else:
    for i in range(0,512):
        stringRep = "{0:0>9b}".format(i);
        matRep = mat(stringRep);
        if numpy.linalg.matrix_rank(matRep.matrix) == bcRank:
            bcList.append(matRep);

#generate all a matrices of appropriate form
aList = list();
for i in range(0,512):
    stringRep = "{0:0>9b}".format(i);
    testString = stringRep[2] + stringRep[3] + stringRep[6] + stringRep[7];

    if testString == '0000' or not args.aFilter:
        aList.append(mat(stringRep));

#begin testing selected matrices
diag_f = open('diag' + str(bcRank) + '.txt', 'w');
diag_f.close();
iternum = 0
for (b , c) in product(bcList, repeat=2):
    iternum = iternum + 1;
    diag_f = open('diag' + str(bcRank) + '.txt', 'a');
    diag_f.write(str(iternum) + '\n');
    diag_f.close();
    
    #skip LEquivalent b,c matrices
    if isLEquivalent(b, c, matList):
        continue;

    for a in aList:
        cab = c * a * b;

        #check if b is in Scab and c is in cabS
        b_in_Scab = False;
        c_in_cabS = False;
        for Sterm in matList:
            Scab_term = Sterm * cab;
            cabS_term = cab * Sterm;

            if not b_in_Scab and Scab_term == b:
                b_in_Scab = True;
                v = Sterm;

            if not c_in_cabS and cabS_term == c:
                c_in_cabS = True;

            if b_in_Scab and c_in_cabS:
                y  = v * c;
                ya = y * a;
                ay = a * y;
                ba = b * a;
                ab = a * b;
                break;


        if b_in_Scab and c_in_cabS:
                comm2_ba = comm_2(ba, matList);
                comm2_ab = comm_2(ab, matList);
                ya_in_comm2_ba = ya in comm2_ba;
                ay_in_comm2_ab = ay in comm2_ab;

                if ya_in_comm2_ba and ay_in_comm2_ab:
                    printResults(a,b,c,v,y,filename);

diag_f.write('\nDone');
diag_f.close()
