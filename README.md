# 2023a-data
> Simulation data for first submitted paper of 2023, _Devolatilization of extrasolar planetesimals by 26Al and 60Fe heating_.

This repository contains all of the files needed to bootstrap the results for our paper. Storage of the data from this paper is extremely large (on the order of 4TB), and as such we will instead be offering a 

## Main segments of the archive
- `Simulations`: All of the simulations from this paper can be generated and run
  - As there are many redundant files, a script, `bootstrap.sh` is included in the folder that will copy all of the files into the specific 
- `plot_data`: We also include the data relevant for all figures, so the plots can be replicated easily, since there is quite a bit of data this LZMA compressed.
- `i2elvis.tar.xz`: a tarballed copy of the [`i2elvis`](https://github.com/FormingWorlds/i2elvis_planet) numerical simulation codebase as used in the code, see [Requirements](#requirements) for more information on simulation. Compressed with LZMA, can be decompressed with the command `tar -xf i2elvis.tar.xz`

## Processing requirements
As this is a fairly low resolution 2D simulations series, simulations can be run within a day and in parallel using a workstation of reasonable performance. It is important to note that the [Intel compiler suite](https://www.intel.com/content/www/us/en/developer/tools/oneapi/dpc-compiler.html) (ICC/ICPC) is required with this current iteration, which rules out ARM and AMD x86-64 machines.

The workstation that did the bulk of the processing is as follows:
- Intel W-1290P CPU, 10 cores, 20 threads @ 3.70GHz
- 128GB DDR4 memory
- RTX A2000 (not needed)
- 1TB of NVMe storage & 8TB of spinning disk storage

The main problem of simulation in this case is that hundreds of simulations were performed, which took approximately 6 weeks of total compute time.