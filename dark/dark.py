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

#USAGE: Keep the dark_start.hkl in the same directory where the dark.py is intented to run.
#       The dark_start.hkl is a output file from CrystFEL with removing the text lines
#       in the file (top and bottom lines). This file has both negative and zero intensities in 
#       addition to the positive intensity reflections.            

#Set the dark_start.hkl here
dark_hkl = open("dark_start.hkl","r")

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

max_res = input("Enter the maximum resolution for dark data sets:\n")
min_res = input("Enter the minimum resolution for dark data sets:\n")
print(f'The maximum resolution and minimum resolution are {max_res} and {min_res}') 
 
filtered_lines = []

for line in dark_hkl:
    columns = line.split()
    if float(columns[3]) >= 0:
        filtered_lines.append(" ".join(columns[:4] + [columns[5]]))

dark_hkl.close()

with open("dark.hkl", "w") as output_file:
    output_file.write("\n".join(filtered_lines))


f2mtz_dark = "f2mtz_dark.txt"

with open(f2mtz_dark, "w") as f:
    f.write(f"CELL {a} {b} {c} {alpha} {beta} {gamma}\n")
    f.write(f"SYMM {spacegroup_symmetry}\n")
    f.write("LABOUT H K L I_DARK SIGI_DARK\n")
    f.write("CTYPE H H H J Q P\n")
    f.write("END")

subprocess.Popen(f"f2mtz HKLIN dark.hkl HKLOUT IOBS_dark.mtz < {f2mtz_dark} > f2mtz_dark.log", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()

os.remove(f2mtz_dark)

sort_dark = "sortmtz HKLIN IOBS_dark.mtz HKLOUT IOBS_sort.mtz <<eof > s2mtz_dark.log \n H K L \nend\neof"
subprocess.Popen(sort_dark,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()


trunc_dark = (
    f"truncate hklin IOBS_sort.mtz hklout FOBS_dark_tru.mtz << eof > tru_dark.log \n"
    f"title truncate dark intensities \n"
    f"truncate no \n"
    f"wilson all \n"
    f"nresidue {nres} \n"
    f"resolution {min_res} {max_res} \n"
    f"ranges 20 \n"
    f"rscale {min_res} {max_res} \n"
    f"labin IMEAN=I_DARK SIGIMEAN=SIGI_DARK \n"
    f"labout  F=F_DARK SIGF=SIGF_DARK\n"
    f"end\neof"
)

subprocess.Popen(trunc_dark, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()

free_dark = "free_dark.txt"
with open(free_dark, "w") as f:
	f.write("freerfrac 0.05 \n")
	f.write("END")
subprocess.Popen(f"freerflag HKLIN FOBS_dark_tru.mtz HKLOUT FOBS_dark_free.mtz << eof > free_dark.log", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()

os.remove(free_dark)


cad_dark = "cad hklin1 FOBS_dark_free.mtz hklout dark.mtz <<eof > cad_dark \n labi file 1 ALL \n sort H K L \n \nend\neof"
subprocess.Popen(cad_dark,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()


print(f'The final dark.mtz is ready for refinement and difference electron density map') 

