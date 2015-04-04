import csv

'Using a properly formatted file, read each Cayley table to a list'
def readAllTables(fileName, order):
    result = [];

    #Open file and read each row to a Cayley table
    with open(fileName, 'rb') as csvfile:
        tableReader = csv.reader(csvfile)
        for tableInst in tableReader:
            result.append(readTable(tableInst, order));
    return result;

'Read a Cayley table from a list of symbols'
def readTable(tableList, order):
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

'Table object used to perform group operations'
class CayleyTable(object):
    'Initialize an empty CayleyTable'
    def __init__(self, order):
        self.cTable  = {};
        self.order   = order;
        self.symbols = [];
        for i in range(0, order):
            self.symbols.append(chr(ord('A') + i))

    'Return true if operation is associative for this table'
    def isAssoc(self):
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
                        

    'Using a term with valid symbols, return the evaluated term for the group'
    def simplifyTerm(self, term):
        #If the term is already evaluated or else can be done in one step'
        if len(term) == 1:
            return term;
        elif len(term) == 2:
            return self.cTable[term];

        #Iteratively process term using table'
        newTerm = self.cTable[term[0:2]]
        for i in range(2, len(term)):
            newTerm = self.cTable[newTerm + term[i]];

        return newTerm;

    'Print table in matrix form'
    def printTable(self):
        for left in self.symbols:
            columnNum = 0;
            rowChar   = [];
            for right in self.symbols:
                rowChar.append(self.simplifyTerm(left + right));
            print ' '.join(rowChar)



