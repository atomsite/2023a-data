# Devolatilization of extrasolar planetesimals by 60Fe and 26Al heating data archive

> Simulation data for the paper _Devolatilization of extrasolar planetesimals by 26Al and 60Fe heating_ (J W Eatson, T Lichtenberg, T V Gerya, R J Parker, 2023). 

This repository contains all of the files needed to bootstrap the results for our paper. Storage of the data from this paper is extremely large (on the order of 4TB), and as such we will instead be offering an archive containing the plotting data as well as the means to reproduce our work.

## Main segments of the archive
- `Simulations`: All of the simulations from this paper can be generated and run from this archive, a copy of the simulation code `I2Elvis` is included.
  - As there are many redundant files, a script, `bootstrap.sh` is included in the folder that will generate the initial conditions for each simulation used in each plot.
- `plot_data`: We also include the data relevant for all figures, so the plots can be replicated easily, since there is quite a bit of data this LZMA compressed, each plot has its own plotting script contained within the `plot_data` archives.
- `i2elvis.tar.xz`: A tarballed copy of the [`i2elvis`](https://github.com/FormingWorlds/i2elvis_planet) numerical simulation codebase as used in the code, see [Requirements](#requirements) for more information on the simulation. Compressed with LZMA, and can be decompressed with the `bash` command `tar -xf i2elvis.tar.xz`.

## Reasoning behind using this type of archive

Because it saves an enormous amount of data, and lets a large parameter space exploration be stored in a single repository.

- Total size of data repository: `4.6TiB`
- Size of repo before compression of plotting data files: `1.57GiB`
- Size of repo after compression of plotting data files: `104MiB`

## Processing requirements
As this is a fairly low resolution 2D simulation series, simulations can be run within a day and in parallel using a workstation of reasonable performance. It is important to note that the [Intel compiler suite](https://www.intel.com/content/www/us/en/developer/tools/oneapi/dpc-compiler.html) (ICC/ICPC) is required with this current iteration, which rules out ARM and AMD x86-64 machines.

The workstation that did the bulk of the processing is as follows:
- Intel W-1290P CPU, 10 cores, 20 threads @ 3.70GHz
- 128GB DDR4 memory
- RTX A2000 (not needed)
- 1TB of NVMe storage & 8TB of spinning disk storage

The main problem of simulation in this case is that hundreds of simulations were performed, which took approximately 6 weeks of total compute time.

## Data columns
The `hydrous_silicates.t3c` file is user-readable as a CSV, the following is the parameters in each column

- Column 1:  `time`, **simulation time (years)**
- Column 2:  `sol_frac`, fraction of solid silicates
- Column 3:  `liq_frac`, fraction of liquid silicates
- Column 4:  `hydrous_frac`, fraction of silicates in the hydrous phase
- Column 5:  `primitive_frac`, fraction of silicates in primitive phase
- Column 6:  `n2co2_frac`, remaining fraction of N2/CO2 
- Column 7:  `cocl_frac`, remaining fraction of COCl
- Column 8:  `h2o_frac`, **remaining fraction of H2O (Hf in paper)**
- Column 9:  `phyllo1_frac`, user defined fraction
- Column 10: `phyllo2_frac`, user defined fraction
- Column 11: `phyllo3_frac`, user defined fraction
- Column 12: `phyllo4_frac`, user defined fraction
- Column 13: `perco_frac`, fraction of remaining perchlorates 
- Column 14: `melt1_frac`, user defined melt fraction
- Column 15: `melt2_frac`, user defined melt fraction
- Column 16: `maxtk`, maximum simulation temperature (K)
- Column 17: `t_max_body`, maximum planetesimal body temperature (K)
- Column 18: `meantk`, mean simulation temperature (K)
- Column 19: `t_mean_body`, mean planetesimal body temperature (K)
- Column 20: `count_toohot`, count of cells considered too hot

Data in the simulation checkpoint files with the extension `.prn` store the following data, the module `plot2d.py` can currently access the following data:

- `rho`: Density (kg m^-3)
- `temp`: Temperature (K)
- `kt`: Thermal conductivity (W m^-1 K^-1)
- `press`: Pressure (Pa)
- `radius`: Radius from simulation center (m)
- `heat`: Radiogenic heating rate (w kg^-1)

Additional data is stored in the checkpoint files such as velocity, stress tensors and viscosity, but editing the module code would be required to access these.