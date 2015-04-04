% convertCArraysToCayleyInput

filename = 'order4raw.txt';
outputName = 'order4.csv';

fid = fopen(filename);
material  = textscan(fid, '%s %s %d;');
elements = material{3};
fclose(fid);

for i = 124:-1:0
    elements(17*i + 1) = [];
end

outputStr = reshape(char(elements' + 'A'), [16,125])';
csvwrite(outputName, outputStr);