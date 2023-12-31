#!/usr/bin/env python3

"""
Set up simulation in separate folder with requisite files
Creates a new init.t3c file, traverses to directory and executes it
"""

source_file_folder = "simulation_files"
t3c_files = ["amir.t3c",
             "core_dynamo.t3c",
             "core_stuff.t3c",
             "file.t3c",
             "hydrous_silicates.t3c",
             "impact_history.t3c",
             "impact_mass.t3c",
             "impact_no.t3c",
             "mode.t3c",
             "pebble_accr.t3c",
             "pebble_history.t3c",
             "start_mass.t3c"]
compressed_files = ["mars_crust.gz","mars_mantle.gz"]

from bz2 import compress
from string import Template
from shutil import copyfile
from os import mkdir
from subprocess import Popen
import sys
import argparse
from tqdm import tqdm
from yaml import dump,add_representer

def write_yaml(work_dir,mant_ext,core_frac,al_ratio,fe_ratio,sim_time,init_time,grain_volume_frac=False,xysize=251):
  """
  Write YAML file used for configuring plotter, also provides plain-text and
  easy to parse simulation parameters for the reader
  
  Inputs:
    - work_dir:    Working directory
    - mant_ext:    Mantle extent, effective radius of planetesimal
    - core_frac:   Core/mantle radius ratio
    - al_ratio:    Ratio of al26/al27 as a factor of solar system abundance
    - fe_ratio:    Ratio of fe60/fe56 as a factor of solar system abundance
    - sim_time:    Total simulation time
    - init_time:   Initial simulation time 
  Outputs:
    - None, but writes a YAML file
  """
  def float_representer(dumper, value):
    text = '{0:.3E}'.format(value)
    return dumper.represent_scalar(u'tag:yaml.org,2002:float', text)
  add_representer(float, float_representer)
  config = {}
  # Dump raw parameters
  config["mantle_radius"] = float(mant_ext)
  config["core_fraction"] = float(core_frac)
  config["al_ss_ratio"]   = float(al_ratio)
  config["fe_ss_ratio"]   = float(fe_ratio)
  # Calculate parameters for al and fe values
  al26_ss_abun = 5.250e-5 # Al_26/Al_27 solar system ratio
  fe60_ss_abun = 1.150e-8 # Fe_60/Fe_56 solar system ratio
  config["al26_al27_ratio"] = float(al_ratio) * al26_ss_abun
  config["fe60_fe56_ratio"] = float(fe_ratio) * fe60_ss_abun
  # Calculate parameters for core values
  config["core_radius"] = core_frac * mant_ext
  # Add simulation time parameters
  config["sim_time"]  = sim_time
  config["init_time"] = init_time
  config["grain_volume_frac"] = grain_volume_frac
  # Write the file
  with open(work_dir+"/simulation.yaml","w") as yaml_file:
    dump(config,yaml_file)
  return

