function Job5Function(orderN)
% Load all Caylay tables and get properties
tbls = CayleyTable.tablesFromFile(['order' num2str(orderN) '.csv'], orderN);
numberOfSets = length(tbls);
count = 0;
total = 0;

% Run tests on each Caylay table for each permutation of the group set
groupSet = tbls(1).Cset;
outputFile = fopen(['JOB5_ORDER_' num2str(orderN) '.txt'], 'w');
for tableNum = 1:numberOfSets
    tableNum
    workTable = tbls(tableNum);
    for a1Num = 1:length(groupSet)
        a1 = groupSet{a1Num};
        for a2Num = 1:length(groupSet)
            a2 = groupSet{a1Num};
            for b1Num = 1:length(groupSet)
                b1 = groupSet{b1Num};
                for b2Num = 1:length(groupSet)
                    b2 = groupSet{b2Num};
                    for zNum = 1:length(groupSet)
                        z = groupSet{zNum};
                        for xNum = 1:length(groupSet)
                            x = groupSet{xNum};
                            for dNum = 1:length(groupSet)
                                d = groupSet{dNum};

                                
                                % Determine each subset needed for testing
                                b1S = zeros(orderN, 1);
                                Sb2 = zeros(orderN, 1);
                                for elemNum = 1:orderN
                                    b1S(elemNum) = workTable.simplifyTerm([b1, groupSet{elemNum}]);
                                    Sb2(elemNum) = workTable.simplifyTerm([groupSet{elemNum}, b2]);                                    
                                end
                                
                                % Check clause (1)
                                z_b1S = any(z == b1S);
                                b1a1z = workTable.simplifyTerm([b1,a1,z]);
                                clause1 = 0;
                                if ~(z_b1S && ~(b1a1z == b1))
                                    clause1 = 1;
                                end
                                
                                % Check clause (2)
                                x_Sb2 = any(x == Sb2);
                                xa2b2 = workTable.simplifyTerm([x,a2,b2]);
                                clause2 = 0;
                                if ~(x_Sb2 && ~(xa2b2 == b2))
                                    clause2 = 1;
                                end
                                
                                % Check clause (3)
                                da1 = workTable.simplifyTerm([d,a1]);
                                a2d = workTable.simplifyTerm([a2,d]);
                                db1 = workTable.simplifyTerm([d,b1]);
                                b2d = workTable.simplifyTerm([b2,d]);
                                clause3 = 0;
                                if ~(da1 == a2d && ~(db1 == b2d))
                                    clause3 = 1;
                                end
                                
                                % Check clause (4)
                                xd = workTable.simplifyTerm([x,d]);
                                dz = workTable.simplifyTerm([d,z]);
                                clause4 = 0;
                                if xd == dz
                                    clause4 = 1;
                                end
                                
                                % Check if clauses (1) - (3) are true and clause (4) is false 
                                if clause1 && clause2 && clause3 && ~clause4
                                    count = count + 1;
                                    fprintf(outputFile, 'S# %d:\r\nS:\r\n', tableNum);
                                    for rowID = groupSet
                                        fprintf(outputFile, '   ');
                                        for colID = groupSet
                                            fprintf(outputFile, '%c ', table2array(workTable.Ctable(rowID, colID)));
                                        end
                                        fprintf(outputFile, '\r\n');
                                    end
                                    fprintf(outputFile, ...
                                       ['a1  = %s\r\n' ...
                                        'a2  = %s\r\n' ...
                                        'b1 = %s\r\n' ...
                                        'b2 = %s\r\n' ...
                                        'z = %s\r\n' ...
                                        'x = %s\r\n' ...
                                        'd = %s\r\n\r\n\r\n' ...
                                        ], ...
                                        a1, ...
                                        a2, ...
                                        b1, ...
                                        b2, ...
                                        z, ...
                                        x, ...
                                        d);
                                end
                                total = total + 1;
                            end
                        end
                    end
                end
            end
        end
    end
end
count
total
fclose(outputFile);
end