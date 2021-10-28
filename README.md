# AutonomSH
Autonomous tool for handling the creation and numerical setup of a shaped hole case for LES simultion
This whole set of codes are created to autonomously handle the setup of a numerical case for shaped film cooling hole geometry
We have to concern ourselves mainly with the MESH folder wherein the following things are done automatically in a chain:
 - CAD hole goeometry creation using CFD-GEOM
 - Computational domain creation using CFD-GEOM
 - Mesh sources creation in CENTAUR
 - Mesh generation in CENTAUR
 - AsciiBound creation
 - Initialization of the solution with initial prediction
 - Setup of current case for RUN

all this is done by launching the generate.py in MESH folder

CAUTION:
1. Do load the cfd-geom module before launching the case
2. Run on visu terminal or likewise cause cfd-geom runs there
3. There are certain limitations which are discussed in depth in MESH folder
4. Don't forget to drink water

Good Luck,
Shan
