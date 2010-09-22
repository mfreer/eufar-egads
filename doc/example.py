#!/usr/bin/env python

import egads
import egads.algorithms.thermodynamics as thermo

filenames = egads.get_file_list('data/*.nc')

f = egads.input.EgadsNetCdf()   # create EgadsNetCdf instance

for name in filenames:          # loop through files

    f.open(name, 'a')            # open NetCdf file 

    T_s = f.read_variable('T_t') # read in static temperature
    P_s = f.read_variable('P_s') # read in static pressure from file

    rho = thermo.density_dry_air_cnrm(P_s, T_s)  # calculate density

    f.write_variable(rho, 'rho', ('Time',))      # output variable

    f.close()                                    # close file

