#!/bin/bash
mkdir simulations
cd simulations
python3 ../../plotters/batchbuilder.py -s 50 -c 0.25 -al 0 1 1.78 3.16 5.62 10 -fe 0
cd ..