#!/bin/bash

for ((i = $1; i < 836021; i = i + 20))
do
    j=$(($i + 20))
    python JobUniqueness/Last.py ../tables/order7.csv 7 $i $j >> JobUniqueness/Last7.txt
    echo $i > counter.txt
done
