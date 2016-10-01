#!/bin/bash

for ((i = $1; i < 836021; i = i + 20))
do
    j=$(($i + 20))
    python JobLR/D3_JobLR.py ../tables/order7.csv 7 $i $j >> JobLR/success.txt
    echo $i > JobLR/tester.txt
done
