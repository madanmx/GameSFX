#!/usr/bin/env python3
# CCP4 Map reader in Python: Read and extract the values from CCP4 map files
#For more information on the CCP4 map data structure read https://www.ccp4.ac.uk/html/maplib.html#description
#############################################################
#                                                           #
#                                                           #
#  (c) 2023 Madan Kumar Shankar <madan.shankar@kemi.uu.se>  #
#   Version Thursday 3rd August 2023 11:00 CEST             #   
#                                                           #
#############################################################

import numpy as np
import math
import sys
import re
from math import sqrt


# Load REFERENCE DED map / Extrapolated map / any CCP4 map
MAP_FILE = input("Enter the map_file name (ex: file.map or file.ccp4)")
print(f'Name of the map is : {MAP_FILE}')


def ReadCCP4(MAP_FILE):
  f=open(MAP_FILE,'rb')

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
  
  IR = NC * NR * NS + 256 + NSW
  NOR = IR // 256
  NREST = IR % 1024
  NBYTE = IR * 4
  NTOT = IR
  NHDRS = 256 + NSW
  BUFI = np.fromfile(MAP_FILE, dtype=np.float32, count=NTOT)
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
  print(f' MACHINE STAMP FLOAT REPRESENT  : {MACH}')
  print(f' LABEL({1}):{CLABL}')
  # Print total size information
  print(f"Number of 256 Word Records (Incl. Header): {NOR} + 1 Partially Filled by {NREST} Words")
  print(f"Total Bytes: {NBYTE}, Total Words: {NTOT}")
  print(f"Entire File Will Be Read:")
  print(f"Total Bytes: {NBYTE}, Total Words: {NTOT}, Header: {NHDRS}")
 
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
  
  return header_info

#=============Call ReadDCCP4====================================
#Call the function to read the map
header_info = ReadCCP4(MAP_FILE)


  
  

