import os
import math
import json
import time

# Here we calculate arithmetically the lcoation of the points defining the comuptational domain and the shaped hole
# This is a bunch of trignometric and other relations which can be solved via pen paper for more interested ones (It works here)
# The intereting part is the curvature of the hole sides and to be able to do it in CFD-GEOM, it's done at last

#SEE SEE SEE !!!!! 
scale = 1000
#the parameter values are scaled up by a factor of 10 so that centaur can read it nicely
#for all geometries the constant parameters are
#d       = 0.00035*scale         #diameter
#ep      = 0.0008*scale          #epaisseur de paroi
#rf	= 0.000175*scale	#fillet radius

default = 0

if default == 0:
   # Input from points.choices
   with open('./point.json', 'r') as fd:
       data = json.load(fd)
   for params in data['params']: 
    d   = params['d']*scale
    ep  = params['ep']*scale
    rf  = params['rf']*scale
    alpha   = params['alpha']
    betafwd = params['betafwd']
    betalat = params['betalat']
    e = params['e']*scale

if default == 1:
   # Input from space.json
   with open('../batman-coupling/space.json', 'r') as fd:
       params = json.load(fd)
   print('Geometrical parameters: ', params)
   alpha   = params['alpha'][0][0]
   betafwd = params['betafwd'][0][0]
   betalat = params['betalat'][0][0]
   e = params['e'][0][0]*scale

print (d,ep,rf,alpha,betafwd,betalat,e)

#write the part, IF NEEDED, that if you change the alpha, the overall ldd remains the same

#elif default == 0:
#   alpha   = 50.0		#angle of inclination
#   betafwd = 25.0		#forward expansion in degrees
#   betalat = 25.0		#lateral expansion in degrees
#   e	   = 0.00035*scale 		#profendeur

#origin is at (0,0)
#calculaint all necessary angles cosines and sines
cosalp     = math.cos(math.radians(alpha))
sinalp     = math.sin(math.radians(alpha))
cosbetfwd  = math.cos(math.radians(betafwd))
sinbetfwd  = math.sin(math.radians(betafwd))
cosbetlat  = math.cos(math.radians(betalat))
sinbetlat  = math.sin(math.radians(betalat))
cosalpbetf = math.cos(math.radians(alpha-betafwd))
sinalpbetf = math.sin(math.radians(alpha-betafwd))

#printing details then all parameters = 1, ptherwide as 0
ch = 0

print("\n ********** Beginning Coordinate Calculation for Geometry ********** \n")

##########################################################################
#calculate the rest variables

lmd     = (d*cosalp/(2*sinalp) + (ep-e)/sinalp)/d               #for circular section
lfwdd   = (e/sinalp - d*cosalp/(2*sinalp))/d                    #shaped section
ldd     = lmd + lfwdd                                           #overall length
rfd	= rf/d

if (ch==1):
   print(lmd,lfwdd,ldd)

##########################################################################
#centre of elipse in xz plane and major and minor axis length
#make ellipse using the centre and the major and minor axis locations

ex   = -1*(ldd*d)*cosalp
ey   =  0.0
ez   = -1*(ldd*d)*sinalp
emaj = d/(2.0*sinalp)	#this wil be calculated using cos(90-alpha) which is same as sinalp
emin = d/2.0

##########################################################################
#print ellipse points

print (" Cordinate calculation for ellipse done !! \n")
if ch == 1:
   print("Ellipse Centre : ", ex,ey,ez)
   print("Ellipse major and minor axis respectively",emaj,emin)

##########################################################################
#centre of circle in the xz plane 
cx   = -1*(lfwdd*d)*cosalp
cy   =  0.0
cz   = -1*(lfwdd*d)*sinalp

#calculate four points around the circle
# the 2nd and fourth point are calculated with reference to the centre and the distance of the centre from these points
#take special care if it is cosine or sine in the x and z direction and of alpha or 90-alpha
# finally make two arcs: one with points 1 2 3 and the second with points 3 4 1 

c1x = cx - d/2*sinalp
c1y = cy
c1z = cz + d/2*cosalp

c3x = cx
c3y = cy + d/2
c3z = cz

c2x = cx + d/2*sinalp
c2y = cy
c2z = cz - d/2*cosalp

c4x = cx
c4y = cy - d/2
c4z = cz

##########################################################################
#print coordinates of all construction points

print (" Cordinate calculation for circle done !! \n")
if ch == 1:
   print("Circle Centre  : ", cx,cy,cz)
   print("Circle point 1 : ",c1x,c1y,c1z)
   print("Circle point 2 : ",c2x,c2y,c2z)
   print("Circle point 3 : ",c3x,c3y,c3z)
   print("Circle point 4 : ",c4x,c4y,c4z)

##########################################################################
#slope check

slopel1 = (cz-ez)/(cx-ex)
slopel2 = (c1z-ez)/(c1x-ex+emaj)
if ch == 1:
   print("\n")
   print( slopel1,slopel2)
if slopel1 == slopel2:
   print(" \n Slopes verified and same !! Proceed to next step \n")
else:
      print(" Slopes not equal !! Problem exiting !!")

##########################################################################
#calculation of parameters for the shape on the top

#the left most line meets the xy plane
px1 = -1*d/(2*sinalp)
py1 = 0.0
pz1 = 0.0

