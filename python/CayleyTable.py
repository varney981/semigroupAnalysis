import csv

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

    def printTable(self):
        """Print table in matrix form"""
        for left in self.symbols:
            columnNum = 0;
            rowChar   = [];
            for right in self.symbols:
                rowChar.append(self.simplifyTerm(left + right));
            print ' '.join(rowChar)

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
        
        Finds all elements b in the group set such that if xa == ax for some a in
        the group set, then ba == ab for all a in the group set.
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
            if isCommutant:
                result.add(b);
        return result;
