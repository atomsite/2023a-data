from plot2d import plot_split,plot_circles,Image,Desiccation
from i2_plot import Simulation
import pandas as pd
import matplotlib.pyplot as plt
import sys
from os.path import exists
import numpy as np

# Get folder
try:
  folder = sys.argv[1]
except:
  print("Need folder name!")
  sys.exit(1)

# Check to see if postprocessor occurred
if exists(folder+"/core_temps.csv"):
  print("Postprocessor already run")
else:
  print("Need to run postprocessor first!")
  from postprocessor import desiccation_times
  desiccation_times(folder)

# Read in file
try:
  sim = Simulation(folder)
except:
  print("Issues reading in hydrous_silicates.t3c")
  sys.exit(1)

# Get number and filename
try:
  n = sys.argv[2]
  finished_imgname   = folder+"/prnfiles/dd_"+str(n)+".prn.gz" 
  unfinished_imgname = folder+"/dd_"+str(n)+".prn"
  if exists(finished_imgname):
    imgname = finished_imgname
  elif exists(unfinished_imgname):
    imgname = unfinished_imgname
  else:
    raise FileNotFoundError("File not found!")
except:
  print("Script requires you to read in a specific PRN file")
  sys.exit(1)

# Read in img file
img = Image(imgname)
t   = img.t - 1e6
print(img.t)

df_core = pd.read_csv(folder+"/core_temps.csv")
df_mant = pd.read_csv(folder+"/mantle_temps.csv")

dess = Desiccation(folder)
dess.generate_img(t)

print(np.mean(dess.vap))

import numpy as np
print(np.min(dess.vap))

fig = plt.figure(figsize=(10,7))
gs = fig.add_gridspec(3,3)
# Define axes
ax1 = fig.add_subplot(gs[0:2, 0])
ax2 = fig.add_subplot(gs[0:2, 1])
ax3 = fig.add_subplot(gs[0:2, 2])
ax4 = fig.add_subplot(gs[2, :])
# Plot images/plots
img.rho.plot(ax1)
img.temp.plot(ax2)
dess.plot(ax3)
plot_split(ax4,df_mant,0,plot_maxmin=False)
plot_split(ax4,df_core,1,plot_maxmin=False)
ax4.set_xscale("log")
plt.savefig("test.pdf")