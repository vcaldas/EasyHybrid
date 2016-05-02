#!/bin/bash

# . Bash environment variables and paths to be added to a user's ".bash_profile" file.
# . Some of these values may need modifying (e.g. PEPDICE_SCRATCH and PYTHONPATH).

# . The root of the program.
#/home/fernando/programs/EasyMol/installation

EASYMOL_ROOT=$HOME/programs/EasyHybrid/ ; export EASYMOL_ROOT

# . Package paths.
EASYMOL_BABEL=$EASYMOL_ROOT/pyBabel                         ; export EASYMOL_BABEL           
EASYMOL_CORE=$EASYMOL_ROOT/pyEasyCore                       ; export EASYMOL_CORE            


# . Additional paths.
#PEPDICE_PARAMETERS=$PEPDICE_ROOT/Parameters                                   ; export PEPDICE_PARAMETERS
#PEPDICE_SCRATCH=$PEPDICE_ROOT/scratch                                         ; export PEPDICE_SCRATCH   
#PEPDICE_STYLE=$PEPDICE_PARAMETERS/ccsStyleSheets/defaultStyle.css ; export PEPDICE_STYLE     

# . The python path.
PYTHONPATH=$PYTHONPATH:$EASYMOL_ROOT/pyBabel:$EASYMOL_ROOT/pyEasyCore ; export PYTHONPATH
