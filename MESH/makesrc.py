import os
import time
import json
#import numpy as np

# this script automatically generates the sources in the regions of interest on the domain
# the paramter meshparam will change the refinement in the sources and increase or decrease the mesh size
# this parameter is an input in the enterpoints.py
execfile("parameterCalc.py")

f = open("opt.src","w+")
f.write("1")

#for 0.05 there are 10 points per diameter
#mf = 0.05
with open('./point.json', 'r') as fd:
    datam = json.load(fd)
for params in datam['params']:
    mf = params['meshparam']

#source1
#hole cylindrical part
ex1 = ex - emaj
f.write("\nSTARTGEOMSOURCE\n\"HoleCircle\" CYLINDER\n")
f.write("0.3 0\n")			#OuterInnerRadius
f.write("%f 0 %f\n"%(cx,cz))		#point1
f.write("%f 0 %f\n"%(ex1,ez))		#point2
f.write("Surface ABSOLUTE %f\n"%mf)	#SurfaceMeshValue
f.write("Tetra ABSOLUTE %f\n"%mf)	#TetraMeshValue
f.write("ENDGEOMSOURCE")

#source2
#hole expanded part
f.write("\nSTARTGEOMSOURCE\n\"HoleTrap\" HEXAHEDRON\n")
f.write("%f %f 0\n"%(pxc1-0.1, pyc11+0.1))           #point1 
f.write("%f %f 0\n"%(pxc2-0.1, pyc22-0.1))           #point2 
f.write("%f %f 0\n"%(pxc3+0.1, pyc33+0.1))           #point3
f.write("%f %f 0\n"%(pxc4+0.1, pyc44-0.1))           #point4
f.write("%f %f %f\n"%((c1x-0.1),(c1y+d/2),(c1z)))            #point5
f.write("%f %f %f\n"%((c1x-0.1),(c1y-d/2),(c1z)))            #point6
f.write("%f %f %f\n"%((c2x),(c2y+d/2),(c2z-0.1)))            #point7
f.write("%f %f %f\n"%((c2x),(c2y-d/2),(c2z-0.1)))            #point8
f.write("Surface ABSOLUTE %f\n"%mf)     #SurfaceMeshValue
f.write("Tetra ABSOLUTE %f\n"%mf)       #TetraMeshValue
f.write("ENDGEOMSOURCE")

#source3
#source in domain above the hole
f.write("\nSTARTGEOMSOURCE\n\"DomainOnHole\" HEXAHEDRON\n")
f.write("%f %f -0.1\n"%(pxc1-0.5, pyc11+0.5))           #point1 
f.write("%f %f -0.1\n"%(pxc2-0.5, pyc22-0.5))           #point2 
f.write("%f %f -0.1\n"%(pxc3+0.75, pyc33+0.75))           #point3
f.write("%f %f -0.1\n"%(pxc4+0.75, pyc44-0.75))           #point4
f.write("%f %f 0.5\n"%(pxc1-0.5, pyc11+0.5))           #point5 
f.write("%f %f 0.5\n"%(pxc2-0.5, pyc22-0.5))           #point6 
f.write("%f %f 1\n"%(pxc3+0.75, pyc33+0.75))         #point7
f.write("%f %f 1\n"%(pxc4+0.75, pyc44-0.75))         #point8
f.write("Surface TRILINEAR %f %f %f %f %f %f %f %f \n"%(mf,mf,mf,mf,mf,mf,mf,mf)) #SurfaceMeshValue
f.write("Tetra TRILINEAR %f %f %f %f %f %f %f %f \n"%(mf,mf,mf,mf,mf,mf,mf,mf))   #TetraMeshValue
f.write("ENDGEOMSOURCE")

#source4
#source in domain after the hole
#extends two time the length of the hole in x direction, also height is increased
f.write("\nSTARTGEOMSOURCE\n\"DomainAftHole\" RECTANGLE\n")
f.write("%f %f -0.1\n"%(pxc4+0.5, pyc44-0.75))           #point1
f.write("%f %f 1.5\n"%((pxc3-pxc2)*5, pyc33+0.75))       #point2
f.write("Surface TRILINEAR %f %f %f %f %f %f %f %f \n"%(mf,mf,mf,mf,mf,mf,mf,mf)) #SurfaceMeshValue
f.write("Tetra TRILINEAR %f %f %f %f %f %f %f %f \n"%(mf,mf,mf,mf,mf,mf,mf,mf))   #TetraMeshValue
f.write("ENDGEOMSOURCE")

