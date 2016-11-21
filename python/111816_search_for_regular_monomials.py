#!/usr/bin/python

from tools import util
from tools import CayleyTable as ct
from tools import ResultPrinter as rp
from itertools import product

###START OF FUNCTIONS

###END OF FUNCTIONS


###START OF SCRIPT

#process arguments
args = util.parseArgs()

#create tables using selected mode
if args.mode == "all":
    tables = util.readAllTables(args.order, args.transpose)
elif args.mode == "range":
    tables = util.readRangeOfTables(args.order, args.first, args.last, args.transpose)
elif args.mode == "single":
    tables = util.readSingleTable(args.order, args.singleNum, args.transpose)
else:
    raise ValueError("Mode selected undefined")

#generate output file and (if necessary) a filename
if args.output == None:
    filename = "results/" + __file__[0:-3] + "_order" + str(args.order) + "_mdegree_" + args.special
else:
    filename = args.output
if args.transpose:
    filename += '_S_op'
filename += '.txt'
with open(filename, 'w') as fh:
    pass

#define the degree using the special argument
try:
    degree = int(args.special)
except ValueError:
    print("Invalid degree chosen for monomials")

#begin testing
abhy_table_list = []
tableNum = 0
for table in tables:
    for (a,b,h,y) in util.orderProduct(table, 4):
        bhy = table.multiply([b,h,y])
        yhb = table.multiply([y,h,b])
        if not (bhy == y and y == yhb):
            continue
        yab = table.multiply([y,a,b])
        bay = table.multiply([b,a,y])
        if not (yab == b and b == bay):
            continue
        hya = table.multiply([h,y,a])
        ayh = table.multiply([a,y,h])
        if not (hya == h and h == ayh):
            continue
        abhy_table_list.append({'table': tableNum,'a':a,'b':b,'h':h,'y':y})
    tableNum += 1

#write satisfactory a,b,h,y,S to file if needed
with open(filename, 'a') as fh:
    #fh.write('\n'.join(list(map(lambda x: str(x), abhy_table_list))) + '\n')

for monomial_char_tuple in product('abhy', repeat=degree):
    monomial_char_list = list(monomial_char_tuple)
    typeC = False
    for test_dict in abhy_table_list:
        table = tables[test_dict['table']]
        a = test_dict['a']
        b = test_dict['b']
        h = test_dict['h']
        y = test_dict['y']
        m = table.multiply(list(map(lambda x: test_dict[x],monomial_char_list)))
        if table.isRegular(m) == -1:
            typeC = True
            typeC_tableNum = test_dict['table']
            typeC_table = table
            break

    if typeC:
        m_str = ''.join(monomial_char_list)
        mSm = typeC_table.xSy(m,m)
        results = rp.ResultPrinter(typeC_tableNum,typeC_table)
        results.addToResults('a',a)
        results.addToResults('b',b)
        results.addToResults('h',h)
        results.addToResults('y',y)
        results.addToResults(''.join([m_str,'S',m_str]), mSm)
        with open(filename,'a') as fh:
            fh.write('m={0} is of Type C, as in\n'.format(m_str))
            results.printAll(fh)
        continue
        
    valid_u = []
    typeA = False
    for u_degree in range(1,4):
        for u_char_tuple in product('abhy', repeat=u_degree):
            u_char_list = list(u_char_tuple)
            u_is_valid = True
            for test_dict in abhy_table_list:
                table = tables[test_dict['table']]
                a = test_dict['a']
                b = test_dict['b']
                h = test_dict['h']
                y = test_dict['y']
                m = table.multiply(list(map(lambda x: test_dict[x],monomial_char_list)))
                u = table.multiply(list(map(lambda x: test_dict[x],u_char_list)))
                mum = table.multiply([m,u,m])
                if mum != m:
                    u_is_valid = False
                    break
            if u_is_valid:
                u_str = ''.join(u_char_list)
                valid_u.append(u_str)

    if len(valid_u) > 0:
        u_list_str = ', '.join(valid_u)
        m_str = ''.join(monomial_char_list)
        results = 'm = {0} is of Type A, and the possible monomials u of degree at most 3 are u = {1}\n\n'.format(m_str,u_list_str)
        with open(filename, 'a') as fh:
            fh.write(results)
    else:
        m_str = ''.join(monomial_char_list)
        results = 'm = {0} is of Type B, i.e. {0} is always in {0}S{0}, but there is no monomial u of degree 1, 2, or 3 in a,b,h,y such that {0} = {0}u{0} for all S,a,b,h,y as in (1*),(2),(3).\n\n'.format(m_str,u_list_str)
        with open(filename, 'a') as fh:
            fh.write(results)
        
###END OF SCRIPT

