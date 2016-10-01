import csv
import numpy
from numpy import matrix

def readRangeOfTables(fileName, order, first, last):
    """Using a properly formatted file, read each Cayley table to a list
    
    Defined range must use 0-based indexing. 
    The first table is included, and the last is excluded.
    """
    result = [];

    #Open file and read each row to a Cayley table
    with open(fileName, 'rb') as csvfile:
        tableNum = 0;
        tableReader = csv.reader(csvfile)
        for tableInst in tableReader:
            if first <= tableNum and tableNum < last:
                result.append(readTable(tableInst, order));
            tableNum += 1;
    return result;

def readAllTables(fileName, order):
    """Using a properly formatted file, read each Cayley table to a list"""
    result = [];

    #Open file and read each row to a Cayley table
    with open(fileName, 'rb') as csvfile:
        tableReader = csv.reader(csvfile)
        for tableInst in tableReader:
            result.append(readTable(tableInst, order));
    return result;

def readTable(tableList, order):
    """Read a Cayley table from a list of symbols"""
    result = CayleyTable(order);

    #Use each element in the list
    listElem = 0;
    for left in range(0, order):
        for right in range(0, order):
            result.cTable[left,right] = ord(tableList[listElem]) - ord('A');
            listElem += 1;

    if result.isAssoc():
        return result;
    else:
        print('Unacceptable!')
        return None;

#TODO: DEVELOP SOLUTION FOR TRANSPOSING A LIST OF TABLES RESPONSIBLY
#def transposeAllTables(tableList): 
    """Transpose each table in this list and return only associative tables.

    Non-associative transpositions will not be returned and a blank list (?)
    will be returned instead.
    """ 

