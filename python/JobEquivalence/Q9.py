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
        result.trace = numpy.trace(resultMatrix);
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

    def __add__(self,other):
        modulo = self.modulo;
        dimension = self.dimension;
        numEntries = pow(dimension, 2);
        matArg = (premat(self.matrix) + premat(other.matrix)) % modulo;
        newMat = mat.generateMatrixFromMatrix(matArg);

        return newMat;

    def __mul__(self,other):
        modulo = self.modulo;
        dimension = self.dimension;
        numEntries = pow(dimension, 2);
        try:
            matArg = (premat(self.matrix) * premat(other.matrix)) % modulo;
        except AttributeError:
            matArg = (premat(self.matrix) * other) % modulo;
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

# function: determine all matrices in a passed list that 2nd-commute with the given matrix
def comm_2(p):
    global groupTable;
    # generate matrices for powers of p
    p_mat_powers = list();
    for n in range(mat.dimension):
        p_power = groupTable.power(p, n);
        p_mat_powers.append(mat.generateMatrixFromNumber(p_power));

    # generate comm^2 of p
    result = set();
    for coeffs in product(range(mat.modulo),repeat=mat.dimension):
        app_matrix = mat();
        for i in range(mat.dimension):
            app_matrix = app_matrix + p_mat_powers[i] * coeffs[i];
        result.add(app_matrix.number);

    return result;

# function: determine all comm^2 sets for all matrices
def all_comm_2():
    global groupTable;
    result = list()
    for i in range(groupTable.order):
        result.append(comm_2(i));
    return result;

# function: deprecated method
def _comm_2(p):
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


# function: determine if two matrices are L-equivalent
def isLEquivalent(b, c):
    global groupTable;
    if b == c:
        return True;

    Sb = set();
    Sb.add(b);
    Sc = set();
    Sc.add(c);

    Sb.update(groupTable.cTable[:, b]);
    Sc.update(groupTable.cTable[:, c]);


    return b in Sc and c in Sb;


# function: populate a list with all trace values for matrices
def generate_trace_values(order):
    result = list()
    for i in range(order):
        M = mat.generateMatrixFromNumber(i)
        result.append(numpy.trace(M.matrix))
    return result


# function: print results in desired format
def print_results(a ,b, filename):
    print "a = "
    print (mat.generateMatrixFromNumber(a)).matrix
    print "b = "
    print (mat.generateMatrixFromNumber(b)).matrix
    print
        
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
print time.time() - now;

#generate new file for results
resultFile = open(filename, 'w');
resultFile.close();

#generate all 2nd commutant sets for all matrices
comm_2_sets = all_comm_2();

#generate all trace values for each matrix
trace_list = generate_trace_values(order);

#begin testing selected matrices
fh = open('Q9Results.txt', 'w');
for (a , b) in product(range(order), repeat=2):
    if not trace_list[a] == trace_list[b]:
        continue

    rs_found = False
    for (r, s) in product(range(order), repeat=2):
        rs = groupTable.multiply([r,s])
        sr = groupTable.multiply([s,r])
        if(a == rs and b == sr):
            rs_found = True
            break

    if(not rs_found):
        print_results(a, b, filename)

fh.write('\nDone');
fh.close()
