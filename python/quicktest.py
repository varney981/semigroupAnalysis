import CayleyTable

tableSet = CayleyTable.readAllTables('../tables/order4.csv', 4);
sampleTable = tableSet[17];

sampleTable.printTable();
for j in range(0, 128):
    i = 0
    while i < 80000:
        'ABC = ' + sampleTable.simplifyTerm('ABC');
        'CCC = ' + sampleTable.simplifyTerm('CCC');
        'CC  = ' + sampleTable.simplifyTerm('CC');
        'CAB = ' + sampleTable.simplifyTerm('CAB');
        i += 1;
    print j
