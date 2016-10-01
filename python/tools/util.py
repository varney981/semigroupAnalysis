import csv
import CayleyTable
import argparse
from itertools import product as preProduct

def readAllTables(order):
    """Using a properly formatted file, read each Cayley table to a list"""
    result = [];

    #Open file and read each row to a Cayley table
    filename = "../tables/order" + str(order) + ".csv"
    with open(fileName, 'rb') as csvfile:
        tableReader = csv.reader(csvfile)
        for tableInst in tableReader:
            result.append(readTable(tableInst, order));
    return result;

def readRangeOfTables(order, first, last):
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

def readSingleTable(

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
        raise Exception('Table found to be non-associative.')

#TODO: DEVELOP SOLUTION FOR TRANSPOSING A LIST OF TABLES RESPONSIBLY
#def transposeAllTables(tableList): 
    """Transpose each table in this list and return only associative tables.

    Non-associative transpositions will not be returned and a blank list (?)
    will be returned instead.
    """ 


def isAssociative(tbl):
    """Return true if operation is associative for this table"""
    iterNum = 0
    for left in range(0, tbl.order):
        iterNum += 1;
        for mid in range(0, tbl.order):
            for right in range(0, tbl.order):
                #Perform left operation first
                left_mid  = tbl.multiply([left, mid]);
                lResult   = tbl.multiply([left_mid, right]);

                #Perform right operation first
                mid_right = tbl.multiply([mid, right]);
                rResult   = tbl.multiply([left,  mid_right]);

                #Compare each order of operations
                if lResult != rResult:
                    return 0;

    #If a non-associative case is not found, associativity proven
    return 1;

def printTable(table, fh=None):
    """Print table in matrix form"""
    for left in range(table.order):
        columnNum = 0;
        rowChar   = [];
        for right in range(table.order):
            rowChar.append(self.multiply([left , right]));
        if fh == None:
            print (' '.join(rowChar))
        else:
            fh.write(' '.join(rowChar) + '\n');

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

def parseArgs():
    parser = argparse.ArgumentParser();
    parser.add_argument('--dRank', help='restrict rank of matrices in set D to this integer', type=int, default=-1);
    parser.add_argument('--modulo', help='determine integer group', type=int, default=2);
    parser.add_argument('--dimension', help='determine matrix dimensions (nxn)', type=int, default=3);
    parser.add_argument('--aFilter', help='remove forms of a that do not cause loss of generality', action='store_true');
    parser.add_argument('--output', help='filename for output');
    parser.add_argument('--first', help='index of first table to use', type=int);
    parser.add_argument('--last', help='index of last table to use', type=int);
    parser.add_argument('--singleNum', help='index of table for analysis', type=int);
    parser.add_argument('--mode', help='number of tables to be tested', default="all");
    return parser.parse_args();

def product(iterable, n):
    return preProduct(iterable, repeat=n)


