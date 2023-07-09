#!/usr/bin/env python3
#############################################################
#							                                #	 
#                                                           #
#  (c) 2023 Madan Kumar Shankar <madan.shankar@kemi.uu.se>  #
#   Version Sunday 9th July 2023 23:00 CEST                 #  
#           Monday 10th July 2023 02:30 IST                 #
#############################################################


import sys
import os
import subprocess
import numpy as np
from math import sqrt

#USAGE:Make the directory dark_refine and copy the following files to this directory:
# 1. dark.mtz  (The dark reflection file)
# 2. dark_start.pdb (The intial dark.pdb from the previous experiment)
# 3. cif of the cofactor/lignad (ex: LBV.cif)
# 4. Set the resolution RESO <low-res> <high-res> (ex:RESO 60 2.05)

dark_start = input("Enter the initial name of dark pdb for the refinement ex: dark : \n")
print(f'The name of the PDB is {dark_start}')

lig_cif = input("Enter the name of the ligand/cofactor ex. LBV : \n")
print(f'The name of the cofator/ligand CIF is {lig_cif}')

max_res = input("Enter the maximum resolution for dark structure refinement:\n")
min_res = input("Enter the minimum resolution for dark structure refinement:\n")
print(f'The maximum resolution and minimum resolution are {max_res} and {min_res}')

print(f'Now the dark structure refinement in progress...')


refmac = (
    f"refmac5 HKLIN dark.mtz HKLOUT dark_phases.mtz XYZIN {dark_start}.pdb XYZOUT dark.pdb LIBIN {lig_cif}.cif << eof > refmac_log \n"
    f"REFI TYPE RESTRAINED \n" 
    f"RESO {min_res} {max_res} \n"
    f"REFI RESI MLKF \n"
    f"REFI BREF isotropic \n"
    f"LABIN FP=F_DARK SIGFP=SIGF_DARK FREE=FreeR_flag \n"
    f"LABOUT FC=FC_DARK PHIC=PHIC_DARK \n"
    f"NCYC 30 \n"
    f"END \n"
    )
subprocess.Popen(refmac, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() 

print(f'End of the refinement and use the dark.pdb and dark_phases files for DED map plotting')


#Check the dark.pdb output from this script in coot then fit the residues/water/ligands if necessary and reun this script by changing the input
