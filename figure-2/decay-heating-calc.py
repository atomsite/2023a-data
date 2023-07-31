import matplotlib.pyplot as plt
from numpy import exp,logspace

def decay_heating(t,m,E,tau):
  # Constants
  A     = 6.0221408e+23
  ln2   = 0.69314718056
  myr2s = 3.15576e+13
  mev2j = 1.60218e-13
  # Convert variables
  tau_sec = tau * myr2s
  t_sec   = t*myr2s
  Ej      = E * mev2j
  l       = ln2 / tau_sec
  # Calculate H0
  H   = (A/m) * Ej * l
  # Scale in accordance with decay law
  H  *= exp(-t_sec/tau_sec)
  return H

def heating_solarsystem(H,fss,Zss):
  Q = H*fss*Zss
  print(Q[0])
  return Q

# Define 
t_array = logspace(-2,2,1000)
# Calculate heating constant 
al26_q_array = decay_heating(t_array,25.9868919e-3,3.210,0.717)
fe60_q_array = decay_heating(t_array,59.93407e-3,2.712,2.600)
# Calculate solar system equivalents
al26_q_ss_array = heating_solarsystem(al26_q_array,0.0085,5.250e-5)
fe60_q_ss_array = heating_solarsystem(al26_q_array,0.1828,1.150e-8)
fe60_q_10ss_array = heating_solarsystem(al26_q_array,0.1828,1.150e-7)

# Formatting
plt.rcParams.update({"text.usetex": True,
                     "font.family": "Computer Modern"})
fig, ax = plt.subplots(1, 1, sharex=True, sharey=False,figsize=(5,3))

# Plot one, mass normalised
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Time, $t$ (Myr)")
ax.set_ylabel(r"Specific heating, $H$ (W$\,$kg$^{-1}$)")
ax.set_xlim(1e-2,1e2)
ax.set_ylim(1e-6,1)
ax.grid(True,which="both",linestyle=":")
# Plotting
ax.plot(t_array,al26_q_array,label="$^{26}$Al")
ax.plot(t_array,fe60_q_array,label="$^{60}$Fe")
ax.legend()
plt.savefig("decay_heating-1.pdf",bbox_inches="tight")

# Plot 2, solar system normalised

fig, ax = plt.subplots(1, 1, sharex=True, sharey=False,figsize=(5,3))
ax.plot(t_array,al26_q_ss_array,label="$^{26}$Al, solar abundance")
ax.plot(t_array,fe60_q_ss_array,label="$^{60}$Fe, solar abundance")
ax.plot(t_array,fe60_q_10ss_array,label="$^{60}$Fe, 10$\\times$ solar abundance")
ax.plot(t_array,al26_q_ss_array+fe60_q_ss_array,label="$Q_\\textrm{T}$",linestyle=":",c="red")
ax.legend()
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Time, $t$ (Myr)")
ax.set_ylabel(r"Body heating rate, $Q_\textrm{ss}$ (W$\,$kg$^{-1}$)")
ax.set_xlim(1e-2,1e2)
ax.set_ylim(1e-16,1e-6)
ax.grid(True,which="both",linestyle=":")
# Save figure
plt.savefig("decay_heating-2.pdf",bbox_inches="tight")