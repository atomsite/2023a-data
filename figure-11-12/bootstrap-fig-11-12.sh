mkdir simulations
cd simulations

for gr in 0.00 0.01 0.02 0.04 0.08 0.16 0.18 0.25 0.50 0.75 0.90
do
  mkdir psi$gr
  cd psi$gr
  python3 ../../../plotters/batchbuilder.py -s 100 -c 0 -al 0 1 1.78 3.16 5.62 10 -fe 0 1 10 100 1000 1000 10000 -g $gr
  cd ..
cd ..