def gen_sim(mant_ext,core_frac,al,fe,exit_time,init_time,work_dir,xyres=251,grain_volume_frac=False):
  # Quick checks for input conditions
  if mant_ext <= 0.:
    print("!!! Zero or negative mantle size! Check inputs !!!")
    sys.exit()
  if al < 0 or fe < 0:
    print("!!! Cannot have negative abundance ratios !!!")
    sys.exit()
  if mant_ext <= core_frac:
    print("!!! Core/Mantle ratio > 1, nonsensical !!!")
    sys.exit()
  try:
    float(mant_ext)
    float(core_frac)
    float(al)
    float(fe)
    str(work_dir)
  except TypeError:
    print("!!! Input parameters generally wrong, see help with -h command !!!")
    sys.exit()
  # Begin!
  print("! Initialising environment at {}".format(work_dir))
  repo_path = sys.path[0]
  # Copy files
  print("! Copying files")
  try:
    mkdir(work_dir)
    print("! Created {}!".format(work_dir))
  except FileExistsError:
    print("! Already created {}!".format(work_dir))

  try:
    # Copy all config files from folder simulation_files
    for file in tqdm(t3c_files):
      src = "{}/{}/{}".format(repo_path,source_file_folder,file)
      dst = "{}/{}".format(work_dir,file)
      copyfile(src,dst)
    # Transfer and decompress crustal/mantle files
    for file in tqdm(compressed_files):
      src = "{}/{}/{}".format(repo_path,source_file_folder,file)
      dst = "{}/{}".format(work_dir,file)
      copyfile(src,dst)
      # Decompress mars crustal/mantle files, since they are quite large
      compress = Popen(["gunzip",file],cwd=work_dir)
      compress.wait()
  except FileNotFoundError:
    raise("Cannot find files, make sure they are in the same directory as this script!")
  
  print("! Writing plot config file... ",end="")

  write_yaml(work_dir,mant_ext,core_frac,al,fe,exit_time,init_time)

  print("Done!")

  print("! Creating init file... ",end="")
  # Read in template file
  template_filename = "{}/init-template.pytemp".format(repo_path)
  try:
    with open(template_filename) as template_file:
      template_text = template_file.read()
      template = Template(template_text)
  except FileNotFoundError:
    raise("Template file not found! Make sure it is in the same directory as this script")

  # Begin modifying template
  init_params = {}
  # Resolution
  init_params["x_res"] = "{}-xnumx".format(xyres)
  init_params["y_res"] = "{}-ynumy".format(xyres)
  # Format string for exit time
  init_params["exit_time"] = "{:.3e}-timeexit(yr)".format(exit_time)
  init_params["init_time"] = "{:.3e}-timesum(yr)".format(init_time)
  # Calculate abundance ratio from Solar System values
  al26_ss_abun = 5.250 # Al_26/Al_27 solar system ratio, in units of 1e-5
  fe60_ss_abun = 1.150 # Fe_60/Fe_56 solar system ratio, in units of 1e-8
  al26_abun = al * al26_ss_abun
  fe60_abun = fe * fe60_ss_abun
  # Format strings
  init_params["al_abun"] = "{:.3f}-al2627_init(e-5,ss_0=5.250)".format(al26_abun)
  init_params["fe_abun"] = "{:.3f}-fe6056_init(e-8,ss_0=1.150)".format(fe60_abun)
  # Calculate core and mantle size
  comp = ""
  core_ext   = core_frac * mant_ext
  core_ext_m = int(core_ext * 1000)
  mant_ext_m = int(mant_ext * 1000)
  init_params["core_extent"] = "{}".format(core_ext_m)
  init_params["mantle_extent"] = "{}".format(mant_ext_m)
  # Calculate simulation size, which is the diameter of the planetisemal
  sim_ext_m = int(mant_ext_m * 2.5)
  sim_grav_m = int(sim_ext_m / 2.0) # Recalc grav
  # Check to see if a core is included
  if core_ext > 0:
    comp += "/Iron_1\n"
    comp += " 3 7 0.5 0.5 0.5 0.5 m{} m0 0 360\n".format(core_ext_m)
  # Build mantle
  comp += "/Wet_Silicates\n"
  comp += " 3 6 0.5 0.5 0.5 0.5 m{} m{} 0 360\n".format(mant_ext_m,core_ext_m)
  # Build surrounding vacuum, "air"
  comp += "/AIR\n"
  comp += " 3 0 0.5 0.5 0.5 0.5 m{} m{} 0 360".format(sim_ext_m,mant_ext_m)
  init_params["composition"] = comp
  # Format string for GRID_PARAMETERS_DESCRIPTIONS
  init_params["x_size"] = "{}-xsize(m)".format(sim_ext_m)
  init_params["y_size"] = "{}-ysize(m)".format(sim_ext_m)
  init_params["xy_grav"] = "{:.4e}-GYKOEF_RADIUS(m)".format(sim_grav_m)
  # Convert template and write
  init_data = template.substitute(init_params)
  init_filename = "{}/init.t3c".format(work_dir)
  with open(init_filename,"w") as init_file:
    init_file.write(init_data)
  print("! Done!\nRunning initialisation programme")

  if grain_volume_frac == False:
    # Execute in2mart
    in2elvis = "in2mart".format(repo_path)
    initialise = Popen([in2elvis],cwd=work_dir)
  else:
    # Execute in2mart_grain
    in2elvis = "in2mart_grain".format(repo_path)
    initialise = Popen([in2elvis,str(grain_volume_frac)],cwd=work_dir)

  print("!!! Environment setup in {} finished !!!".format(work_dir))
  return

if __name__ == "__main__":
  parse = argparse.ArgumentParser(description="Initialise the i2elvis code in a separate folder")
  parse.add_argument("planet_size",type=float,help="Planetesimal Size (km)")
  parse.add_argument("core_ratio",type=float,help="Core ratio (fraction)")
  parse.add_argument("al26_ratio",type=float,help="Al26/Al27 ratio comparative to solar system ratio")
  parse.add_argument("fe60_ratio",type=float,help="Fe60/Fe56 ratio comparative to solar system ratio")
  parse.add_argument("-i","--init_time",type=float,default=1e6,help="Exit time in years, default is 1Myr")
  parse.add_argument("-e","--exit_time",type=float,default=20e6,help="Exit time in years, default is 20Myr")
  parse.add_argument("-f","--folder_name",type=str,help="Folder name, defaults to sim_p_<planet_size>_c_<core_ratio>_al_<al26_ratio>_fe_<fe60_ratio>")
  parse.add_argument("-xy","--xysize",type=int,default=251,help="Simulation resolution in cells")
  args = parse.parse_args()
  # Use argparse as a wrapper
  mant_ext  = args.planet_size
  core_ext  = args.core_ratio
  al        = args.al26_ratio
  fe        = args.fe60_ratio
  exit_time = args.exit_time
  init_time = args.init_time
  xysize = args.xysize
  # Make folder name if none specified
  if args.folder_name == None:
    work_dir = "sim_p_{}_c_{}_al_{}_fe_{}".format(int(mant_ext),int(core_ext),al,fe)
    print(work_dir)
  else:
    work_dir = args.folder_name
  # Start
  gen_sim(mant_ext,core_ext,al,fe,exit_time,init_time,work_dir,xyres=xysize)