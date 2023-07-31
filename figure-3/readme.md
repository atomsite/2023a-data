# Figure 3: Planetary composition
Data is included for this, as well as the plotting script, to run decompress the file `fig-3-data.tar.xz`[^1].
The simulations are missing the `mars_mantle` and `mars_crust` files for the sake of saving space, as such will not run in `i2mart` without first copying the files from the `i2elvis` directory first. However, even if you do this and run the simulation it will not do anything, as there is no SLR enrichment of any kind! These are purely illustrative simulations.

The plot script is useful however, as it is a good example of what you can do with the plotting libraries I have included in this repository.

[^1]: LZMA compression is used as this is about twice as efficient as `gzip`, `gzip` compression is used for data generated in these simulations as it is handled transparently with python and not processing intensive, LZMA compression takes about a minute per data file, `gzip` takes seconds.