#when the laterally expanded line meets the x axis
px2 = d/(2.0*sinalp) + (lfwdd*d + d*cosalp/2.0/sinalp)*sinbetfwd/sinalpbetf
py2 = py1
pz2 = 0.0

#centre of trapezoid
px3 = px2*cosalp*cosalp
py3 = 0.0
pz3 = px2*cosalp*sinalp

#top left centre point of the trapezoid
px4 = px3 - d*sinalp/2.0
py4 = py3
pz4 = pz3 + d*cosalp/2.0

#calculating the corner points of two lines at the x plane
#A,L1 correspond to smaller length, and hence pc1 and pc2 are two corner points of smaller length side
#corresponding understanding for B, L2, pc3 and pc4
A    = lfwdd*d - (d/2.0)/(sinalp/cosalp)
B    = (lfwdd*d + (d/2.0)/(sinalp/cosalp))*cosbetfwd + ((lfwdd*d + (d/2.0)/(sinalp/cosalp))*sinbetfwd)*cosalpbetf/sinalpbetf
l1   = A*math.tan(math.radians(betalat))+d/2.0
l2   = B*math.tan(math.radians(betalat))+d/2.0

#reduce also from the sides in the ratio of length multiplied by filet radius of r/d 0.5
#pyc11/22 are the extrme corner points and then the new points are calculated bu subtracting 0.5rd from both ends in respective proportions
pxc1  = px1 
pyc11 = py1 + l1
pyc1  = pyc11 - rfd*d*l1/l2
pzc1  = 0.0

pxc2  = px1
pyc22 = py1 - l1
pyc2  = pyc22 + rfd*d*l1/l2
pzc2  = 0.0

#simimarly for the larger length points
pxc3  = px2
pyc33 = py2 + l2
pyc3  = pyc33 - rfd*d
pzc3  = 0.0

pxc4  = px2
pyc44 = py2 - l2 
pyc4  = pyc44 + rfd*d
pzc4  = 0.0

#we need four more points of the opposite line, now calculating those before doing the curve option
m1   = (pyc33-pyc11)/(pxc3-pxc1)	#slope of the first line
df    = rfd*d#/cosalp			#distance in actual after projection, assumed using simple trignometry
f    = df/((1+m1**2)**0.5)

pxc5 = pxc1 + f  
pyc5 = m1*(pxc5-pxc1) + pyc11
pzc5 = 0.0

pxc7 = pxc3 - f
pyc7 = m1*(pxc7 - pxc3) + pyc33 
pzc7 = 0.0

pxc6 = pxc5
pyc6 = -1*pyc5
pzc6 = 0.0

pxc8 = pxc7
pyc8 = -1*pyc7
pzc8 = 0.0

##########################################################################
#print coordinates of all construction points of the top trapezoid

print ("\n Cordinate calculation for trapezoid done !! \n")
if ch == 1:
   print("Trap corner point 1 : ",pxc1,pyc1,pzc1)
   print("Trap corner point 2 : ",pxc2,pyc2,pzc2)
   print("Trap corner point 3 : ",pxc3,pyc3,pzc3)
   print("Trap corner point 4 : ",pxc4,pyc4,pzc4)
   print("Trap corner point 5 : ",pxc5,pyc5,pzc5)
   print("Trap corner point 6 : ",pxc6,pyc6,pzc6)
   print("Trap corner point 7 : ",pxc7,pyc7,pzc7)
   print("Trap corner point 8 : ",pxc8,pyc8,pzc8)
   print("Trap point 1 : ",px1,py1,pz1)
   print("Trap point 2 : ",px2,py2,pz2)
   #print("Trap point 3 : ",px3,py3,pz3)
   #print("Trap point 4 : ",px4,py4,pz4)

##########################################################################

print(" ************* Done Coordinate Calculation for Geometry ************ \n")

##########################################################################
#write the data to text files to be able to read later by geom-script.py

#f = open("pointsE.dat","w+")
#f.write("%.10f	%.10f	%.10f	%.10f  %.10f" % (ex,ey,ez,emaj,emin))
#f.close()
#if det == 1:
#  print("Written file pointsE")
#
#f = open("pointsC.dat","w+")  
#f.write("%.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f" % (c1x,c1y,c1z,c2x,c2y,c2z,c3x,c3y,c3z,c4x,c4y,c4z))
#f.close()
#if det == 1:
#  print("Written file pointsC")
#
#f = open("pointsP14.dat","w+")
#f.write("%.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f" % (pxc1,pyc1,pzc1,pxc2,pyc2,pzc2,pxc3,pyc3,pzc3,pxc4,pyc4,pzc4))
#f.close()
#if det == 1:
#  print("Written file pointsP14")
#
#f = open("pointsP58.dat","w+")
#f.write("%.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f  %.10f" % (pxc5,pyc5,pzc5,pxc6,pyc6,pzc6, pxc7,pyc7,pzc7, pxc8,pyc8,pzc8))
#f.close()
#if det == 1:
#  print("Written file pointsP58")
#
#f = open("pointsP12.dat","w+")
#f.write("%.10f	%.10f	%.10f	%.10f	%.10f	%.10f" % (px1,py1,pz1,px2,py2,pz2))
#f.close()
#if det == 1:
#  print("Written file pointsP12")

##########################################################################
