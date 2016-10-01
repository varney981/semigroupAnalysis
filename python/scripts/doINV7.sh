#!/bin/bash

filename="../tables/order7.csv"
output="Job_Inv_Results_Order7.txt"

for ((i=$1; i < 836020; i=$((i+20))));
do
  python JobInvertibility/JobInvertibility.py $filename 7 $i $((i+20))
  echo $i
done

echo "Job done"
