#!/usr/bin/env python3
#############################################################
#							     #	 
#                                                           #
#  (c) 2023 Madan Kumar Shankar <madan.shankar@kemi.uu.se>  #
#   Version Monday 12th June 2023 15:00 CEST                #  
#           Monday 12th June 2023 19:00 IST                 #
#############################################################


import sys
import os
import subprocess
import numpy as np
from math import sqrt

#USAGE:Make the directory dark_refine and copy the following files to this directory:
# 1. FOBS_dark.mtz  (The dark reflection file)
# 2. dark_start.pdb (The intial dark.pdb from the previous experiment)
# 3. cif of the cofactor/lignad (ex: LBV.cif)
# 4. Set the resolution RESO <low-res> <high-res> (ex:RESO 60 2.05)


refmac = (
    f"refmac5 HKLIN FOBS_dark.mtz HKLOUT refine.mtz XYZIN dark_start.pdb XYZOUT dark.pdb LIBIN <file.cif> << eof > refmac_log \n"
    f"REFI TYPE RESTRAINED \n" 
    f"RESO <low-res> <high-res> \n"
    f"REFI RESI MLKF \n"
    f"REFI BREF isotropic \n"
    f"LABIN FP=F_DARK SIGFP=SIGF_DARK FREE=FreeR_flag \n"
    f"LABOUT FC=FC_DARK PHIC=PHIC_DARK \n"
    f"NCYC 30 \n"
    f"END \n"
    )
subprocess.Popen(refmac, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() 

#Check the dark.pdb output from this script in coot then fit the residues/water/ligands if necessary and reun this script by changing the input
