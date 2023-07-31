mkdir simulations
cd simulations 

for (( n=0; n<10; n=n+1 ))
do
  echo Generating simulation with 60Fe enrichment $n times solar system levels
python3 ../../plotters/batchbuilder.py -s 100 -c 0.25 0.50 -al 0 -fe $n 
done

for (( n=10; n<=90; n=n+10 ))
do
  echo Generating simulation with 60Fe enrichment $n times solar system levels
  python3 ../../plotters/batchbuilder.py -s 100 -c 0.25 0.50 -al 0 -fe $n 
done

for (( n=100; n<=900; n=n+100 ))
do
  echo Generating simulation with 60Fe enrichment $n times solar system levels
  python3 ../../plotters/batchbuilder.py -s 100 -c 0.25 0.50 -al 0 -fe $n 
done

for (( n=1000; n<=10000; n=n+1000 ))
do
  echo Generating simulation with 60Fe enrichment $n times solar system levels
  python3 ../../plotters/batchbuilder.py -s 100 -c 0.25 0.50 -al 0 -fe $n 
done

cd ..