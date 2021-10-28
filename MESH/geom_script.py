# This file was journaled by CFD-GEOM
import GUtils
import GGeometry
import GMesh
import GFileIO
import GBCVC

#this script calls a script for calculating point coordinates which define the computational domain and it's parts
execfile("parameterCalc.py")

#ex,ey,ez,emaj,emin = np.loadtxt('pointsC.dat', usecols = (0,1,2,3,4), unpack=True, skiprows=0)
#c1x,c1y,c1z,c2x,c2y,c2z,c3x,c3y,c3z,c4x,c4y,c4z = np.loadtxt('pointsP14.dat', usecols = (0,1,2,3,4,5,6,7,8,9,10,11), unpack=True, skiprows=0)
#pxc1,pyc1,pzc1,pxc2,pyc2,pzc2,pxc3,pyc3,pzc3,pxc4,pyc4,pzc4 = np.loadtxt('pointsP14.dat', usecols = (0,1,2,3,4,5,6,7,8,9,10,11), unpack=True, skiprows=0)
#pxc5,pyc5,pzc5,pxc6,pyc6,pzc6, pxc7,pyc7,pzc7, pxc8,pyc8,pzc8 = np.loadtxt('pointsP58.dat', usecols = (0,1,2,3,4,5,6,7,8,9,10,11), unpack=True, skiprows=0)
#px1,py1,pz1,px2,py2,pz2 = np.loadtxt('pointsP12.dat', usecols = (0,1,2,3,4,5), unpack=True, skiprows=0)

##########################################################################
# To launch : CFD-GEOM -script filename.py

GUtils.StartGeom()

GUtils.SetUnits( 0 )

##########################################################################
#create the ellipse

geom_point1 = GGeometry.CreatePoint(ex,ey,ez)
geom_curve1 = GGeometry.CreateEllipse(geom_point1, emaj, emin, 180, 360)
geom_curve2 = GGeometry.CreateEllipse(geom_point1, emaj, emin,   0, 180)
GUtils.DeleteEntities( geom_point1 )

##########################################################################
#Create the middle circle

geom_point2 = GGeometry.CreatePoint(c1x,c1y,c1z)
geom_point3 = GGeometry.CreatePoint(c2x,c2y,c2z)
geom_point4 = GGeometry.CreatePoint(c3x,c3y,c3z)
geom_point5 = GGeometry.CreatePoint(c4x,c4y,c4z)
geom_curve3 = GGeometry.Create3PtArc(geom_point3, geom_point5, geom_point2)
geom_curve4 = GGeometry.Create3PtArc(geom_point3, geom_point4, geom_point2)

##########################################################################
#create the trapezoid, for description of points see parameter script

geom_point6 = GGeometry.CreatePoint(pxc1,pyc1,pzc1)
geom_point7 = GGeometry.CreatePoint(pxc2,pyc2,pzc2)
geom_point8 = GGeometry.CreatePoint(pxc3,pyc3,pzc3)
geom_point9 = GGeometry.CreatePoint(pxc4,pyc4,pzc4)
geom_point10 = GGeometry.CreatePoint(pxc5,pyc5,pzc5)
geom_point11 = GGeometry.CreatePoint(pxc6,pyc6,pzc6)
geom_point12 = GGeometry.CreatePoint(pxc7,pyc7,pzc7)
geom_point13 = GGeometry.CreatePoint(pxc8,pyc8,pzc8)
geom_point14 = GGeometry.CreatePoint(px1,py1,pz1)
geom_point15 = GGeometry.CreatePoint(px2,py2,pz2)

#connect the top trapezoid but not at the edges
geom_line1 = GGeometry.CreateLine( geom_point8, geom_point15 )
geom_line2 = GGeometry.CreateLine( geom_point15, geom_point9 )
geom_line3 = GGeometry.CreateLine( geom_point13, geom_point11 )
geom_line4 = GGeometry.CreateLine( geom_point7, geom_point14 )
geom_line5 = GGeometry.CreateLine( geom_point14, geom_point6 )
geom_line6 = GGeometry.CreateLine( geom_point10, geom_point12 )

#create blend curves to connect the corners in the calculated way
geom_curve5 = GGeometry.CreateBlendCurve(geom_line1, geom_point8, geom_line6, geom_point12)
geom_curve6 = GGeometry.CreateBlendCurve(geom_line2, geom_point9, geom_line3, geom_point13)
geom_curve7 = GGeometry.CreateBlendCurve(geom_line3, geom_point11, geom_line4, geom_point7)
geom_curve8 = GGeometry.CreateBlendCurve(geom_line5, geom_point6, geom_line6, geom_point10)

