import csv

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

    #Use each element in the list and add to dictionary
    columnNum = 0;
    for left in result.symbols:
        for right in result.symbols:
            result.cTable[left + right] = tableList[columnNum];
            columnNum += 1;

    if result.isAssoc():
        return result;
    else:
        print 'Unacceptable!'
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
        self.cTable  = {};
        self.order   = order;
        self.symbols = [];
        for i in range(0, order):
            self.symbols.append(chr(ord('A') + i))

    def isAssoc(self):
        """Return true if operation is associative for this table"""
        for left in self.symbols:
            for mid in self.symbols:
                for right in self.symbols:
                    #Perform left operation first
                    left_mid  = self.simplifyTerm(left + mid);
                    lResult   = self.simplifyTerm(left_mid + right);

                    #Perform right operation first
                    mid_right = self.simplifyTerm(mid + right);
                    rResult   = self.simplifyTerm(left + mid_right);

                    #Compare each order of operations
                    if lResult != rResult:
                        print left;
                        print mid;
                        print right;
                        return 0;

        #If a non-associative case is not found assume associativity
        return 1;
                        
    def simplifyTerm(self, term):
        """Using the term, return evaluated term for the group"""
        if len(term) == 1:
            #If the term is already evaluated or else can be done in one step
            return term;
        elif len(term) == 2:
            return self.cTable[term];

        #Iteratively process term using table
        newTerm = self.cTable[term[0:2]]
        for i in range(2, len(term)):
            newTerm = self.cTable[newTerm + term[i]];

        return newTerm;

    def printTable(self, fh=None):
        """Print table in matrix form"""
        for left in self.symbols:
            columnNum = 0;
            rowChar   = [];
            for right in self.symbols:
                rowChar.append(self.simplifyTerm(left + right));
            if fh == None:
                print ' '.join(rowChar);
            else:
                fh.write(' '.join(rowChar) + '\n');

    def leftMultiplyBySet(self, y):
        """For passed term y and the group set for this table, compute the set Sy"""
        result = set();
        rightTerm = self.simplifyTerm(y);
        for leftTerm in self.symbols:
            result.add(self.simplifyTerm(leftTerm + rightTerm));
        return result;

    def rightMultiplyBySet(self, y):
        """For passed term y and the group set for this table, compute the set yS"""
        result = set();
        leftTerm = self.simplifyTerm(y);
        for rightTerm in self.symbols:
            result.add(self.simplifyTerm(leftTerm + rightTerm));
        return result;

    def leftMultiplyByPartialSet(self, right, setTerms):
        """For passed term right and the passed set, compute the set S(right)"""
        result = set();
        rightTerm = self.simplifyTerm(right);
        for leftTerm in setTerms:
            result.add(self.simplifyTerm(leftTerm + rightTerm));
        return result;
        
    def rightMultiplyByPartialSet(self, left, setTerms):
        """For passed term left and the passed set, compute the set (left)S"""
        result = set();
        leftTerm = self.simplifyTerm(left);
        for rightTerm in setTerms:
            result.add(self.simplifyTerm(leftTerm + rightTerm));
        return result;

    def findLeftMultipleInSetProduct(self, x, y):
        """Find left multiples of x = zy.
        
        For passed terms x, y and for the group set for this table, compute the
        set Sy and return each term z in S such that x = zy. If no such z is found,
        return the empty set.
        """     
        result = set();
        rightTerm = self.simplifyTerm(y);
        for leftTerm in self.symbols:
            productTerm = self.simplifyTerm(leftTerm + rightTerm);
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
        leftTerm = self.simplifyTerm(y);
        for rightTerm in self.symbols:
            productTerm = self.simplifyTerm(leftTerm + rightTerm);
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
            ax = self.simplifyTerm(a+x);
            xa = self.simplifyTerm(x+a);
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
                ba = self.simplifyTerm(b+a);
                ab = self.simplifyTerm(a+b);
                if ba != ab:
                    isCommutant = 0;
                    break;
            if isCommutant:
                result.add(b);
        return result;

    def transposeTable(self):
        """Transpose the multiplication table and return.

        Non-associative transpositions will not be returned and a blank list
        will be returned instead.
        """
        #tblCopy = self.copy;
        numToTranspose = 0;
        for row in range(0, self.order):
            left = chr(ord('A') + row);
            for col in range(0, numToTranspose):
                right = chr(ord('A') + col);
                swap = self.cTable[left + right];
                self.cTable[left + right] = self.cTable[right + left];
                self.cTable[right + left] = swap;
            numToTranspose = numToTranspose + 1;
        if self.isAssoc():
            return 1;
        else:
            return 0;

