mkdir simulations
cd simulations
# Very long list of batch arguments
python3 ../../batchbuilder.py -s 1 3 10 30 100 -c 0.5 -al 0 -fe  1 10 100 1000 10000
cd ..
