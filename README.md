# GameSFX
A set of python utilities for SFX dataset processing.
Part 1: Beamtime difference electron density map making

In this part we have three python programs dark.py, light.py and DED.py
Prerequisites: 
1. Make sure the shell enviornement can access the CCP4 program and python.
2. Preprocessed hkl files (ex: dark_start.hkl and 1ps_start.hkl) for generating the structure factor files (ex: FOBS_dark.mtz and FOBS_1ps) 
Note: In this process, the text lines in the hkl file generated from the CrystFEL processing will be removed. Then the hkl files will be used to generate structure factor files.
3. Refined dark.pdb and phases (ex: dark_phases.mtz). These files can be generated after 2.

Step 1: Create a directoty named "dark". Keep the dark_start.hkl and copy the dark.py to that directory.
Execute the dark.py python program to generate FOBS_dark.

Step 2: Create a directory named "light" and a subdirectory "hkl". Copy the light.py into the light directory.
Execute the light.py python program to generate the FOBS_light (ex: FOBS_1ps).

Step 3: Create a directory named "DED_maps". Copy the dark and light mtz files from step 1 and step2.
In addition, copy the dark_phases.mtz. Execute the DED.py program to get the map.

DED.py is a python program to generate difference electron density from light and dark datasets.
The map calculation is based on k-weight parameter and according to the reference --Ren et al., 1999.


