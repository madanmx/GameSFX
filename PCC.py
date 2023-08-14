#!/usr/bin/env python3
#############################################################
#	                                                    #
#  (c) 2023 Madan Kumar Shankar <madan.shankar@kemi.uu.se>  #
#   Version Thursday 12th July 2023 15:00 CEST              #  
#           Thursday 12th July 2023 19:00 IST               #
#############################################################

import numpy as np
import math
import sys
import re
from math import sqrt


#USAGE: use pcc.inp # It is an input file to the program PCC.py
# Calculated difference/reference electron density map
# Observed difference electron density map
# OUTMAP for displaying spherical volume only
# Number of symmetry
# Symetry operators
# Coordinates
# Radius of the sphere


#================Input=================
#Input the file
with open('pcc.inp') as f:
  lines= f.readlines()

FREF=   lines[0].rstrip()  # REFERENCE DIFFERENCE ELECTRON DENSITY
print(f'{FREF}')
FRO=    lines[1].rstrip()  # OBSERVED DIFFERENCE ELECTRON DENSITY
print(f'{FRO}')
OUTMAP= lines[2].rstrip()  # OUTPUT MAP DISPAYING SPHERICAL VOLUME ONLY
print(f'{OUTMAP}')

NSYM=   int(lines[3].rstrip())   #  READ NUMBER OF SYMMETRY OPERATORS (FOR OUTPUT ONLY) ===>
print(f'{NSYM}')
#NNSYM is NSYM

SYMOPS= [lines[i].rstrip() for i in range(4,4+NSYM)]  # READ SYMMETRY OPERATORS (FOR OUTPUT ONLY) ===>
print(f'{SYMOPS}')

X,Y,Z = [float(i) for i in lines[4+NSYM].rstrip().split()] #PRINT SYMMETRY OPEATOR
print(f'{X,Y,Z}')

RADIUS= float(lines[4+NSYM+1].rstrip()) #INPUT RADIUS AROUND THE SELECTED COORDINATE
print(f'{RADIUS}')

#VARIABLES USED: FREF, FRO, OUTMAP, NSYM, SYMOPS, X,Y,Z, RADIUS
MASK = np.zeros(100000)

