# GameSFX "Data analyis for dummies"
A set of python utilities for serial femtosecond crystallography data analysis. The required tools are Python, editors (whatever the editor you like!!) and CCP4/Phenix. For map visualization "coot". 

Take home message: Classical interactive computing with less mousing and more keyboarding!!!


A XFEL data analysis tutorial using Python programs

Abstract

This tutorial is based on the reported literatiure. (Pandey et al., 2020) The direct hkl files (dark and light) from the CrystFEL will be prepared to convert intensities to structure factors (my scripts). Then this file will be used to prepare difference electron density (DED) maps which are based on the Bayesian statistical analysis and are called Q-weighed electron difference density maps. (Ursby and Bourgeios; Terwilliger and Berendzen). Further, the extrapolated maps will be generated to refine the light activated model. Then the refined light model will be used to generate the calculated DED map. Finally, the map-to-map correlation (local region not whole map) using Pearson Correlation Coefficient (PCC) will be used to compare the region of excitation between the observed and calculated maps. 

## Part 1: Beamtime maps: Difference electron density map plotting using python programs.
The 1ps data used for the demo purpose is from the https://doi.org/10.7554/eLife.53514

### Install GameSFX
git clone git@github.com:madanmx/GameSFX.git \
or                                                     \
click on 'Code', then click on 'Download ZIP"          \

In this part 1 we have three plus one python programs: \
1.dark.py         #Prepare the structure factors from hkl i.e., dark.mtz  \
2.light.py        #Prepare the structure factors from hkl i.e., timepoint.mtz (ex: 1ps.mtz) \
3.dark_refine.py  #Quick refine the dark structure to produce the dark.pdb and dark_phases.mtz  files \
4.DED_map.py      #Difference electron dentsity maps prepration using the files; dark.mtz, timepoint.mtz, dark.pdb and dark_phases.mtz

### Hands on commands and explaination
#### 1.Clone and browse the GameSFX
command-prompt$git clone git@github.com:madanmx/GameSFX.git #This creates a directory with the name GameSFX \
command-prompt$cd GameSFX                                    #Change directory to the GameSFX               \
command-prompt$ls                                            #list the files and directory present          \
DED_map                                                                                                     \
LICENSE                                                                                                      \
README.md                                                                                                    \
dark                                                                                                         \ 
dark_refine                                                                                                  \
light                                                                                                        \

#### 2.Prepare dark.mtz
command-prompt$cd dark                                       #change directory to the dark folder           \
command-prompt$ls                                            #list the files                                \
dark.py                                                                                                      \
command-prompt$cp /path/dark_crystfel.hkl .                  #copy the dark hkl file directly outout from crystFEL \
command-prompt$ls                                            #list the files                                \
dark.py            
dark_crystfel.hkl  
command-prompt$vi dark_crystfel.hkl                          #edit the dark_crystfel.hkl using any editor. Here for example I will use vi editor. \

  CrystFEL reflection list version 2.0                                \
  Symmetry: mmm                                                       \
   h    k    l          I    phase   sigma(I)   nmeas                 \
   0    0    4   30476.13        -   10561.76      15                 \
   0    0    5     -88.01        -      66.08      51                 \   
   0    0    6    6769.51        -    1836.28      62                 \
   0    0    7      49.19        -      51.63      54                 \
  .                                                                   \
  .                                                                   \
  .                                                                   \
  .                                                                   \
  .                                                                   \
  .                                                                   \
  29    1    2      18.66        -      46.57       2                 \     
  End of reflections                                                  \
  
In the editor, delete the first three lines and the last line in dark_crystfel.hkl file (make sure no chractercters exist) and save it as dark_start.hkl. NOTE: Make sure there is "NO" empty line in the starting of the file for example the first line should start with the  0    0    4   30476.13        -   10561.76      15 as in the above example  \
command-prompt$ls                                            #list the files  \
dark.py                                                                       \
dark_crystfel.hkl                                                             \
dark_start.hkl                                                                \
command-prompt$./dark.py  #After preparing the dark_start.hkl file execute this command and the relevant details prompted by this code. The details include No. of residues, cell parameters, space group, resolution,... This will generate several files out of which dark.mtz is the final file required to prepare DED map.
After this go back to the previous directory with the path /path/GameSFX 

