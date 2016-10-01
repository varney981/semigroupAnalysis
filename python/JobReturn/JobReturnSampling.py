import sys;
sys.path.insert(0, "CayleyTable/");
from CayleyTable_Matrices import CayleyTable;
from itertools import product;
import random;
from numpy import matrix as premat;
import numpy;
from itertools import product;
import argparse
import time


# matrix class restricting comparison and multiplication
class mat(object):
    
    # static matrix definitions to be set at start up
    dimension = 3;
    modulo    = 2;

    # static method: create format strings and set dimensions
    @staticmethod
    def setupMatrixClass(newDimension, newModulo):
        dimension = newDimension;
        modulo = newModulo;

    # static method: generate a matrix number based on matrix
    @staticmethod
    def generateMatrixNumber(M):
        dimension = mat.dimension;
        modulo    = mat.modulo;
        
        result = 0;
        elementNumber = 0;
        for i in range(0, dimension):
            for j in range(0, dimension):
                result += pow(modulo, elementNumber) * M[i,j];
                elementNumber += 1;

        return result;

    # static method: generate a matrix using a matrix number
    @staticmethod
    def generateMatrixFromNumber(n):
        dimension = mat.dimension;
        modulo = mat.modulo

        resultMatrix = numpy.zeros((mat.dimension,mat.dimension), dtype=numpy.int);
        result = mat();
        elementNumber = pow(dimension, 2) - 1;
        for i in reversed(range(dimension)):
            for j in reversed(range(dimension)):
                digitNumber = pow(modulo, elementNumber);
                entryValue  = 0;
                while n >= digitNumber:
                    entryValue += 1;
                    n -= digitNumber;
                resultMatrix[i, j] = entryValue;
                elementNumber -= 1;

        result.matrix = resultMatrix;
        result.number = n;
        return result;

    @staticmethod
    def generateMatrixFromMatrix(M):
        result = mat();
        result.matrix = M;
        result.number = mat.generateMatrixNumber(M);
        return result;
      

    def __init__(self):
        self.matrix = numpy.zeros((mat.dimension,mat.dimension), dtype=numpy.int);
        self.number = 0;

    def __eq__(self, other):
        return self.number == other.number;

    def __mul__(self,other):
        modulo = self.modulo;
        dimension = self.dimension;
        numEntries = pow(dimension, 2);
        matArg = (premat(self.matrix) * premat(other.matrix)) % modulo;
        newMat = mat.generateMatrixFromMatrix(matArg);

        return newMat;

# function: generate matrix strings using a specified integer modulo group and square matrix dimension
def genMatStrings(modulo, dimension, index=-1):
    result = list();
    numEntries = pow(dimension, 2);
    numStrings = pow(modulo, numEntries);
    if not index == -1:
        lower = index;
        upper = index + 1;
    else:
        lower = 0;
        upper = numStrings;
    for i in range(lower, upper):
        temp = i;
        modList = [0] * numEntries;
        newString = '';
        powerNumbers = range(0, pow(dimension, 2));
        powerNumbers.reverse();
        for j in powerNumbers:
            placeNumber = pow(modulo, j);
            while temp - placeNumber >= 0:
                modList[j] += 1;
                temp -= placeNumber;

        # generate matrix string
        for j in range(0, numEntries):
            newString = newString + str(modList[j]);
            if j % dimension == dimension - 1 and j < numEntries - 1: 
                newString = newString + ';';
            elif j < numEntries - 1:
                newString = newString + ',';
            else:
                pass;
        result.append(newString)

    if index == -1:
        return result;
    else:
        return result[0];

# function: generate table for testing all matrices
def genCayleyTable(modulo, dimension):
    order = pow(modulo, pow(dimension, 2));
    result = CayleyTable(order);
    for left in range(0, order):
        leftMatrix  = mat.generateMatrixFromNumber(left);
        for right in range(0, order):
            rightMatrix = mat.generateMatrixFromNumber(right);
            indexMatrix = leftMatrix * rightMatrix;
            result.cTable[left, right] = indexMatrix.number;

    #if not result.isAssoc():
    #    raise NameError('Cayley Table is not associative!');
    return result;


# function: determine all matrices in a passed list that commute with the given matrix (use string form)
def comm_1(p, matList=None, termEarly=False):
    global groupTable;
    if matList == None:
        matList = range(0, groupTable.order);

    result = list();
    for q in matList:
        pq = groupTable.cTable[p, q];
        qp = groupTable.cTable[q, p];
        if pq == qp:
            result.append(q);
        elif termEarly:
            return list();

    return result;

