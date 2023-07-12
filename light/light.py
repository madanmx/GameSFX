#!/usr/bin/env python3
############################################################
#
#
#  (c) 2023 Madan Kumar Shankar <madan.shankar@kemi.uu.se>
#   Version Thursday 1st June 2023 15:00 CEST
#           Thursday 1st June 2023 19:00 IST     
#############################################################

import sys
import os
import subprocess
import numpy as np
from math import sqrt
#USAGE: Keep all the time delay hkl in the hkl directory (ex: /hkl/1ps.hkl) 
#       Enter the correspoding time delay as input so that it will fetch the same for
#       preparing the timedelay/timepoint.mtz 

nres = input("Enter the number of residues: \n")
print(f'The number of resiudes entered is {nres}')

a = input("Enter the cell parameter a = \n")
b = input("Enter the cell parameter b = \n")
c = input("Enter the cell parameter c = \n")
alpha = input("Enter the cell parameter alpa = \n")
beta = input("Enter the cell parameter beta = \n")
gamma = input("Enter the cell parameter gamma = \n")
spacegroup_symmetry = input("Enter the spacegroup symmetry No. = \n")
print(f'The cell parameters are a = {a} Å, b = {b} Å, c = {c} Å, alpha = {alpha} deg, beta = {beta} deg, gamma = {gamma} deg \n')
print(f'The space group symeentry of the crystal is {spacegroup_symmetry}') 

max_res = input("Enter the maximum resolution for dark and light data sets:\n")
min_res = input("Enter the minimum resolution for dark and light data sets:\n")
print(f'The maximum resolution and minimum resolution are {max_res} and {min_res}') 
 
#Set the light.hkl
timepoint = input("Enter the timepoint:\n")  
timepoint = str(timepoint)                     
print(f'You entered {timepoint}')

path ='./hkl/'
timepoint_hkl = open(os.path.join(path, timepoint + '.hkl'), 'r') 
input_hkl = timepoint_hkl.read()
observations = len(input_hkl)
print(f'The total number of observations for given resolution are {observations} \n')

filtered_lines = []

for line in open(os.path.join(path, timepoint + '.hkl'), 'r'):
    columns = line.split()
    if float(columns[3]) >= 0:
        filtered_lines.append(" ".join(columns[:4] + [columns[5]]))

with open(timepoint + '.hkl' , 'w') as output_file:
    output_file.write("\n".join(filtered_lines))
    

f2mtz_light = (
      f"f2mtz HKLIN {timepoint}.hkl HKLOUT IOBS_{timepoint}.mtz << eof > f2mtz_light.log \n"
      f"CELL {a} {b} {c} {alpha} {beta} {gamma}\n"
      f"SYMM {spacegroup_symmetry}\n"
      f"LABOUT H K L I_{timepoint} SIGI_{timepoint}\n"
      f"CTYPE H H H J Q P\n"
      f"end\neof"
)
subprocess.Popen(f2mtz_light, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()


sort_light = (
	f"sortmtz HKLIN IOBS_{timepoint}.mtz HKLOUT IOBS_sort.mtz <<eof > s2mtz_light.log \n"
	f"H K L \n"
	f"end\neof"
)
subprocess.Popen(sort_light, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()


trunc_light = (
    f"truncate hklin IOBS_sort.mtz hklout FOBS_{timepoint}_tru.mtz <<eof > tru_light.log \n"
    f"title truncate light intensities \n"
    f"truncate no \n"
    f"wilson all \n"
    f"nresidue {nres} \n"
    f"resolution {min_res} {max_res} \n"
    f"ranges 20 \n"
    f"rscale {min_res} {max_res} \n"
    f"labin IMEAN=I_{timepoint} SIGIMEAN=SIGI_{timepoint} \n"
    f"labout  F=F_{timepoint} SIGF=SIGF_{timepoint}\n"
    f"end\neof"
)
subprocess.Popen(trunc_light, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()


free_light = (
    f"freerflag HKLIN FOBS_{timepoint}_tru.mtz HKLOUT FOBS_{timepoint}_free.mtz << eof > free_light.log \n"
    f"freerfrac 0.05 \n"
    f"end\neof"
)
subprocess.Popen(free_light, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()

cad_light = (
     f"cad hklin1 FOBS_{timepoint}_free.mtz hklout {timepoint}.mtz <<eof > cad_light.log \n"
     f"labi file 1 ALL \n"
     f"sort H K L \n"
     f"\nend\neof"
)
subprocess.Popen(cad_light, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()


print(f'The final timepoint mtz file, {timepoint}.mtz is ready for difference electron density map') 

    
