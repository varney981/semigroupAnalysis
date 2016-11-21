import csv
from CayleyTable import CayleyTable
import argparse
from itertools import product as preProduct
import IntMatrix
import random


def readAllTables(order, isTransposed):
    """Using a properly formatted file, read each Cayley table to a list"""
    result = [];

    #Open file and read each row to a Cayley table
    fileName = "../tables/order" + str(order) + ".csv"
    with open(fileName, 'rb') as csvfile:
        tableReader = csv.reader(csvfile)
        for tableInst in tableReader:
            result.append(readTable(tableInst, order, isTransposed));
    return result;

def readRangeOfTables(order, first, last, isTransposed):
    """Using a properly formatted file, read each Cayley table to a list
    
    Defined range must use 0-based indexing. 
    The first table is included, and the last is excluded.
    """
    result = [];

    #Open file and read each row to a Cayley table
    fileName = "../tables/order" + str(order) + ".csv"
    with open(fileName, 'rb') as csvfile:
        tableNum = 0;
        tableReader = csv.reader(csvfile)
        for tableInst in tableReader:
            if first <= tableNum and tableNum < last:
                result.append(readTable(tableInst, order, isTransposed));
            tableNum += 1;
    return result;

def readSingleTable(order, index, isTransposed):
    result = [];

    #Open file and read each row to a Cayley table
    fileName = "../tables/order" + str(order) + ".csv"
    with open(fileName, 'rb') as csvfile:
        tableNum = 0;
        tableReader = csv.reader(csvfile)
        for tableInst in tableReader:
            if index == tableNum:
                result.append(readTable(tableInst, order, isTransposed));
            tableNum += 1;
    return result;

def readTable(tableList, order, isTransposed):
    """Read a Cayley table from a list of symbols"""
    result = CayleyTable(order);

    #Use each element in the list
    listElem = 0;
    for left in range(0, order):
        for right in range(0, order):
            result.cTable[left,right] = ord(tableList[listElem]) - ord('A');
            listElem += 1;

    if isTransposed:
        result.cTable = result.cTable.transpose()
    if isAssociative(result):
        return result;
    else:
        raise Exception('Table found to be non-associative.')

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

def find_absent_array(list1, list2):
    print(list1)
    print(list2)
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
    parser.add_argument('--output', help='filename for output', default=None);
    parser.add_argument('--first', help='index of first table to use', type=int);
    parser.add_argument('--last', help='index of last table to use', type=int);
    parser.add_argument('--singleNum', help='index of table for analysis', type=int);
    parser.add_argument('--mode', help='number of tables to be tested', default="all");
    parser.add_argument('--transpose', help='number of tables to be tested', action='store_true');
    parser.add_argument('--order', help='number of tables to be tested', type=int);
    parser.add_argument('--special', help='tag used as defined by job', type=str, default='');
    return parser.parse_args();

def product(iterable, n):
    return preProduct(iterable, repeat=n)

def orderProduct(table, n):
    return preProduct(range(table.order), repeat=n)

def findMatrixGroup(table, sizeLimit=2, moduloLimit=2, sizeStart=2, moduloStart=2):
    order = table.order
    for size in range(sizeStart, sizeLimit+1):
        IntMatrix.IntMatrix.dimension = size
        for modulo in range(moduloStart, moduloLimit+1):
            print "Size: {0}, Modulo: {1}".format(size,modulo)
            IntMatrix.IntMatrix.modulo = modulo
            matrixMegaGroup = IntMatrix.genCayleyTable(modulo, size)
            mgOrder = modulo**(size**2)
            count = 0
            for testGroup in preProduct(range(mgOrder), repeat=order):
                count += 1
                if count % 10000 == 0:
                    print "{0:13.9f}%".format((float(count)/mgOrder**order)*100)
                if random.random() < 0.9999:
                    continue
                failedGroup = False
                for (left, right) in preProduct(range(order), repeat=2):
                    product = table.multiply([left,right])
                    testProduct = matrixMegaGroup.multiply([testGroup[left],testGroup[right]])
                    try:
                        if testGroup.index(testProduct) != product:
                            failedGroup = True
                            break
                    except ValueError:
                        failedGroup = True
                        break

                    if failedGroup:
                        break
                if not failedGroup:
                    return testGroup
    return None