class CayleyTable(object):
    """Table object used to perform group operations"""
    def __init__(self, order):
        """Initialize an empty CayleyTable"""
        self.cTable  = numpy.zeros((order, order), dtype=numpy.int);
        self.order   = order;
        self.unitElementFound = False;
        self.prevUnit = None;

    def multiply(self, term):
        """Using the term, return evaluated term for the group"""
        if len(term) == 1:
            #If the term is already evaluated or else can be done in one step
            return term;
        elif len(term) == 2:
            return self.cTable[term[0], term[1]];

        #Recursively process term using table
        newTerm = self.multiply(term[0:len(term) - 1]);
        return self.cTable[newTerm][term[len(term) - 1]];

    def transposeTable(self):
        self.cTable = numpy.transpose(self.cTable)
        self.unitElementFound = False;
        self.prevUnit = None;

    def isAssoc(self):
        """Return true if operation is associative for this table"""
        iterNum = 0
        for left in range(0, self.order):
            #print iterNum
            iterNum += 1;
            for mid in range(0, self.order):
                for right in range(0, self.order):
                    #Perform left operation first
                    left_mid  = self.multiply([left, mid]);
                    lResult   = self.multiply([left_mid, right]);

                    #Perform right operation first
                    mid_right = self.multiply([mid, right]);
                    rResult   = self.multiply([left,  mid_right]);

                    #Compare each order of operations
                    if lResult != rResult:
                        return 0;

        #If a non-associative case is not found, associativity proven
        return 1;

    def hasUnitElement(self):
        """Check for a unit element"""
        leftUnities = [];
        for left in range(0, self.order):
            isLeftUnity = True;
            for right in range(0, self.order):
                if not self.multiply([left,right]) == right:
                    isLeftUnity = False;
                    break;
            if isLeftUnity:
                leftUnities.append(left);

        for right in leftUnities:
            isRightUnity = True;
            for left in range(0, self.order):
                if not self.multiply([left,right]) == left: 
                    isRightUnity = False;
                    break;
            if isRightUnity:
                return True;

        return False;

    def unitElement(self):
        """Return unit element"""
        if self.unitElementFound:
            return self.prevUnit;

        leftUnities = [];
        for left in range(0, self.order):
            isLeftUnity = True;
            for right in range(0, self.order):
                if not self.multiply([left,right]) == right:
                    isLeftUnity = False;
                    break;
            if isLeftUnity:
                leftUnities.append(left);

        for right in leftUnities:
            isRightUnity = True;
            for left in range(0, self.order):
                if not self.multiply([left,right]) == left: 
                    isRightUnity = False;
                    break;
            if isRightUnity:
                self.unitElementFound = True;
                self.prevUnit = right;
                return right;
                        
    def printTable(self, fh=None):
        """Print table in matrix form"""
        for left in self.symbols:
            columnNum = 0;
            rowChar   = [];
            for right in self.symbols:
                rowChar.append(self.multiply([left , right]));
            if fh == None:
                print (' '.join(rowChar))
            else:
                fh.write(' '.join(rowChar) + '\n');

    def leftMultiplyBySet(self, y):
        """For passed term y and the group set for this table, compute the set Sy"""
        result = set();
        rightTerm = self.multiply(y);
        for leftTerm in self.symbols:
            result.add(self.multiply([leftTerm , rightTerm]));
        return result;

    def rightMultiplyBySet(self, y):
        """For passed term y and the group set for this table, compute the set yS"""
        result = set();
        leftTerm = self.multiply([y]);
        for rightTerm in self.symbols:
            result.add(self.multiply([leftTerm , rightTerm]));
        return result;

    def leftMultiplyByPartialSet(self, right, setTerms):
        """For passed term right and the passed set, compute the set S(right)"""
        result = set();
        rightTerm = self.multiply([right]);
        for leftTerm in setTerms:
            result.add(self.multiply([leftTerm , rightTerm]));
        return result;
        
    def rightMultiplyByPartialSet(self, left, setTerms):
        """For passed term left and the passed set, compute the set (left)S"""
        result = set();
        leftTerm = self.multiply([left]);
        for rightTerm in setTerms:
            result.add(self.multiply([leftTerm , rightTerm]));
        return result;

    def findLeftMultipleInSetProduct(self, x, y):
        """Find left multiples of x = zy.
        
        For passed terms x, y and for the group set for this table, compute the
        set Sy and return each term z in S such that x = zy. If no such z is found,
        return the empty set.
        """     
        result = set();
        rightTerm = self.multiply([y]);
        for leftTerm in self.symbols:
            productTerm = self.multiply([leftTerm , rightTerm]);
            if productTerm == x:
                result.add(leftTerm)
        return result;
        
    def findRightMultipleInSetProduct(self, x, y):
        """Find the right multiples of x = yz.
        
        For passed terms x, y and for the group set for this table, compute the 
        set yS and return each term z in S such that x = yz. If no such z is
        found, return the empty set.
        """
        result = set();
        leftTerm = self.multiply([y]);
        for rightTerm in self.symbols:
            productTerm = self.multiply([leftTerm , rightTerm]);
            if productTerm == x:
                result.add(rightTerm)
        return result;

    def findFirstCommutants(self, x):
        """Find all elements a in the group set such that xa == ax.
        
        The method returns a set containing all elements in the group set that
        commute with the term passed. If none are found, the empty set is returned.
        """
        result = set();
        for a in self.symbols:
            ax = self.multiply([a,x]);
            xa = self.multiply([x,a]);
            if ax == xa:
                result.add(a);
        return result;

    def findSecondCommutants(self, x):
        """Determine second commutant elements of x.
        
        First, find the set A such that each element in A commutes with x.
        Then find the set B such that each element in B commutes with
        each element in A. Return set B.
        """
        result = set();
        firstCommSet = self.findFirstCommutants(x);
        for b in self.symbols:
            isCommutant = 1;
            for a in firstCommSet:
                ba = self.multiply([b,a]);
                ab = self.multiply([a,b]);
                if ba != ab:
                    isCommutant = 0;
                    break;
            if isCommutant:
                result.add(b);
        return result;

    def power(self, operand, n):
        if n == 0:
            return self.unitElement();
        elif n == 1:
            return operand;

        # compute power
        result = operand;
        for i in range(n-1):
            result = self.multiply([result, operand])
        return result;
