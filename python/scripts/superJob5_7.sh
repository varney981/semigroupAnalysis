#!/bin/bash

for ((i = $1; i < 836021; i = i + 20))
do
    j=$(($i + 20))
    python Job5/Job5_Cor_3_3.py ../tables/order7.csv 7 $i $j >> results.txt
    echo $i > tester.txt
done