#===============READ MAP======================================================================
def RDCCP4(FNAM):
  f=open(FNAM,'rb')

  header=np.fromfile(f, [('NC','i4'),('NR','i4'),('NS','i4'),
                       ('NMODE','i4'),('NCST','i4'),('NRST','i4'),
                       ('NSST','i4'),('NNX','i4'),('NNY','i4'),
                       ('NNZ','i4'),('CELL','f4',(6,)),
                       ('MAPC','i4'),('MAPR','i4'),('MAPS','i4'),
                       ('AAMN','f4'),('AAMX','f4'),
                       ('AAMEAN','f4'),
                       ('IISPG','i4'), ('NSB','i4'),('LSKF','i4'),
                       ('SKIP','i4',(28)),
                       ('MACH','i4'),
                       ('AARMS','f4'),('NLABL','i4'),
                       ('CLABL1','|S80',(1,)),
                       ],
                         count=1)
  f.close()

  NC, NR, NS= header[['NC','NR','NS']][0]
  NMODE= header['NMODE'][0]
  NCST, NRST, NSST= header[['NCST','NRST','NSST']][0]
  MAPC, MAPR, MAPS, ISPG, NSB, NLABL= header[['MAPC','MAPR','MAPS','IISPG','NSB','NLABL']][0]
  NX, NY, NZ= header[['NNX','NNY','NNZ']][0]
  AMN= header['AAMN'][0]
  AMX= header['AAMX'][0]
  AMIN= AMN; AMAX= AMX; 
  AMEAN, ARMS= header[['AAMEAN','AARMS']][0]
  MACH= header[['MACH']][0]
  CLABL= header['CLABL1'][0].astype('|U80')[0]
  CCELL= header['CELL'][0]
  
  NSW = NSB // 4
  
  # Calculate total number of bytes and words
  IR = NC * NR * NS + 256 + NSW
  NOR = IR // 256
  NREST = IR % 1024
  NBYTE = IR * 4
  NTOT = IR
  NHDRS = 256 + NSW
  BUFI = np.fromfile(FNAM, dtype=np.float32, count=NTOT)
  print(f' NUMBER OF COLUMNS      : {NC:10d}')
  print(f' NUMBER OF ROWS         : {NR:10d}')
  print(f' NUMBER OF SECTIONS     : {NS:10d}')
  print(f' MODE (O,1,2,3,4)       : {NMODE:10d}')
  print(f' FIRST COLUMN IN MAP    : {NCST:10d}')
  print(f' FIRST ROW IN MAP       : {NRST:10d}')
  print(f' FIRST SECTION IN MAP   : {NSST:10d}')
  print(f' INTERVALS ALONG X      : {NX:10d}')
  print(f' INTERVALS ALONG Y      : {NY:10d}')
  print(f' INTERVALS ALONG Z      : {NZ:10d}')
  print(f' CELL DIMENSIONS ')
  print(f' A      : {CCELL[0]:10.3f}')
  print(f' B      : {CCELL[1]:10.3f}')
  print(f' C      : {CCELL[2]:10.3f}')
  print(f' ALPHA  : {CCELL[3]:10.3f}')
  print(f' BETA   : {CCELL[4]:10.3f}')
  print(f' GAMMA  : {CCELL[5]:10.3f}')
  print(f' AXIS CORRESPONDING TO COLUMNS  : {MAPC:6d}')
  print(f' AXIS CORRESPONDING TO ROWS     : {MAPR:6d}')
  print(f' AXIS CORRESPONDING TO SECTIONS : {MAPS:6d}')
  print(f' SPACE GROUP NUMBER             : {ISPG:6d}')
  print(f' BYTES USED TO STORE SYM-OPS    : {NSB:6d}')
  print(f' NUMBER OF LABELS USED          : {NLABL:6d}')
  print(f' MINIMUM DENSITY IN MAP         : {AMIN:6f}')
  print(f' MAXIMUM DENSITY IN MAP         : {AMAX:6f}')
  print(f' AVERGAE (MEAN) DENSITY IN MAP  : {AMEAN:6f}')
  print(f' RMS DEVIATION FROM AVERAGE     : {ARMS:6f}')
  print(f' MACHINE STAMP INT REPRESENT    : {MACH}')
  print(f' LABEL({1}):{CLABL}')
  # Print total size information
  print(f"Number of 256 Word Records (Incl. Header): {NOR} + 1 Partially Filled by {NREST} Words")
  print(f"Total Bytes: {NBYTE}, Total Words: {NTOT}")
  print(f"Entire File Will Be Read:")
  print(f"Total Bytes: {NBYTE}, Total Words: {NTOT}, Header: {NHDRS}")

  # Return the header information as a dictionary
  header_info = {
        'NC': NC,
        'NR': NR,
        'NS': NS,
        'NMODE': NMODE,
        'NCST': NCST,
        'NRST': NRST,
        'NSST': NSST,
        'NX': NX,
        'NY': NY,
        'NZ': NZ,
        'CCELL': CCELL,
        'MAPC': MAPC,
        'MAPR': MAPR,
        'MAPS': MAPS,
        'ISPG': ISPG,
        'NSB': NSB,
        'NLABL': NLABL,
        'AMIN': AMIN,
        'AMAX': AMAX,
        'AMEAN': AMEAN,
        'ARMS': ARMS,
        'MACH': MACH,
        'CLABL': CLABL,
        'BUFI' : BUFI
    }
  print(f'{BUFI}')
  return header_info, BUFI, CCELL, NX, NY, NZ, NHDRS, ARMS, AMEAN

#=============Call RDCCP4====================================
header_info_FREF, BUFI_FREF, CCELL_FREF, NX, NY, NZ, NHDRS, ARMS, AMEAN = RDCCP4(FREF)
CCELL = header_info_FREF['CCELL']
CELL = CCELL
BUFI = BUFI_FREF
header_info_FRO, BUFI_FRO, CCELL_FRO, NX, NY, NZ, NHDRS, ARMS, AMEAN = RDCCP4(FRO)
CCELL = header_info_FREF['CCELL']
CELL = CCELL
BUFI = BUFI_FREF

#============================================================

#====================================MATSYM===========================
def MATSYM(TEXT):
  VALID= ['1','2','3','4','5','6','X','Y','Z','-','+','/',',',' ']
  MATSYM= 0; # No error
 
  # Check if TEXT contains only VALID characters
  if not set(TEXT) <= set(VALID):
    MATSYM = 1
    print('ERROR: ILLEGAL CHARACTER ON SYMMETRY CARD!')
    exit()
  # Check there are 2 commas in the symmetry
  if not TEXT.count(',') == 2:
    MATSYM= 3
    print('ERROR: INCORRECT NUMBER OF COMMAS')

  #----CLEAR SYMOP ARRAY
  S= np.zeros([3,4])

  # Run over fieds
  FIELDS= TEXT.split(',')
  for i,FIELD in enumerate(FIELDS):
    if   '-X' in FIELD:                    S[i]= S[i] + np.array([-1.0, 0.0, 0.0, 0.0])
    elif '+X' in FIELD or 'X' in FIELD:    S[i]= S[i] + np.array([ 1.0, 0.0, 0.0, 0.0])

    if   '-Y' in FIELD:                    S[i]= S[i] + np.array([ 0.0,-1.0, 0.0, 0.0])
    elif '+Y' in FIELD or 'Y' in FIELD:    S[i]= S[i] + np.array([ 0.0, 1.0, 0.0, 0.0])
    
    if   '-Z' in FIELD:                    S[i]= S[i] + np.array([ 0.0, 0.0,-1.0, 0.0])
    elif '+Z' in FIELD or 'Z' in FIELD:    S[i]= S[i] + np.array([ 0.0, 0.0, 1.0, 0.0])

    res= re.search('[+-]?[1234/6]+',FIELD)
    if res:  S[i]= S[i] + np.array([0.0, 0.0, 0.0, eval(res[0])])

  if not math.isclose( abs(np.linalg.det(S[:,:3])) -1 , 0.0 ):
    MATHSYM= 4
    print('ERROR: DETERMINANT IS NOT + OR - 1')
    exit()

  return S
  
##########Print Symmetry #######################
SYM= np.zeros([NSYM,3,4])

for i,CARD in enumerate(SYMOPS):
  print(f'SYMMETRY OPERATOR:  {i+1}     {CARD}')
  SYM[i]= MATSYM(CARD)
  print(f'      {SYM[i,0,0]:4.1f} {SYM[i,0,1]:4.1f} {SYM[i,0,2]:4.1f}        {SYM[i,0,3]:.5f}')
  print(f'      {SYM[i,1,0]:4.1f} {SYM[i,1,1]:4.1f} {SYM[i,1,2]:4.1f}        {SYM[i,1,3]:.5f}')
  print(f'      {SYM[i,2,0]:4.1f} {SYM[i,2,1]:4.1f} {SYM[i,2,2]:4.1f}        {SYM[i,2,3]:.5f}')
  print('\n')

###################Working till ################

#========================SETMAT=================
def SETMAT(CELL):
    # Initialize variables
    MAT = [[0.0] * 3 for _ in range(3)]
    IMAT = [[0.0] * 3 for _ in range(3)]
    G = [[0.0] * 3 for _ in range(3)]

    # Conversion factor from degrees to radians
    D = 0.017453

    # Set up orthogonalization matrix
    CABG = [math.cos(CELL[i+3] * D) for i in range(3)]
    SABG = [math.sin(CELL[i+3] * D) for i in range(3)]

    # Handle special case when CELL(I+3) equals 90.0
    for i in range(3):
        if CELL[i+3] == 90.0:
            CABG[i] = 0.0
            SABG[i] = 1.0

    CABGS = (CABG[1] * CABG[2] - CABG[0]) / (SABG[1] * SABG[2])
    SABGS = math.sqrt(1.0 - CABGS * CABGS)

    MAT[0][0] = CELL[0]
    MAT[0][1] = CELL[1] * CABG[2]
    MAT[0][2] = CELL[2] * CABG[1]
    MAT[1][1] = CELL[1] * SABG[2]
    MAT[1][2] = -CELL[2] * SABG[1] * CABGS
    MAT[2][2] = CELL[2] * SABG[1] * SABGS

    # Set up inverse matrix
    IMAT[0][0] = 1.0 / MAT[0][0]
    IMAT[0][1] = -MAT[0][1] / (MAT[0][0] * MAT[1][1])
    IMAT[0][2] = (MAT[0][1] * MAT[1][2] - MAT[0][2] * MAT[1][1]) / (MAT[0][0] * MAT[1][1] * MAT[2][2])
    IMAT[1][1] = 1.0 / MAT[1][1]
    IMAT[1][2] = -MAT[1][2] / (MAT[1][1] * MAT[2][2])
    IMAT[2][2] = 1.0 / MAT[2][2]

    # Set up metric tensor
    G[0][0] = MAT[0][0] * MAT[0][0]
    G[0][1] = 2.0 * MAT[0][0] * MAT[0][1]
    G[0][2] = 2.0 * MAT[0][0] * MAT[0][2]
    G[1][1] = MAT[0][1] * MAT[0][1] + MAT[1][1] * MAT[1][1]
    G[1][2] = 2.0 * MAT[0][1] * MAT[0][2] + 2.0 * MAT[1][1] * MAT[1][2]
    G[2][2] = MAT[0][2] * MAT[0][2] + MAT[1][2] * MAT[1][2] + MAT[2][2] * MAT[2][2]

    # Print matrices for visualization
    print("-----------------------------------")
    print("ORTHOGONALIZATION MATRIX")
    for row in MAT:
        print("{:10.5f} {:10.5f} {:10.5f}".format(*row))
    print("-----------------------------------")
    print("INVERSE OF ORTHOGONALIZATION MATRIX")
    for row in IMAT:
        print("{:10.5f} {:10.5f} {:10.5f}".format(*row))
    print("-----------------------------------")

    return MAT, IMAT, G
#============Call SETMAT====================
MAT, IMAT, G = SETMAT(CELL)
#============Worked till now================

#===============Gen_MASK====================
#NM is the number of grid points within the mask
#MASK the mask of grid point number within a sphere are stored in the MASK array 

