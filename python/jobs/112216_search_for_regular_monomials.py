#!/usr/bin/python

import sys
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
abcghy_table_list = []
tableNum = 0
for table in tables:
    for (a,b,c,g,h,y) in util.orderProduct(table, 6):
        if g == h or b == c:
            continue
        bhy = table.multiply([b,h,y])
        ygc = table.multiply([y,g,c])
        if not (bhy == y and y == ygc):
            continue
        yab = table.multiply([y,a,b])
        cay = table.multiply([c,a,y])
        if not (yab == b and c == cay):
            continue
        hya = table.multiply([h,y,a])
        ayg = table.multiply([a,y,g])
        if not (hya == h and g == ayg):
            continue
        abcghy_table_list.append({'table': tableNum,'a':a,'b':b,'c':c,'g':g,'h':h,'y':y})
    tableNum += 1

#write satisfactory a,b,g,h,y,S to file if needed
with open(filename, 'a') as fh:
    #fh.write('\n'.join(list(map(lambda x: str(x), abcghy_table_list))) + '\n')
    pass

total_monomials = 6**degree
current_monomial = 0
for monomial_char_tuple in product('abcghy', repeat=degree):
    current_monomial += 1
    print "{0} out of {1}\r".format(current_monomial, total_monomials),
    sys.stdout.flush()
    monomial_char_list = list(monomial_char_tuple)
    typeC = False
    for test_dict in abcghy_table_list:
        table = tables[test_dict['table']]
        a = test_dict['a']
        b = test_dict['b']
        c = test_dict['c']
        g = test_dict['g']
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
        results.addToResults('c',c)
        results.addToResults('g',g)
        results.addToResults('h',h)
        results.addToResults('y',y)
        results.addToResults(''.join([m_str,'S',m_str]), mSm)
        with open(filename,'a') as fh:
            fh.write('m = {0} is of Type C, as in\n'.format(m_str))
            results.printAll(fh)
        results.printAll()
        continue
        
    valid_u = []
    typeA = False
    for u_degree in [2,4,6]:
        for u_char_tuple in product('abcghy', repeat=u_degree):
            u_char_list = list(u_char_tuple)
            u_is_valid = True
            for test_dict in abcghy_table_list:
                table = tables[test_dict['table']]
                a = test_dict['a']
                b = test_dict['b']
                c = test_dict['c']
                g = test_dict['g']
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
            #if len(valid_u) > 3*(u_degree/2):
            #    break

    if len(valid_u) > 0:
        u_list_str = ', '.join(valid_u)
        m_str = ''.join(monomial_char_list)
        results = 'm = {0} is of Type A, and the possible monomials u of degree 2,4, or 6 are u = {1}\n\n'.format(m_str,u_list_str)
        with open(filename, 'a') as fh:
            fh.write(results)
    else:
        m_str = ''.join(monomial_char_list)
        results = 'm = {0} is of Type B, i.e. {0} is always in {0}S{0}, but there is no monomial u of degree 2, 4, or 6 in a,b,c,g,h,y such that {0} = {0}u{0} for all S,a,b,c,g,h,y as in (1*),(2),(3).\n\n'.format(m_str)
        with open(filename, 'a') as fh:
            fh.write(results)
        print results
        
###END OF SCRIPT

