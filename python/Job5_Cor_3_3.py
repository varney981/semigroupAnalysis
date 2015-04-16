#!/usr/bin/python

import sys;
import CayleyTable;

# Get file name and order from input
filename = sys.argv[1];
order = ord(sys.argv[2]) - ord('0');

# Load all Caylay tables
tbls = CayleyTable.readAllTables(filename, order);

# Run tests on each Cayley table for each permutation of the group set
groupSet = tbls[0].symbols;
#TODO: SET UP OUTPUT FILE
tableNum = 0;
count = 0;
total = 0;
for tbl in tbls:
    tableNum += 1;
    print tableNum;
    for a1 in groupSet:
        for a2 in groupSet:
            for b1 in groupSet:


