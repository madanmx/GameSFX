#!/usr/bin/env python3
#############################################################
#							     #	 
#                                                           #
#  (c) 2023 Madan Kumar Shankar <madan.shankar@kemi.uu.se>  #
#   Version Thursday 10th June 2023 15:00 CEST              #  
#           Thursday 10th June 2023 19:00 IST               #
#############################################################

import sys
import os
import subprocess
import numpy as np
from math import sqrt

#USAGE: Keep the dark.mtz and light.mtz/set of light.mtz file in the same directory 
#       Files to keep in the same directory:
#       1. dark.mtz
#       2. light.mtz (ex:1ps, 500fs, 3ps)
#       3. dark.pdb
#       4. refine.mtz
#       where the DEDmap.py is copied.
#      ./DEDmap.py timepoint
##ex:  ./DEDmap.py 1ps

timepoint = sys.argv[1]
os.mkdir(timepoint)
os.chdir(timepoint)
print(f'You entered {timepoint} for the generating DED map')

#Set the files and make sure they are in the same older where the DED_maps exists!!
#*****************************************************************
dark_model = "dark.pdb"          #Set the dark.pdb here
OFF = "dark.mtz"                 #Set the dark reflections here   
F_model = "dark_phases.mtz"      #Set the refined dark phases here  
ON = "timepoint.mtz"             #Set the light reflections here   
#*****************************************************************

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
print(f'The maximum resolution and minimum resolution for DED maps are {max_res} and {min_res}') 

mtzv = (
    f"mtz2various HKLIN ../{F_model} HKLOUT model_phs.hkl <<eof > mtz2various.log\n"
    f"LABIN FP=FC_ALL PHIC=PHIC_DARK \n"
    f"OUTPUT USER '(3I5,F12.3,' 1.00 ',F12.3)'\n"
    f"END"
    )