##########################################################################
#create cureves for connecting the ellipse, circle and the top trapezoid

geom_line7 = GGeometry.CreateLine( geom_curve1['points'][0], geom_point2 )
geom_line8 = GGeometry.CreateLine( geom_point2, geom_point14 )
geom_line9 = GGeometry.CreateLine( geom_curve1['points'][1], geom_point3 )
geom_line10 = GGeometry.CreateLine( geom_point3, geom_point15 )

##########################################################################
#create the four surfaces representing the shaped hole 

geom_surf5 = GGeometry.FitSurfaceThroughCurves([geom_curve3, geom_line7, geom_curve1, geom_line9])
geom_surf6 = GGeometry.FitSurfaceThroughCurves([geom_curve3, geom_line8, geom_curve7, geom_line3, geom_line4, geom_curve6, geom_line2, geom_line10])
geom_surf7 = GGeometry.FitSurfaceThroughCurves([geom_line8, geom_curve8, geom_line5, geom_line6, geom_curve5, geom_line1, geom_line10, geom_curve4])
geom_surf8 = GGeometry.FitSurfaceThroughCurves([geom_curve4, geom_line7, geom_curve2, geom_line9])


##########################################################################
#domain dimensions
#all dimensions are defined in terms of diameter
#the width is necessary for the extreme design points
#the height is negotiable
#the length after the hole is negotiable
d = 0.35
dlnx = -10*d
dlpx = 18
wd   = 12*d
dlhe = 20*d

##########################################################################
#the domain for the top part 
#the first six points define the dmain on the surface plane of the wall and next four points are the top wall surface

#domain extensions
dlnw = -0.5*wd
dlpw = 0.5*wd

geom_point17 = GGeometry.CreatePoint(dlnx, 0, 0)
geom_point18 = GGeometry.CreatePoint(dlnx, dlpw, 0)
geom_point19 = GGeometry.CreatePoint(dlnx, dlnw, 0)
geom_point20 = GGeometry.CreatePoint(dlpx, dlnw, 0)
geom_point21 = GGeometry.CreatePoint(dlpx, dlpw, 0)
geom_point22 = GGeometry.CreatePoint(dlpx, 0, 0)
geom_point23 = GGeometry.CreatePoint(dlpx, dlpw, dlhe)
geom_point24 = GGeometry.CreatePoint(dlpx, dlnw, dlhe)
geom_point25 = GGeometry.CreatePoint(dlnx, dlnw, dlhe)
geom_point26 = GGeometry.CreatePoint(dlnx, dlpw, dlhe)

geom_line11 = GGeometry.CreateLine( geom_point18, geom_point21 )
geom_line12 = GGeometry.CreateLine( geom_point19, geom_point20 )
geom_line13 = GGeometry.CreateLine( geom_point21, geom_point22 )
geom_line14 = GGeometry.CreateLine( geom_point22, geom_point20 )
geom_line15 = GGeometry.CreateLine( geom_point18, geom_point17 )
geom_line16 = GGeometry.CreateLine( geom_point17, geom_point19 )
geom_line17 = GGeometry.CreateLine( geom_point17, geom_point14 )
geom_line18 = GGeometry.CreateLine( geom_point15, geom_point22 )
geom_line19 = GGeometry.CreateLine( geom_point18, geom_point26 )
geom_line20 = GGeometry.CreateLine( geom_point19, geom_point25 )
geom_line21 = GGeometry.CreateLine( geom_point20, geom_point24 )
geom_line22 = GGeometry.CreateLine( geom_point21, geom_point23 )
geom_line23 = GGeometry.CreateLine( geom_point26, geom_point23 )
geom_line24 = GGeometry.CreateLine( geom_point25, geom_point24 )
geom_line25 = GGeometry.CreateLine( geom_point26, geom_point25 )
geom_line26 = GGeometry.CreateLine( geom_point23, geom_point24 )

