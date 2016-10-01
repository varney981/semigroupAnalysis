from numpy import matrix as premat;

class IntMatrix(object):
    
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
        start_time1 = time.time()
        modulo = self.modulo;
        dimension = self.dimension;
        numEntries = pow(dimension, 2);
        matArg = (premat(self.matrix) + premat(other.matrix)) % modulo;
        start_time2 = time.time()
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