def GEN_MASK(RADIUS, X, Y, Z, MASK, NM, NX, NY, NZ):
    
  # Constants
    XF, YF, ZF = O2F(X, Y, Z, IMAT[0][0], IMAT[0][1], IMAT[0][2], IMAT[1][1], IMAT[1][2], IMAT[2][2])

    XA = CCELL[0] / (2.0 * NX)
    YA = CCELL[1] / (2.0 * NY)
    ZA = CCELL[2] / (2.0 * NZ)

    # Determine boundaries
    XMAX = X + (RADIUS + XA)
    XMIN = X - (RADIUS + XA)
    YMAX = Y + (RADIUS + YA)
    YMIN = Y - (RADIUS + YA)
    ZMAX = Z + (RADIUS + ZA)
    ZMIN = Z - (RADIUS + ZA)

    # Fractionalize coordinates and boundaries
    XMXF, _, _ = O2F(XMAX, Y, Z, IMAT[0][0], IMAT[0][1], IMAT[0][2], IMAT[1][1], IMAT[1][2], IMAT[2][2])
    XMNF, _, _ = O2F(XMIN, Y, Z, IMAT[0][0], IMAT[0][1], IMAT[0][2], IMAT[1][1], IMAT[1][2], IMAT[2][2])
    _, YMXF, _ = O2F(X, YMAX, Z, IMAT[0][0], IMAT[0][1], IMAT[0][2], IMAT[1][1], IMAT[1][2], IMAT[2][2])
    _, YMNF, _ = O2F(X, YMIN, Z, IMAT[0][0], IMAT[0][1], IMAT[0][2], IMAT[1][1], IMAT[1][2], IMAT[2][2])
    _, _, ZMXF = O2F(X, Y, ZMAX, IMAT[0][0], IMAT[0][1], IMAT[0][2], IMAT[1][1], IMAT[1][2], IMAT[2][2])
    _, _, ZMNF = O2F(X, Y, ZMIN, IMAT[0][0], IMAT[0][1], IMAT[0][2], IMAT[1][1], IMAT[1][2], IMAT[2][2])

    print(f" BOX FROM {XMIN:.3f} TO {XMAX:.3f},      {YMIN:.3f} TO {YMAX:.3f},      {ZMIN:.3f} TO {ZMAX:.3f}\n"
      f"       {XMIN:.3f}   {XMAX:.3f} ||  {YMIN:.3f}   {YMAX:.3f} ||  {ZMIN:.3f}   {ZMAX:.3f}")


    # Determine search box boundaries
    NXMX = int(XMXF * NX) + 2
    NXMN = int(XMNF * NX) - 2
    NYMX = int(YMXF * NY) + 2
    NYMN = int(YMNF * NY) - 2
    NZMX = int(ZMXF * NZ) + 2
    NZMN = int(ZMNF * NZ) - 2

    # Run through search box
    LL = 0
    NNX = NXMX - NXMN
    NNY = NYMX - NYMN
    NNZ = NZMX - NZMN

    print(" BOX GRID FROM NXMIN TO NXMAX, NYMIN TO NYMAX, NZMIN TO NZMAX \n"
      " NXMIN   {:8d} || NYMIN  {:8d} || NZMIN  {:8d} \n"
      " NXMAX   {:8d} || NYMAX  {:8d} || NZMAX  {:8d} \n"
      " TOTALX  {:8d} || TOTALY {:8d} || TOTALZ {:8d}".format(NXMN, NYMN, NZMN, NXMX, NYMX,NZMX, NNZ, NNY, NNZ))
    
       
    for JJ in range(1, NNZ + 1):
        for KK in range(1, NNY + 1):
            for II in range(1, NNX + 1):
                J = NZMN + JJ - 1
                K = NYMN + KK - 1
                I = NXMN + II - 1
                GFX = float(I) / float(NX)
                GFY = float(K) / float(NY)
                GFZ = float(J) / float(NZ)
                DX = GFX - XF
                DY = GFY - YF
                DZ = GFZ - ZF
                DIST = OL(DX, DY, DZ, IMAT[0][0], IMAT[0][1], IMAT[0][2], IMAT[1][1], IMAT[1][2], IMAT[2][2])

                if DIST < RADIUS:
                    LL += 1
                    KKK = K
                    JJJ = J
                    III = I

                    if KKK <= 0:
                        KKK = NY + KKK
                    if KKK > NY:
                        KKK -= NY
                    if JJJ <= 0:
                        JJJ = NZ + JJJ
                    if JJJ > NZ:
                        JJJ -= NZ
                    if III <= 0:
                        III = NX + III
                    if III > NX:
                        III -= NX

                    NGRID = JJJ * NX * NY + III * NY + KKK
                    MASK[LL - 1] = NGRID + NHDRS
    print(f'Print the MASK {MASK}')
    NM = LL
    print(f'Total number of grid points within selected region is {NM}')
    return NM, MASK
    
#==================================================================    
def O2F(X, Y, Z, IMAT11, IMAT12, IMAT13, IMAT22, IMAT23, IMAT33):
    XF = X * IMAT11 + Y * IMAT12 + Z * IMAT13
    YF = X * IMAT12 + Y * IMAT22 + Z * IMAT23
    ZF = X * IMAT13 + Y * IMAT23 + Z * IMAT33
    return XF, YF, ZF