subprocess.Popen(mtzv,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()

f2mtz_DED = "f2mtz_DED.txt"

with open(f2mtz_DED, "w") as f:
    f.write(f"CELL {a} {b} {c} {alpha} {beta} {gamma}\n")
    f.write(f"SYMM {spacegroup_symmetry}\n")
    f.write("LABOUT H K L FC_DARK SIG_FC_DARK PHI_DARK \n")
    f.write("CTYPE H  H  H   F   Q   P\n")
    f.write("END")
subprocess.Popen(f"f2mtz HKLIN model_phs.hkl HKLOUT FC_DARK.mtz < {f2mtz_DED} > f2mtz_DED.log", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()

cad_DED = (
    f"cad HKLIN1 FC_DARK.mtz HKLIN2 ../dark.mtz HKLIN3 ../{timepoint}.mtz HKLOUT all.mtz << eof > cad_DED.log \n"
    f"LABIN FILE 1 E1=FC_DARK E2=SIG_FC_DARK E3=PHI_DARK \n"
    f"CTYP  FILE 1 E1=F E2=Q E3=P  \n"
    f"LABIN FILE 2 E1=F_DARK E2=SIGF_DARK \n"
    f"CTYP  FILE 2 E1=F E2=Q \n"
    f"LABIN FILE 3 E1=F_{timepoint} E2=SIGF_{timepoint} \n"
    f"CTYP  FILE 3 E1=F E2=Q \n"
    f"END"
    )
subprocess.Popen(cad_DED, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()  


# Scaling:scale the things
# 1 scale dark to FC dark
# 2 scale light to dark
print(f'Scaling Dark to FC dark')


scale1 = (
   f"scaleit HKLIN all.mtz HKLOUT all_sc1.mtz << eof >scaleit1.log \n"
   f"TITLE FPHs scaled to FP \n"
   f"reso {min_res} {max_res} \n"
   f"EXCLUDE FP SIG 4 FMAX 10000000 \n"
   f"REFINE ANISOTROPIC \n"
   f"LABIN FP=FC_DARK SIGFP=SIGF_DARK - \n"
   f"FPH1=F_DARK SIGFPH1=SIGF_DARK - \n"
   f"FPH2=F_{timepoint} SIGFPH2=SIGF_{timepoint} \n"
   f"CONV ABS 0.0001 TOLR  0.000000001 NCYC 150 \n"
   f"END"
   )
subprocess.Popen(scale1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()  

print(f'Scaling Light to Dark')

scale2 = (
   f"scaleit HKLIN all_sc1.mtz HKLOUT all_sc2.mtz << eof >scaleit2.log \n"
   f"TITLE FPHs scaled to FP \n"
   f"reso {min_res} {max_res} \n"
   f"WEIGHT \n"
   f"EXCLUDE FP SIG 4 FMAX 10000000 \n"
   f"REFINE ANISOTROPIC \n"
   f"LABIN FP=F_DARK SIGFP=SIGF_DARK - FPH1=F_{timepoint} SIGFPH1=SIGF_{timepoint} \n"
   f"CONV ABS 0.0001 TOLR  0.000000001 NCYC 50 \n"
   f"END"
   )
subprocess.Popen(scale2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()  

fhscal = (
   f"fhscal hklin all_sc1.mtz hklout all_sc2.mtz << eof >scaleit2.log \n"
   f"TITLE scale  by Kraut method \n"
   f"BIAS 1 ! iff we trust the standard deviations \n"
   f"LABIN FP=F_DARK SIGFP=SIGF_DARK FPH=F_{timepoint} SIGFPH=SIGF_{timepoint} \n"
   f"AUTO \n"
   f"END  \n"
   )
subprocess.Popen(fhscal, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()

freef = "freerflag HKLIN all_sc2.mtz HKLOUT all_sc2_free.mtz <<eof > freerflag.log \n freerfrac 0.05 \neof"
subprocess.Popen(freef,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()

nonw_map = (
    f"fft HKLIN all_sc2.mtz MAPOUT {timepoint}_nonw.map << eof >nonw_map.log \n"
    f"RESO {min_res}  {max_res} \n"
    f"GRID SAMPLE 3 \n"
    f"BINMAPOUT \n"
    f"LABIN F1=F_{timepoint} SIG1=SIGF_{timepoint} F2=F_DARK SIG2=SIGF_DARK PHI=PHI_DARK \n"
    f"END"
    )
subprocess.Popen(nonw_map,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()


# Scaled files to calculate the weighted map
m2v_light = (
    f"mtz2various HKLIN all_sc2.mtz  HKLOUT light_scaled.hkl << eof > m2v_light.log \n"
    f"LABIN FP=F_{timepoint} SIGFP=SIGF_{timepoint} \n"
    f"OUTPUT USER '(3I5,2F12.3)' \n"
    f"RESOLUTION {min_res}  {max_res} \n"
    f"END"
    )
subprocess.Popen(m2v_light,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()

m2v_dark = (
    f"mtz2various HKLIN all_sc2.mtz  HKLOUT dark_scaled.hkl << eof > m2v_dark.log \n"
    f"LABIN FP=F_DARK SIGFP=SIGF_DARK \n"
    f"OUTPUT USER '(3I5,2F12.3)' \n" 
    f"RESOLUTION {min_res}  {max_res} \n"
    f"END"
    )
subprocess.Popen(m2v_dark,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()

m2v_phase = (
    f"mtz2various HKLIN all_sc2.mtz  HKLOUT dark_phase.hkl << eof > m2v_phase.log \n"
    f"LABIN FP=FC_DARK SIGFP=SIG_FC_DARK PHIC=PHI_DARK \n"
    f"OUTPUT USER '(3I5,3F12.3)' \n"
    f"RESOLUTION {min_res}  {max_res} \n"
    f"END"
    )
subprocess.Popen(m2v_phase,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()

print(f'Difference structure factors calculation')
print(f'h k l DF weight Phase')

# Difference structure factors calculation
# h k l DF weight Phase
#########################DED.py###################################
offset=250
FDARK = np.empty([501,501,501,3])
FDARK[offset-150:offset+150, offset-150:offset+150, offset-150:offset+150, 2]= 999.9
# Load all files
f1= np.loadtxt('light_scaled.hkl', dtype={'names':('IH','K', 'L', 'F1', 'SIGF1'),        'formats':('i4','i4','i4','f8','f8')})
f2= np.loadtxt('dark_scaled.hkl', dtype={'names':('IH','K', 'L', 'F1', 'SIGMA'),        'formats':('i4','i4','i4','f8','f8')})
f3= np.loadtxt('dark_phase.hkl', dtype={'names':('IH','IK','IL','DM1','DM2', 'PHASE'), 'formats':('i4','i4','i4','f8','f8','f8')})
f3['PHASE']= np.where( f3['PHASE'] >  180.0 , f3['PHASE'] - 360.0, f3['PHASE'] )
f3['PHASE']= np.where( f3['PHASE'] < -180.0 , f3['PHASE'] + 360.0, f3['PHASE'] )
FDARK[offset+f3['IH'], offset+f3['IK'], offset+f3['IL'], 2] = f3['PHASE']
FDARK[offset+f2['IH'], offset+f2['K' ], offset+f2['L' ], 0] = f2['F1']
FDARK[offset+f2['IH'], offset+f2['K' ], offset+f2['L' ], 1] = f2['SIGMA']
light= len(f1)
phase= len(f3)
dark = len(f2)
# Matching HKLs from light_scaled.hkl to dark_scaled.hkl.
IC=    0
DFSQ=  0.0
S12SQ= 0.0
DF=    0.0
S12=   0.0
ADF=   0.0
DFSQ=  0.0

for IH,K,L,F1,SIGF1 in f1:
  if ( FDARK[offset+IH, offset+K, offset+L, 0] != 0.0 and FDARK[offset+IH, offset+K, offset+L, 2] != 999.9 ):
    DFSQ= (F1 - FDARK[offset+IH, offset+K, offset+L, 0])**2 + DFSQ
    S12SQ= SIGF1**2 + FDARK[offset+IH, offset+K, offset+L, 1]**2 + S12SQ
    # BE CONSISTENT WITH OTHERS, EASY TO CHANGE (SEE BELOW)
    DF= F1 - FDARK[offset+IH, offset+K, offset+L, 0] + DF
    ADF= abs(F1 - FDARK[offset+IH, offset+K, offset+L, 0]) + ADF
    S12= sqrt(SIGF1**2 + FDARK[offset+IH, offset+K, offset+L, 1]**2) + S12
    IC= IC + 1

DFSQM=  DFSQ/IC
S12SQM= S12SQ/IC
DFM=    DF/IC
S12M=   S12/IC
ADFM=   ADF/IC

# DETERMINE MEAN WEIGHT TO PRESERVE ABSOLUTE SCALE
IO=     0
WMEAN=  0
WZMEAN= 0


for IH,K,L,F1,SIGF1 in f1:
  if ( FDARK[offset+IH, offset+K, offset+L, 0] != 0.0 and FDARK[offset+IH, offset+K, offset+L, 2] != 999.9 ):
    # WEIGHT MEAN SQUARE
    DF= F1 - FDARK[offset+IH, offset+K, offset+L, 0]
    # DON'T TAKE SQRT, IN NEXT LINE WILL BE SQUARED AGAIN
    S12= SIGF1**2 + FDARK[offset+IH, offset+K, offset+L, 1]**2
    W= 1/(1+(DF**2/DFSQM) + (S12/S12SQM))
    # WEIGTH SQUARED MEAN
    WZ= 1/(1+(DF**2/ADFM**2) + (S12/S12M**2))
    WMEAN= WMEAN + W
    WZMEAN= WZMEAN + WZ
    IO= IO + 1

WMEAN= WMEAN/IO
WZMEAN= WZMEAN/IO

fout= open('light_dark.phs','w')
# CALCULATE WEIGHTS AND WRITE OUT DATA

DFDW= 0

for IH,K,L,F1,SIGF1 in f1:
  if ( FDARK[offset+IH, offset+K, offset+L, 0] != 0.0 and FDARK[offset+IH, offset+K, offset+L, 2] != 999.9):
    DF= (F1 - FDARK[offset+IH, offset+K, offset+L, 0] )
    DFDW= DFDW + DF / WMEAN
    S12= SIGF1**2 + FDARK[offset+IH, offset+K, offset+L, 1]**2
# WEIGHT MEAN SQUARE
    W= 1/(1+(DF**2/DFSQM) + (S12/S12SQM))
# WEIGHT SQUARED MEAN
    WZ= 1/(1+(DF**2/ADFM**2) + (S12/S12M**2))
# DIVIDE BY AVERAGE WEIGHT TO PRESERVE SCALE
    PHASE= FDARK[offset+IH, offset+K, offset+L, 2]
    if (DF < 0.0):
      DF= abs(DF)
      PHASE= PHASE + 180.0
      if (PHASE > 180.0):
         PHASE= PHASE - 360.0

    
    fout.write(f'{IH:5d}{K:5d}{L:5d}{DF/WMEAN:10.4f}{W:10.4f}{PHASE:10.4f}\n')

DFDW= DFDW / IO
fout.close()

print(f' NUMBER OF HKL IN Light_scaled                : {light:10d}')
print(f' NUMBER OF HKL IN Dark_scaled                 : {dark:10d}')
print(f' NUMBER OF PHASES IN Phases                   : {phase:10d}')
print(f' NUMBER OF MATCHING HKL                       : {IC:10d}')
print(f' NUMBER OF DIFFERENCE-F WRITTEN OUT           : {IO:10d}')
print(f' MEAN AMPLITUDE DIFFERENCE                      :  {DFM:14.4f}')
print(f' MEAN AMPLITUDE DIFFERENCE/<WEIGHT>          (M):  {DFDW:14.4f}')
print(f' MEAN AMPLITUDE DIFFERENCE SQUARED              :  {DFM**2:14.4e}')
print(f' MEAN ABSOLUTE AMPLITUDE DIFFERENCE             :  {ADFM:14.4f}')
print(f' MEAN ABSOLUTE AMPLITUDE DIFFERENCE SQUARED  (Z):  {ADFM**2:14.4f}')
print(f' MEAN SQUARE AMPLITUDE DIFFERENCE            (M):  {DFSQM:14.4f}')
print(f' MEAN SIGMA OF DIFFERENCE AMPLITUDES            :  {S12M:14.4f}')
print(f' MEAN SIGMA OF DIFFERENCE AMPLITUDES SQUARED (Z):  {S12M**2:14.4f}')
print(f' MEAN SQUARE SIGMA OF DIFFERENCE AMPLITUDES  (M):  {S12SQM:14.4f}')
print(f' AVERAGE WEIGHT                              (M):  {WMEAN:14.4f}')
print(f' AVERAGE Z WEIGHT                            (Z):  {WZMEAN:14.4f}')
####################################################################################################################################
print(f'Difference structure factors calculation ended and now the DED map calculation starts...')

f2m_weight = (
    f"f2mtz HKLIN light_dark.phs HKLOUT {timepoint}_dwt.mtz << EOF > f2m_weight \n"
    f"CELL {a} {b} {c} {alpha} {beta} {gamma}\n"
    f"SYMM {spacegroup_symmetry}\n"
    f"LABOUT H K L DOBS_{timepoint} FOM_{timepoint} PHI \n"
    f"CTYPE H H H F W P "
    f"END"
    )
subprocess.Popen(f2m_weight,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()

fft_weight = (
    f"fft HKLIN {timepoint}_dwt.mtz MAPOUT {timepoint}_wd.map << eof > fft_weight.log \n "
    f"RESO {min_res}  {max_res} \n"
    f"GRID SAMPLE 3 \n"
    f"BINMAPOUT \n"
    f"LABIN F1=DOBS_{timepoint} W=FOM_{timepoint} PHI=PHI \n"
    f"END"
    )
subprocess.Popen(fft_weight,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()


mapmask = (
    f"mapmask mapin {timepoint}_wd.map mapout {timepoint}.map xyzin ../dark.pdb << eof > mapmask.log \n"
    f"extend xtal \n"
    f"border 0.0 \n"
    f"END"
    )
subprocess.Popen(mapmask,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()

print(f'Now the DED map: {timepoint}.map, ready!!!')



