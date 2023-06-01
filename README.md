# GameSFX
A set of python utilities for SFX dataset processing.
Part 1: Beamtime difference electron density map making

In this part we have three python programs dark.py, light.py and DED.py
Prerequisites: 
1. Make sure the shell enviornement can access the CCP4 program and python.
2. Preprocessed hkl files (ex: dark_start.hkl and 1ps_start.hkl) for generating the structure factor files (ex: FOBS_dark.mtz and FOBS_1ps) 
Note: In this process, the text lines in the hkl file generated from the CrystFEL processing will be removed. Then the hkl files will be used to generate structure factor files.
3. Refined dark.pdb and phases (ex: dark_phases.mtz). These files can be generated after 2.

Step 1: Create a directoty named "dark". Keep the dark_start.hkl and copy the   



 is a diff.py is a python program to generate difference electron density from light and dark datasets.
The map calculation is based on k-weight parameter and according to the reference --Ren et al., 1999.