#==================================================================
# Calculate the orthogonal distance
def OL(XF, YF, ZF, MAT11, MAT12, MAT13, MAT22, MAT23, MAT33):
    XO = XF * MAT11 + YF * MAT12 + ZF * MAT13
    YO = XF * MAT12 + YF * MAT22 + ZF * MAT23
    ZO = XF * MAT13 + YF * MAT23 + ZF * MAT33
    D = sqrt(XO ** 2 + YO ** 2 + ZO ** 2)
    return D
#===================================================================
#Calculate the total number of grid points in the map
Total_grid_points = NX * NY * NZ 
MASK = np.zeros(Total_grid_points, dtype=int)
NM = np.zeros(1, dtype=int)
NM, MASK = GEN_MASK(RADIUS, X, Y, Z, MASK, NM, NX, NY, NZ)
print(f'The Number of grid points in the MASK for {RADIUS} Å is {NM}')

#===================GETRHO=============================================
#MASK contain gridpoint number
#RHO contain value of electron density at gridpoint number
#NP number of points in the mask
#This uses grid values stored in MASK to extract RHO values from a map
NP = NM
def GETRHO(MASK, RHO, NP, BUFI):
  for i in range(NP):
    NGRID = MASK[i]
    #RHO.APPEND(BUFI[NGRID])
    RHO.append(BUFI[NGRID-1])
  return RHO
  
header_info_FREF, BUFI_FREF, CCELL_FREF, NX, NY, NZ, NHDRS, ARMS, AMEAN = RDCCP4(FREF)
ARMS1 = ARMS
AR1 = ARMS1
CCELL = header_info_FREF['CCELL']
CELL = CCELL
NM = np.zeros(1, dtype=int)
NM, MASK = GEN_MASK(RADIUS, X, Y, Z, MASK, NM, NX, NY, NZ)
RHO1 = []
RHO1 = GETRHO(MASK, RHO1, NP, BUFI_FREF)

header_info_FRO, BUFI_FRO, CCELL_FRO, NX, NY, NZ, NHDRS, ARMS, AMEAN = RDCCP4(FRO)
ARMS2 = ARMS
AR2 =ARMS2
RHO2 = []
RHO2 = GETRHO(MASK, RHO2, NP, BUFI_FRO)


#===============PCC function=====================================
def PCORR(RHOF, RHOO, NM, AR1, AR2, IPOS, RR):
    # Initialize variables
    RSM1 = 0.0
    RSM2 = 0.0
    IPOS = 0

    # Set threshold for the Pearson correlation
    RRRD = 1.5

    # Variables to calculate the Pearson correlation
    ANUM = 0.0
    DNM1 = 0.0
    DNM2 = 0.0

    # Loop to calculate RSM1 and RSM2
    for i in range(NM):
        if (RHO1[i] > RRRD * AR1 or RHO2[i] > RRRD * AR2 or
            RHO1[i] < -RRRD * AR1 or RHO2[i] < -RRRD * AR2):
            RSM1 += RHO1[i]
            RSM2 += RHO2[i]
            IPOS += 1

    # Calculate average RSM1 and RSM2
    RSM1 /= IPOS
    RSM2 /= IPOS

    # Loop to calculate the numerator and denominators
    for i in range(NM):
        ANUM += (RHO1[i] - RSM1) * (RHO2[i] - RSM2)
        DNM1 += (RHO1[i] - RSM1) ** 2
        DNM2 += (RHO2[i] - RSM2) ** 2

    # Calculate the Pearson correlation coefficient (RR)
    RR = ANUM / (math.sqrt(DNM1 * DNM2))
    print(f'{RR}')
    return RR

IPOS = 0
RR = 0.0
pcc_value = PCORR(RHO1, RHO2, NM, AR1, AR2, IPOS, RR)
print("Pearson correlation coefficient:", pcc_value)





























