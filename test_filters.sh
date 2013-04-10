#!/bin/bash

set -o xtrace

# Folder

python ofexport.py -o tmp/fi.tp --fi 'Work'
python ofexport.py -o tmp/fe.tp --fe 'Work'

# Project

python ofexport.py -o tmp/pi.tp --pi 'Work'
python ofexport.py -o tmp/pe.tp --pi 'Work'

python ofexport.py -o tmp/pci.tp --fi 'Work' --pci none
python ofexport.py -o tmp/pce.tp --fi 'Work' --pce none

python ofexport.py -o tmp/pdi.tp --fi 'Work' --pdi none
python ofexport.py -o tmp/pde.tp --fi 'Work' --pde none

python ofexport.py -o tmp/psi.tp --fi 'Work' --psi none
python ofexport.py -o tmp/pse.tp --fi 'Work' --pse none

python ofexport.py -o tmp/pfi.tp --fi 'Work' --pfi none
python ofexport.py -o tmp/pfe.tp --fi 'Work' --pfe none

# Task

python ofexport.py -o tmp/ti.tp --pi 'Work'
python ofexport.py -o tmp/te.tp --pi 'Work'

python ofexport.py -o tmp/tci.tp --fi 'Work' --tci none
python ofexport.py -o tmp/tce.tp --fi 'Work' --tce none

python ofexport.py -o tmp/tdi.tp --fi 'Work' --tdi none
python ofexport.py -o tmp/tde.tp --fi 'Work' --tde none

python ofexport.py -o tmp/tsi.tp --fi 'Work' --tsi none
python ofexport.py -o tmp/tse.tp --fi 'Work' --tse none

python ofexport.py -o tmp/tfi.tp --fi 'Work' --tfi none
python ofexport.py -o tmp/tfe.tp --fi 'Work' --tfe none