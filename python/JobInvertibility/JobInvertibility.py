#!/usr/bin/python

import sys;
import random;
import numpy;
sys.path.insert(0, "CayleyTable/");
import CayleyTable_Matrices as CayleyTable;
sys.path.insert(0, "ResultPrinter/");
from ResultPrinter import ResultPrinter;
from itertools import product;


"""START OF FUNCTIONS"""

def b_in_Scab(a, b, c, groupTable):
    cab  = groupTable.multiply([c,a,b]);
    Scab = set((groupTable.cTable[:, cab]).tolist());
    
    return b in Scab;


def c_in_cabS(a, b, c, groupTable):
    cab  = groupTable.multiply([c,a,b]);
    cabS = set((groupTable.cTable[cab, :]).tolist());
    
    return c in cabS;


def write_results(tableNum, tbl, a, b, b_inv, c, cab, v, w, bw, vc):

    result = "";
    result = result + str(tableNum) + ': \n';
    result = result + str(tbl.cTable) + '\n';
    #result = result + ('a = {0}, b = {1}, c = {2} , h = {3}, y = {4}' +
    #                    ', ya = {5}, ay = {6}, hy = {7}, yh = {8}').format(a, b,
    #                    c, h, y, ya, ay, hy, yh);
    return result;


def is_invertible(element, groupTable, unitElement):
    left_unity = set()
    for left in range(0, groupTable.order):
        if groupTable.multiply([left, element])  == unitElement: 
            left_unity.add(left);
    for right in left_unity:
        if groupTable.multiply([element, right]) == unitElement:
            return True;

    return False;


def find_inverse(element, groupTable, unitElement):
    left_unity = set()
    for left in range(0, groupTable.order):
        if groupTable.multiply([left, element])  == unitElement: 
            left_unity.add(left);
    for right in left_unity:
        if groupTable.multiply([element, right]) == unitElement:
            return right;

    return -1;

"""END OF FUNCTIONS"""


"""START OF SCRIPT"""
# Get file name and order from input
filename = sys.argv[1];
order = ord(sys.argv[2]) - ord('0');

# If a range was passed, read tables for this range
if len(sys.argv) >= 5:
    tableNum  = int(sys.argv[3]);
    lastTable = int(sys.argv[4]);
    tbls = CayleyTable.readRangeOfTables(filename,order,
                                         tableNum, lastTable);
else:  #Load all tables
    tableNum = 0;
    tbls = CayleyTable.readAllTables(filename, order);

fh = open('Job_Inv_Results_Order' + str(order) + '.txt', 'a')
for tbl in tbls:
    # Increment the table counter
    tableNum += 1;

    # Search for a unit element
    if not tbl.hasUnitElement():
        continue;
    unitElement = tbl.unitElement();

    # Identify all invertible b
    b_list = list();
    for b in range(0, order):
        if is_invertible(b, tbl, unitElement):
            b_list.append(b);

    for b in b_list:
        print tbl.cTable;
        b_inv = find_inverse(b, tbl, unitElement);
        print str(b) + " * " + str(b_inv) + " = " + str(unitElement);
        print
        for (a, c) in product(range(0, order), repeat=2):
                c_invertible = is_invertible(c, tbl, unitElement);
                if not (b_in_Scab(a, b, c, tbl) and c_in_cabS(a, b, c, tbl) and not c_invertible):
                    continue;

                cab = tbl.multiply([c,a,b]);
                vbIndex = numpy.where(groupTable.cTable[:, cab] == b);
                v = vbIndex[0][0];
                wcIndex = numpy.where(groupTable.cTable[cab, :] == c);
                w = wcIndex[0][0];
                bw = tbl.multiply([b,w])
                vc = tbl.multiply([v,c])
                result_str = write_results(tableNum, tbl, a, b, b_inv, c, cab, v, w, bw, vc);
                fh.write(result_str + '\n\n');
                fh.close();
                sys.exit(-1);
      
"""END OF SCRIPT"""
