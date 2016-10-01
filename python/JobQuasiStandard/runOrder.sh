#!/bin/bash

for ((i = $1; i < 836021; i = i + 20))
do
    j=$(($i + 1))
    python JobStandard/StandardB.py ../tables/order7.csv 7 $i $j >> JobStandard/StandardBResults.txt
    echo $i > JobStandard/counter.txt
done
