# GameSFX
A set of python utilities for SFX dataset processing. The required tools are Python and CCP4i.
Part 1: Beamtime maps: Difference electron density map plotting using python programs.

In this part we have three plus one python programs;
1.dark.py      #Prepare the structure factors from hkls. FOBS_dark.mtz, Note: The negative intensities will not included
2.light.py     #Prepare the structure factors from hkls. FOBS_timepoint.mtz (ex: FOBS_1ps.mtz), Note: The negative intensities will not included
3.dark_refine.py #Quick refine the dark structure to produce the dark.pdb and refine.mtz (phases) files
4.DED_map.py     # Difference electron dentsity maps prepration using the files FOBS_dark.mtz, FOBS_timepoint.mtz, dark.pdb and refine.mtz

Prerequisites: 
1. Make sure the shell enviornement can access the CCP4 program and python.
2. Preprocessed hkl files (ex: dark_start.hkl and 1ps_start.hkl) for generating the structure factor files (ex: FOBS_dark.mtz and FOBS_1ps) 
Note: In this process, the text lines in the hkl file generated from the CrystFEL processing will be removed. Then the hkl files will be used to generate structure factor files using the program dark.py or light.py.
3. Refined dark.pdb and phases (ex: dark_phases.mtz). 

Hands on commands and steps

git clone 

Step 1: Create a directoty named "dark". Keep the dark_start.hkl and copy the dark.py to that directory.
Execute the dark.py python program to generate FOBS_dark.

Step 2: Create a directory named "light" and a subdirectory "hkl". Copy the light.py into the light directory.
Execute the light.py python program to generate the FOBS_light (ex: FOBS_1ps).

Step 3: Create a directory named "DED_maps". Copy the dark and light mtz files from step 1 and step2.
In addition, copy the dark_phases.mtz. Execute the DED_map.py program to get the map.

DED_map.py is a python program to generate difference electron density from light and dark datasets.
The map calculation is based on k-weight parameter and according to the reference --Ren et al., 1999.
This approach is similar to the Elin et al., 2020, Elife.

