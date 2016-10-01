#!/usr/bin/python

import sys;
import random;
import numpy;
sys.path.insert(0, "CayleyTable/");
import CayleyTable_Matrices as CayleyTable;
sys.path.insert(0, "ResultPrinter/");
from ResultPrinter import ResultPrinter;
from itertools import product;
from numpy import matrix as premat;
import argparse
import time


"""START OF FUNCTIONS"""
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

def get_invertible_terms(tbl):
    result = set()
    unitTerm = tbl.unitElement()
    for p in range(tbl.order):
        if unitTerm in set(tbl.cTable[p,:]) and unitTerm in set(tbl.cTable[:,p]):
            result.add(p)
    return result

def are_bLc_related(b,S,c):
    order = S.order
    bUSb = set()
    bUSb.add(b)
    cUSc = set()
    cUSc.add(c)
    for l in range(order):
        bUSb.add(S.multiply([l,b]))
        cUSc.add(S.multiply([l,c]))
    return bUSb == cUSc

def get_L_class(b, S):
    order = S.order
    L_class = set()
    for c in range(order):
        if are_bLc_related(b,S,c):
            L_class.add(c)
    return L_class

#REIMPLEMENT WHEN are_bRc_related(b,S,c) IMPLEMENTED
def get_R_class(a, S):
    return None

def comm_1(a,S):
    comm_1_a = set()
    order = S.order
    for s in range(order):
        s_a = tbl.multiply([s,a])
        a_s = tbl.multiply([a,s])
        if s_a == a_s:
            comm_1_a.add(s)
    return comm_1_a


def comm_2(a, S):
    comm_1_a = set()
    comm_2_a = set()
    order = S.order
    for s in range(order):
        s_a = tbl.multiply([s,a])
        a_s = tbl.multiply([a,s])
        if s_a == a_s:
            comm_1_a.add(s)

    for c in range(order):
        non_comm = False
        for s in comm_1_a:
            s_c = tbl.multiply([s,c])
            c_s = tbl.multiply([c,s])
            if s_c != c_s:
                non_comm = True
                break
        if not non_comm:
            comm_2_a.add(c)

    return comm_2_a


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

# function: generate table for testing all matrices
def genCayleyTable(modulo, dimension):
    order = pow(modulo, pow(dimension, 2));
    result = CayleyTable.CayleyTable(order);
    for left in range(0, order):
        leftMatrix  = mat.generateMatrixFromNumber(left);
        for right in range(0, order):
            rightMatrix = mat.generateMatrixFromNumber(right);
            indexMatrix = leftMatrix * rightMatrix;
            result.cTable[left, right] = indexMatrix.number;
    return result;

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


    #if not result.isAssoc():
    #    raise NameError('Cayley Table is not associative!');
    return result;


def find_null_space(A):
    A_mat = A.matrix
    x_dim = [A.dimension, 1]
    result = []
    x_range = (mat.modulo)**(mat.dimension)
    for x_num in range(x_range):
        x = numpy.zeros(x_dim, dtype=int)
        for i in range(mat.dimension - 1, -1, -1):
            if x_num >= mat.modulo**i:
                while x_num >= mat.modulo**i:
                    x[i][0] += 1
                    x_num -= mat.modulo**i
        comp_mat = (A.matrix.dot(x)) % 2 == numpy.zeros(x_dim,dtype=int)
        #print A.matrix
        #print x
        #print (A.matrix.dot(x)) % 2
        #print comp_mat
        if all(comp_mat):
            result.append(x)
    return result


def equal_array_lists(list1, list2):
    if len(list1) != len(list2):
        return False
    for l1 in list1:
        l1_found = False
        for l2 in list2:
            if all(l1 == l2):
                l1_found = True
        if not l1_found:
            return False
    return True

def find_absent_array(list1, list2):
    print list1
    print list2
    for l1 in list1:
        l1_found = False
        for l2 in list2:
            if all(l1 == l2):
                l1_found = True
        if not l1_found:
            return l1
    return None

"""END OF FUNCTIONS"""


"""START OF SCRIPT"""
#process arguments
parser = argparse.ArgumentParser();
parser.add_argument('--dRank', help='restrict rank of matrices in set D to this integer', type=int, default=-1);
parser.add_argument('--modulo', help='determine integer group', type=int, default=2);
parser.add_argument('--dimension', help='determine matrix dimensions (nxn)', type=int, default=3);
parser.add_argument('--aFilter', help='remove forms of a that do not cause loss of generality', action='store_true');
parser.add_argument('--output', help='filename for output');
args            = parser.parse_args();
dRank           = args.dRank;
filename        = args.output;
mat.dimension   = args.dimension;
mat.modulo      = args.modulo;
order           = pow(mat.modulo, pow(mat.dimension, 2));