geom_surf9  = GGeometry.FitSurfaceThroughCurves([geom_line6, geom_curve8, geom_curve5, geom_line5, geom_line1, geom_line18, geom_line17, geom_line15, geom_line11, geom_line13])
geom_surf10 = GGeometry.FitSurfaceThroughCurves([geom_line18, geom_line14, geom_line12, geom_line16, geom_line17, geom_line3, geom_curve6, geom_curve7, geom_line2, geom_line4])
geom_surf11 = GGeometry.FitSurfaceThroughCurves([geom_line20, geom_line25, geom_line19, geom_line15, geom_line16])
geom_surf12 = GGeometry.FitSurfaceThroughCurves([geom_line26, geom_line22, geom_line21, geom_line14, geom_line13])
geom_surf13 = GGeometry.FitSurfaceThroughCurves([geom_line24, geom_line21, geom_line12, geom_line20])
geom_surf14 = GGeometry.FitSurfaceThroughCurves([geom_line22, geom_line11, geom_line23, geom_line19])
geom_surf15 = GGeometry.FitSurfaceThroughCurves([geom_line23, geom_line24, geom_line25, geom_line26])

##########################################################################
#the plenum design on the bottom 
#same as before, first six points plane on surface, last four are the bottom plenum inlet

#plenum extensions
plnx = -10*d
plpx = 8*d
pldp = ez-10*d
wd = 10*d
plnw = -0.5*wd
plpw = 0.5*wd

geom_point27 = GGeometry.CreatePoint(plnx, 0, ez)
geom_point28 = GGeometry.CreatePoint(plnx, plpw, ez)
geom_point29 = GGeometry.CreatePoint(plnx, plnw, ez)
geom_point30 = GGeometry.CreatePoint(plpx, plnw, ez)
geom_point31 = GGeometry.CreatePoint(plpx, 0, ez)
geom_point32 = GGeometry.CreatePoint(plpx, plpw, ez)
geom_point33 = GGeometry.CreatePoint(plpx, plpw, pldp)
geom_point34 = GGeometry.CreatePoint(plpx, plnw, pldp)
geom_point35 = GGeometry.CreatePoint(plnx, plnw, pldp)
geom_point36 = GGeometry.CreatePoint(plnx, plpw, pldp)

geom_line27 = GGeometry.CreateLine( geom_point27, geom_curve1['points'][0] )
geom_line28 = GGeometry.CreateLine( geom_curve1['points'][1], geom_point31 )
geom_line29 = GGeometry.CreateLine( geom_point29, geom_point30 )
geom_line30 = GGeometry.CreateLine( geom_point31, geom_point30 )
geom_line31 = GGeometry.CreateLine( geom_point27, geom_point29 )
geom_line32 = GGeometry.CreateLine( geom_point27, geom_point28 )
geom_line33 = GGeometry.CreateLine( geom_point28, geom_point32 )
geom_line34 = GGeometry.CreateLine( geom_point32, geom_point31 )
geom_line35 = GGeometry.CreateLine( geom_point30, geom_point34 )
geom_line36 = GGeometry.CreateLine( geom_point32, geom_point33 )
geom_line37 = GGeometry.CreateLine( geom_point28, geom_point36 )
geom_line38 = GGeometry.CreateLine( geom_point29, geom_point35 )
geom_line39 = GGeometry.CreateLine( geom_point35, geom_point34 )
geom_line40 = GGeometry.CreateLine( geom_point34, geom_point33 )
geom_line41 = GGeometry.CreateLine( geom_point33, geom_point36 )
geom_line42 = GGeometry.CreateLine( geom_point36, geom_point35 )

geom_surf16 = GGeometry.FitSurfaceThroughCurves([geom_line29, geom_line31, geom_line27, geom_curve1, geom_line28, geom_line30])
geom_surf17 = GGeometry.FitSurfaceThroughCurves([geom_line28, geom_line34, geom_line33, geom_line32, geom_line27, geom_curve2])
geom_surf18 = GGeometry.FitSurfaceThroughCurves([geom_line33, geom_line37, geom_line41, geom_line36])
geom_surf19 = GGeometry.FitSurfaceThroughCurves([geom_line37, geom_line32, geom_line31, geom_line38, geom_line42])
geom_surf20 = GGeometry.FitSurfaceThroughCurves([geom_line29, geom_line38, geom_line35, geom_line39])
geom_surf21 = GGeometry.FitSurfaceThroughCurves([geom_line35, geom_line30, geom_line34, geom_line36, geom_line40])
geom_surf22 = GGeometry.FitSurfaceThroughCurves([geom_line39, geom_line40, geom_line41, geom_line42])

##########################################################################
# Saving the created geometry and exiting 

GFileIO.ExportIGES('TestHole.igs', 1, 0)
GUtils.StopGeom()

os.system("cp TestHole.igs ./Centaur/.")


