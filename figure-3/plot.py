import sys
sys.path.append("../plotters")
from plot2d import Image
import matplotlib.pyplot as plt
plt.rcParams.update({
  "text.usetex": True,
  "font.family": "serif",
  "font.serif": ["Computer Modern Roman"],
})

fig,ax = plt.subplots(1, 2)
fig.set_figwidth(5)
fig.set_figheight(5)

core_name  = "fig-3-data/sim_p_100.00_c_0.50_al_0.00_fe_0.00_gr_0.00/dd_0.prn"
grain_name = "fig-3-data/sim_p_100.00_c_0.00_al_0.00_fe_0.00_gr_0.25/dd_0.prn"
core = Image(core_name)
grain = Image(grain_name)
cc = ax[0].imshow(core.rho.data,extent=core.extent,cmap="cividis")
ax[0].set_title("Core model, $\\Psi = 0.50$")
ax[0].axis("off")
gg = ax[1].imshow(grain.rho.data,extent=grain.extent,cmap="cividis")
ax[1].set_title("Grain model, $\\Phi = 0.25$")
ax[1].axis("off")
plt.savefig("morph.pdf",dpi=600,bbox_inches="tight")