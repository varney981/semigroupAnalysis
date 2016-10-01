#!/bin/bash

for ((i = $1; i < 836021; i = i + 20))
do
    j=$(($i + 20))
    python JobStrong/Strong.py ../tables/order7.csv 7 $i $j 
    echo $i #> tester.txt
done