#### Quick dark structure refinement
command-prompt$cd dark_refine              #change directory to the dark_refine   \
command-prompt$ls                          #list the files and directory          \
dark_refine.py
Make sure you have all the relevant input files before executing this python code. \
1. dark_start.pdb                                                                  
2. dark.mtz
3. file.cif (ex:LBV.cif)
copy above files to this directory and use ls to see all the files are there       \
command-prompt$ls                          #list the files and directory           \
dark_start.pdb                                                                     \
dark.mtz                                                                           \
LBV.cif                                                                            \   
dark_refine.py                                                                     \ 
command-prompt$./dark_refine.py            #Start the dark structure refinement to generate the dark_phases.mtz and dark.pdb file. \
This will asks to names of pdb and cif file (ex: enter dark if it is dark.pdb and LBV if it is LBV.cif) \
Also enter the maximum and minimum resolution                                     \
command-prompt$ls                          #list the files and directory
dark_start.pdb                                                                     \
dark.mtz                                                                           \
LBV.cif                                                                            \   
dark_refine.py                                                                     \
dark.pdb                                                                           \
dark_phases.mtz                                                                    \
After this go back to the previous directory with the path /path/GameSFX           \ 

#### Prepare timepoint.mtz  
command-prompt$cd light                            #change directory to light directory \
command-prompt$ls                                  #list the files and directory        \
light.py                                                                                \  
command-prompt$mkdir hkl                           #make directory called hkl           \
command-prompt$ls                                  #list the files and directory        \
light.py                                                                                \
hkl                                                                                     \
command-prompt$cd hkl                              #change directory to the hkl         \
command-prompt$cp /path/timepoint_crystfel.hkl .   #copy the crystfel processed timepoint.hkl files to this folder (ex:1ps_crystfel.hkl)  \
In the editor preprocess the 1ps_crystfel.hkl similar to dark_crystfel.hkl file. Then save it as 1ps.hkl.                                 \
command-prompt$ls                                 #list the files within the /hkl/ directory                                                    \  
1ps_crystfel.hkl                                                                                                                                \  
1ps.hkl                                  
NOTE: After the above step, remove the 1ps_crystfel.hkl and keep only the 1ps_start.hkl file. 
command-prompt$cd ..                               #change directory to the /light/                                                               \
command-prompt$./light.py 1ps                      #Execute this command to prepare 1ps.mtz ignore/view the other files. After this go bact to the previous directory with the path /path/GameSFX 

#### 5.DED map plotting

DED_map.py is a python program to generate difference electron density from light and dark datasets. \
Copy dark.mtz, 1ps.mtz, dark.pdb and dark_phases.mtz files into DED_map directory.                   \
command-prompt$cd DED_map                                                                            \
command-prompt$DED_map.py 1ps     #Enter all the values required by this code to generate a 1ps directory. The 1ps.map (DED map) and other relevant files will be found in this directory. \
Open the coot, load the dark.pdb and 1ps.map to see the difference electron density features.


# Many programs for the SFX data (Part 2; Extrapolated maps, Part 3: Pearson Correlation coefficent....)
Work in Progess!!

# License
The programs in GameSFX are published under the GNU General Public License v3.0. Please do take responsibility to install all the relevant pacakges (CCP4 and coot) to work with the GameSFX.

see http://www.gnu.org/licenses/ for more information.

# Acknowledgments
Sebastian Westenhoff for sharing the 1ps data from https://doi.org/10.7554/eLife.53514 and for providing postdoctoral scholarship.


# Contact
Madan Kumar Shankar - madan.shankar@kemi.uu.se
Department of Chemistry BMC-Biochemistry
Uppsala University

