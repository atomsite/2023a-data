#!/bin/bash

mkdir simulations
cd simulations
# Very long list of batch arguments
python3 ../../plotters/batchbuilder.py -s 100 -c 0.01 0.05 0.10 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 0.99 -al 0 -fe 1000
cd ..