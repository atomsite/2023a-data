#!/bin/python3

import sys
import matplotlib.pyplot as plt
sys.path.append("../plotters")
from i2_plot import Simulation,init_plot,plot
import numpy as np
# from plot2d import Image

fig = init_plot(width=5,height=2.5)
folders = np.arange(201,652,50)
# Plot 2 
x = []
y = []

fig,ax = plt.subplots(1,1,figsize=(5,2.5))

for ff in folders:
  folder = str(ff)
  sim = Simulation(folder)
  ax.plot(sim.time,sim.data["h2o_frac"],label="${}^2$".format(int(folder)-1),alpha=0.5)

ax.legend(prop={'size': 6})
ax.set_ylim((1e-2,1.1e0))
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim((1e-2,1e0))
ax.set_xlabel(r"Time, $t$ (Myr)")
ax.set_ylabel("Retained water fraction, $\\mathcal{H}$")
ax.grid(True,which="both",linestyle=":")


plt.tight_layout()
plt.savefig("res-1.pdf",dpi=600,bbox_inches="tight")

fig,ax = plt.subplots(1,1,figsize=(5,2.5))

for ff in folders:
  folder = str(ff)
  sim = Simulation(folder)
  x.append(float(folder)**2 / 1e4)
  y.append(sim.data["h2o_frac"].min())

ax.plot(x,y,"x-")
ax.set_ylim((1e-2,1.1e0))
ax.set_xlim((0,45))
ax.set_yscale("log")
ax.set_xlabel("Simulation size, $N_\\textrm{cells}$ ($10^4$ cells)")
ax.set_ylabel("Final water fraction, $\\mathcal{H}_f$")
ax.grid(True,which="both",linestyle=":")

plt.tight_layout()
plt.savefig("res-2.pdf",dpi=600,bbox_inches="tight")