#generate Cayley Table
now = time.time()
tbl = genCayleyTable(mat.modulo, mat.dimension);
print time.time() - now;

#Step 1: Find set D of all d in S s.t. det(d) = 0
D = set()
for s in range(tbl.order): 
    s_mat = mat.generateMatrixFromNumber(s)
    if(numpy.linalg.det(s_mat.matrix) == 0):
        D.add(s)

#Step 1a: Use bcRank to identify appropriate ranks
D_n = {}
for d in D:
    d_mat = mat.generateMatrixFromNumber(d)
    N_d = find_null_space(d_mat)
    samp_rank = -1
    if len(N_d) == 1:
        samp_rank = mat.dimension
    elif len(N_d) == 2:
        samp_rank = mat.dimension - 1
    elif len(N_d) == 4:
        samp_rank = mat.dimension - 2
        
    if samp_rank == dRank:
        D_n[d] = N_d

#Step 2: Find set P of (b,c)-pairs s.t. b L c is false
P = []
for (b,c) in product(D_n.keys(), repeat=2):
    if not equal_array_lists(D_n[b], D_n[c]):
        P.append((b,c))

#Step 3/4: Find set T of all (a,b,c,y) triples s.t. b in Scab and c in cabS and y = vc
#Step 5 Merge
start = 0
incr = 500

P = P[start:]
while len(P) > 0:
    now = time.time()
    print(len(P))
    T = set()
    count = 0
    if incr < len(P):
        thing = incr
    else:
        thing = len(P)

    a_set = set()
    first_set = True
    for i in range(thing):
        (b,c) = P[i]
        for a in range(tbl.order):
            new_a_set = set()
            cab = tbl.multiply([c,a,b])
            v = None
            w = None
            if (b in tbl.cTable[:,cab]):
                v = numpy.where(tbl.cTable[:,cab] == b)[0][0]
            if (c in tbl.cTable[cab,:]):
                w = numpy.where(tbl.cTable[cab,:] == c)[0][0]
            if v != None and w != None:
                y = tbl.multiply([v,c])
                T.add((a,b,c,v,w,y))
                new_a_set.add(a)
        if not first_set:
            if a_set != new_a_set:
                print 'well it is not the same a set'
        a_set = new_a_set
        first_set = False


#Step 5: The real test
    I = mat.generateMatrixFromMatrix(numpy.identity(mat.dimension,dtype=int))
    count = 0
    for (a,b,c,v,w,y) in T:
        break
        if count % 2000 == 0:
            print count
        count += 1
        ya = tbl.multiply([y,a])
        ya_mat = mat.generateMatrixFromNumber(ya)

        ay = tbl.multiply([a,y])
        ay_mat = mat.generateMatrixFromNumber(ay)

        ba = tbl.multiply([b,a])
        ba_mat = mat.generateMatrixFromNumber(ba)

        ab = tbl.multiply([a,b])
        ab_mat = mat.generateMatrixFromNumber(ab)

        baba = tbl.multiply([ba,ba])
        baba_mat = mat.generateMatrixFromNumber(baba)

        abab = tbl.multiply([ab,ab])
        abab_mat = mat.generateMatrixFromNumber(abab)

        for (p,q,r,s,t,u) in product(range(2), repeat=6):
            ya_test = (I*p + ba_mat*q + baba_mat*r).number
            ay_test = (I*s + ab_mat*t + abab_mat*u).number
            if (ya == ya_test) and (ay == ay_test):
                output = ""
                output += "a    = \n{0}\n".format((mat.generateMatrixFromNumber(a)).matrix)
                output += "b    = \n{0}\n".format((mat.generateMatrixFromNumber(b)).matrix)
                output += "c    = \n{0}\n".format((mat.generateMatrixFromNumber(c)).matrix)
                output += "v    = \n{0}\n".format((mat.generateMatrixFromNumber(v)).matrix)
                output += "w    = \n{0}\n".format((mat.generateMatrixFromNumber(w)).matrix)
                output += "y    = \n{0}\n".format((mat.generateMatrixFromNumber(y)).matrix)
                output += "ba   = \n{0}\n".format((mat.generateMatrixFromNumber(ba)).matrix)
                output += "baba = \n{0}\n".format((mat.generateMatrixFromNumber(baba)).matrix)
                output += "ab   = \n{0}\n".format((mat.generateMatrixFromNumber(ab)).matrix)
                output += "abab = \n{0}\n".format((mat.generateMatrixFromNumber(abab)).matrix)
                output += "bx = 0, but cx =/= 0 for \nx=\n" + str(find_absent_array(D_n[b],D_n[c])) + "\n"
                output += "p = {0}, q = {1}, r = {2},\ns = {3}, t = {4}, u = {5}\n\n".format(p,q,r,s,t,u)
                print output


    P = P[incr:]
    #print time.time() - now;

print 'done'
            
    
"""END OF SCRIPT"""
