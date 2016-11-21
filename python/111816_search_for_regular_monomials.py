#!/usr/bin/python

from tools import util
from tools import CayleyTable as ct
from tools import ResultPrinter as rp
from itertools import product

###START OF FUNCTIONS

###END OF FUNCTIONS


###START OF SCRIPT
#get order of tables
order = int(raw_input("What order semigroups do you want to test? >> "))

#ask to transpose tables
isTransposed = False
transpose_postfix = ''
transpose = raw_input("Do you want to transpose the tables? ([Y]/[n]) >> ")
if transpose == 'Y' or transpose == 'y':
    transpose_postfix = '_S_op'
    isTransposed = True
    
#create tables using selected mode
mode = raw_input("Which tables to test?([]All/[R]ange/[S]ingle) >> ")
if mode == 'S' or mode == 's':
    tables = util.readSingleTable(args.order, args.singleNum, isTransposed)
elif mode == 'R' or mode == 'r':
    first_table = raw_input("First table number? >> ")
    last_table = raw_input("Last table number? >> ")
    tables = util.readRangeOfTables(args.order, first_table, last_table, isTransposed)
else:
    tables = util.readAllTables(order, isTransposed)

#set special arguments here
degree = raw_input("What is desired deg(m)? >> ")
special_str = "degree" + degree
degree = int(degree)

#generate output file and (if necessary) a filename
filename = raw_input("Please enter specific file name, or leave blank for generated name >> ")
if filename == '':
    filename = "results/" + __file__[0:-3] + "_order" + str(order) + "_" + special_str
    filename += transpose_postfix
    filename += '.txt'
with open(filename, 'w') as fh:
    pass

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
    pass

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

