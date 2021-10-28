"""The main script to be launched which then handles the autonomous numerical setup"""
import os
import time
import json

#with open('../batman-coupling/space.json', 'r') as fd:
#    params = json.load(fd)

path = os.getcwd()

print('\n ***************** Creating CAD ***************** \n')

os.system("python enterpoints.py")

os.system("module load visu/cfdgeom/2016.0")

while 'CAD creation':
    os.system("CFD-GEOM -runver 2016.0 -script geom_script.py")
          
    if not os.path.isfile("TestHole.igs"):
        time.sleep(2)
    else:
        break

print('\n ---------------- CAD Creation Done ----------------- \n')

print('\n ***************** Creating Mesh ***************** \n')

os.system("python makesrc.py")
print('\n ---------------- Source Creation Done ----------------- \n')
os.chdir("./Centaur")
#os.system("cp savedfiles/* .")
os.system("python copysource.py")
os.system("centaur -nox centaur.list")

print('\n ---------------- Mesh Creation Done ----------------- \n')
os.chdir(path)

print('\n ***************** Mesh Treatment - HIP ***************** \n')

os.chdir(path)
os.system("cp Centaur/opt.hyb .")
os.system("/data/home/cfd/rolex/HIP/latest/hip-latest centaurhip.script")

print('\n ---------------- Mesh Treatment Done ----------------- \n')
os.system("cp savedAsciiBound/* .")

print(' ***************** ***************** ***************** ')
print(' CAD and the corresponding Mesh successfully generated ')
print(' ***************** ***************** ***************** \n')

print(' ***************** interpolation ***************** ')
os.system("cp opt.mesh.h5 ./interpMesh/.")
os.chdir("./interpMesh")
os.system("/data/home/cfd/rolex/HIP/latest/hip-latest scriptInterp")
os.system("cp interp_opt.sol.h5 ../../RUN/currentSOLUT/.")
os.chdir("../../RUN/currentSOLUT")
os.system("ln -sf interp_opt.sol.h5 linked.h5")
#print(' ***************** solutbound ***************** ')
#os.chdir("../../SOLUTBOUND")
#os.system("gensolutbound --step2 --dir=../RUN")
print(' ***************** ***************** ***************** ')
print(' ***************** ***** DONE! ***** *****************')
print(' ***************** ***************** ***************** \n')