#if the next source is going out of the domain, then cut it till the end onmly
xlimit1 = (pxc3-pxc2)*5
xlimit2 = (pxc3-pxc2)*10
if (xlimit2 > 18):
  xlimit2 = 18
#source5
#source in domain after source4
#extends almost till the end of the domain where flow leaves
if (xlimit1 < 18):  
  f.write("\nSTARTGEOMSOURCE\n\"DomainAftHole2\" RECTANGLE\n")
  f.write("%f %f -0.1\n"%((pxc3-pxc2)*5, pyc44-1.0))         #point1
  f.write("%f %f 2\n"%(xlimit2, pyc33+1.0))             #point2
  f.write("Surface TRILINEAR %f %f %f %f %f %f %f %f \n"%(mf,mf*1.5,mf,mf*1.5,mf,mf*1.5,mf,mf*1.5)) #SurfaceMeshValue
  f.write("Tetra TRILINEAR %f %f %f %f %f %f %f %f \n"%(mf,mf*1.5,mf,mf*1.5,mf,mf*1.5,mf,mf*1.5))   #TetraMeshValue
  f.write("ENDGEOMSOURCE")

#extra source till end of the domain, no height increased, just extend till end. 
# DO NOT CREATE THIS SOURCE IF THE ABOVE SOURCE ALREADY EXTENDS TILL THE END	 
ex = (pxc3-pxc2)*10
if ( ex < 18.0 ):
  #sourceExtra
  #source in domain after source5
  #extends till the end of the domain where flow leaves
  f.write("\nSTARTGEOMSOURCE\n\"DomainEnd\" RECTANGLE\n")
  f.write("%f %f -0.1\n"%((pxc3-pxc2)*10, pyc44-1.0))         #point1
  f.write("%f %f 2\n"%(18.0, pyc33+1.0))             #point2
  f.write("Surface TRILINEAR %f %f %f %f %f %f %f %f \n"%(mf*1.5,mf*2,mf*1.5,mf*2,mf*1.5,mf*2,mf*1.5,mf*2)) #SurfaceMeshValue
  f.write("Tetra TRILINEAR %f %f %f %f %f %f %f %f \n"%(mf*1.5,mf*2,mf*1.5,mf*2,mf*1.5,mf*2,mf*1.5,mf*2))   #TetraMeshValue
  f.write("ENDGEOMSOURCE")

#source6
#source in domain before hole
f.write("\nSTARTGEOMSOURCE\n\"DomainBefHole\" RECTANGLE\n")
f.write("%f %f -0.1\n"%(-10*d, pyc44-0.1))            #point1
f.write("%f %f 0.5\n"%(pxc1, pyc33+0.1))       #point2
f.write("Surface TRILINEAR %f %f %f %f %f %f %f %f \n"%(mf,mf,mf,mf,mf,mf,mf,mf))    #SurfaceMeshValue
f.write("Tetra TRILINEAR %f %f %f %f %f %f %f %f \n"%(mf,mf,mf,mf,mf,mf,mf,mf))      #TetraMeshValue
f.write("ENDGEOMSOURCE")

#source
#plenum entry
f.write("\nSTARTGEOMSOURCE\n\"PlenumHoleEntry\" HEXAHEDRON\n")
f.write("-2.0 1.25 -0.7\n")		#point1
f.write("-2.0 -1.25 -0.7\n")		#point2
f.write("-2.5 1.5 -2.5\n")			#point3
f.write("-2.5 -1.5 -2.5\n")			#point4
f.write("1.0 1.25 -0.7\n")		#point5
f.write("1.0 -1.25 -0.7\n")		#point6
f.write("1.5 1.5 -2.5\n")			#point7
f.write("1.5 -1.5 -2.5\n")			#point8
f.write("Surface TRILINEAR %f %f %f %f %f %f %f %f \n"%(mf,mf,mf*2,mf*2,mf,mf,mf*2,mf*2))    #SurfaceMeshValue
f.write("Tetra TRILINEAR %f %f %f %f %f %f %f %f \n"%(mf,mf,mf*2,mf*2,mf,mf,mf*2,mf*2))      #TetraMeshValue
f.write("ENDGEOMSOURCE")

f.close()

