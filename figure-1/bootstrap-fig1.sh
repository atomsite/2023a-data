#!/bin/bash
for (( n=201; n<=651; n=n+50 ))
do
  echo Simulation of size $n:
  python3 ../plotters/simsetup.py 50 0.25 10 1000 -xy $n -f $n
done