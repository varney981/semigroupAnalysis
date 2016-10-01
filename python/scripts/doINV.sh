#!/bin/bash

filename="../tables/order${1}.csv"
output="Job_Inv_Results_Order${1}.txt"
python JobInvertibility/JobInvertibility.py $filename $1

more $output