# function: determine all matrices in a passed list that 2nd-commute with the given matrix (use string form)
def comm_2(p):
    global groupTable;
    global start_time
    result = list();
    comm_1_list  = comm_1(p);
    if not comm_1_list:
        return;

    for r in range(0, groupTable.order):
        comm_2_list = comm_1(r, comm_1_list, termEarly=True);
        if set(comm_2_list) == set(comm_1_list):
            result.append(r);
    return result;


# function: print results in desired format
def printResults(a ,b ,c ,v ,y, filename):
    print 'gross'

        
#process arguments
parser = argparse.ArgumentParser();
parser.add_argument('--bcRank', help='restrict rank of matrices b and c to this integer', type=int, default=-1);
parser.add_argument('--modulo', help='determine integer group', type=int, default=2);
parser.add_argument('--dimension', help='determine matrix dimensions (nxn)', type=int, default=3);
parser.add_argument('--aFilter', help='remove forms of a that do not cause loss of generality', action='store_true');
parser.add_argument('--output', help='filename for output');
args            = parser.parse_args();
filename        = args.output;
mat.dimension   = args.dimension;
mat.modulo      = args.modulo;
order           = pow(mat.modulo, pow(mat.dimension, 2));


#generate Cayley Table
now = time.time()
groupTable = genCayleyTable(mat.modulo, mat.dimension);
#print time.time() - now;

#generate unit matrix element
unitMatrix = numpy.zeros((mat.dimension, mat.dimension), dtype=numpy.int)
for i in range(0, mat.dimension):
    unitMatrix[i, i] = 1;
unitElement = mat.generateMatrixNumber(unitMatrix);

#find all non-invertible b
b_list = list();
for b in range(0, order):
    b_invertible = False;
    left_unity = set()
    for left in range(0, order):
        if groupTable.multiply([left, b])  == unitElement: 
            left_unity.add(left);
    for right in left_unity:
        if groupTable.multiply([b, right]) == unitElement:
            b_invertible = True;
            break;
    if not b_invertible:
        b_list.append(b);

#print b_list;
#print len(b_list);

#select some random matrices

#begin testing selected matrices
resultFile = open(filename, 'w');

for i in range(0, 100):
    iternum = 0
    last_b = 0;
    start_time = time.time()
    b_start_time = time.time()
    b_list = random.sample(b_list, 16);
    a_list = random.sample(range(0, order), 16);
    c_list = random.sample(range(0, order), 16);
    g_list = random.sample(range(0, order), 100);
    h_list = random.sample(range(0, order), 100);
    for b in b_list:
        if not b == last_b:
            b_remaining = len(b_list) - iternum;
            iternum += 1;
            elapsed_time = time.time() - b_start_time;
            b_start_time = time.time();
#            print 'elapsed time at ' + str(b) + ': ' + str(time.time() - start_time);
#            print 'b matrices remaining: ' + str(b_remaining);
#            print 'estimated time remaining: ' + str(b_remaining * elapsed_time);
#            print;
            last_b = b;
        for a in a_list:
            for c in c_list:
                h_set = set()
                g = -1;
                #print (b,c)
                #iternum = iternum + 1;
                #resultFile = open('diag' + str(bcRank) + '.txt', 'a');
                #resultFile.write(str(iternum) + '\n');
                #resultFile.close();
                
                cab = groupTable.multiply([c , a , b]);

                #check if b is in Scab and c is in cabS
                b_in_Scab = b in groupTable.cTable[:, cab];
                c_in_cabS = c in groupTable.cTable[cab, :];

                if not (b_in_Scab and c_in_cabS):
                    continue;

                vbIndex = numpy.where(groupTable.cTable[:, cab] == b);
                v = vbIndex[0][0];
                wcIndex = numpy.where(groupTable.cTable[cab, :] == c);
                w = wcIndex[0][0];
                y  = groupTable.multiply([v,c]);

                for g in g_list:
                    for h in h_list:
                        bhy = groupTable.multiply([b,h,y]);
                        ygc = groupTable.multiply([y,g,c]);
                        hya = groupTable.multiply([h,y,a]);
                        ayg = groupTable.multiply([a,y,g]);
                        hba = groupTable.multiply([h,b,a]);
                        aya = groupTable.multiply([a,y,a]);
                        acg = groupTable.multiply([a,c,g]);

                        if not (bhy == y and y == ygc and hya == h and ayg == g and hba == aya and aya == acg):
                            continue;

                        h_set.add(h);
                        some_g = g;


                if len(h_set) >= 2:
                    #printStr = 'a = {0}, b = {1}, c = {2}, v = {3}, y = {4}'.format(a, b, c, v, y);
                    #printStr = printStr + '\nba = {0}, ab = {1}, ya = {2}, ay = {3}\n\n'.format(ba, ab, ya, ay);
                    resultFile.write('Found something\n');

resultFile.write('\nDone');
resultFile.close()
