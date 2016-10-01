#!/bin/bash

doTesting () {
    j=$(($1 + 20))
    python JobLR/D3_JobLR.py ../tables/order7.csv 7 $1 $j
    echo $1 > JobLR/tester.txt
}
    

for ((i = $1; i < 836021; i = i + 20));
do
    doTesting "$i"
done
