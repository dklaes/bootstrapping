#!/usr/bin/python
# -*- coding: utf-8 -*-
#scipy-0.11 and numpy-1.6.2 required!

# Importing needed packages
import numpy as np
import sys
import os
import multiprocessing

# Defining global variables
global offset
global NCHIPS
global CHIPXMAX
global CHIPYMAX
global LL
global LR
global UL
global UR

# Reading command line arguments
path = sys.argv[1] + "/bootstrapping/"
NREL = int(sys.argv[2])
NCHIPS = int(sys.argv[3])

# Importing some global variables
PIXXMAX = int((os.popen("echo ${CHIPGEOMETRY} | awk '{print $1}'").readlines())[0]) * int((os.popen("echo ${CHIPGEOMETRY} | awk '{print $3}'").readlines())[0])
PIXYMAX = int((os.popen("echo ${CHIPGEOMETRY} | awk '{print $2}'").readlines())[0]) * int((os.popen("echo ${CHIPGEOMETRY} | awk '{print $4}'").readlines())[0])
CHIPXMAX = int((os.popen("echo ${CHIPGEOMETRY} | awk '{print $3}'").readlines())[0])
CHIPYMAX = int((os.popen("echo ${CHIPGEOMETRY} | awk '{print $4}'").readlines())[0])
MAXCHIPX = int((os.popen("echo ${CHIPGEOMETRY} | awk '{print $1}'").readlines())[0])
MAXCHIPY = int((os.popen("echo ${CHIPGEOMETRY} | awk '{print $2}'").readlines())[0])
LL = np.array([int((os.popen("echo ${OFFSETX} | awk '{print $1}'").readlines())[0]), int((os.popen("echo ${OFFSETY} | awk '{print $1}'").readlines())[0])])
LR = np.array([int((os.popen("echo ${OFFSETX} | awk '{print $" + str(MAXCHIPX) + "}'").readlines())[0]) + CHIPXMAX, int((os.popen("echo ${OFFSETY} | awk '{print $1}'").readlines())[0])])
UL = np.array([int((os.popen("echo ${OFFSETX} | awk '{print $1}'").readlines())[0]), int((os.popen("echo ${OFFSETY} | awk '{print $" + str(MAXCHIPY*MAXCHIPX) + "}'").readlines())[0]) + CHIPYMAX])
UR = np.array([int((os.popen("echo ${OFFSETX} | awk '{print $" + str(MAXCHIPX) + "}'").readlines())[0]) + CHIPXMAX, int((os.popen("echo ${OFFSETY} | awk '{print $" + str(MAXCHIPY*MAXCHIPX) + "}'").readlines())[0]) + CHIPYMAX])


# Calculations for "true" solution
fresiduals = open(path + "results/results_residuals.csv", "w")
fcenters =  open(path + "results/results_centers.csv", "w")

# Getting the prefactors of the true solution.
A = float(((os.popen("cat " + path + "/chip_all.dat | grep A | awk '{print $3}'").readlines())[0]).strip())
B = float(((os.popen("cat " + path + "/chip_all.dat | grep B | awk '{print $3}'").readlines())[0]).strip())
C = float(((os.popen("cat " + path + "/chip_all.dat | grep C | awk '{print $3}'").readlines())[0]).strip())
D = float(((os.popen("cat " + path + "/chip_all.dat | grep D | awk '{print $3}'").readlines())[0]).strip())
E = float(((os.popen("cat " + path + "/chip_all.dat | grep E | awk '{print $3}'").readlines())[0]).strip())

# Calculating the "true" center and write it into a file. The "true" solution is written as realisation 0.
centerx = (-E/C-2.0*B/C*((2.0*A*E-C*D)/(C*C-4.0*A*B)))*PIXXMAX/2.0
centery = ((2.0*A*E-C*D)/(C*C-4.0*A*B))*PIXYMAX/2.0
fcenters.write("0 %.5f %.5f\n" %(centerx,centery))


# Calculating statistics and center postions of each realisation.
for i in range(NREL):
	resbeforeALLCHIPS = np.array([])
	resafterALLCHIPS = np.array([])
	PREFACTORS = np.array([])
	for j in range(NCHIPS):
		resbefore = np.fromfile(path + "/realisation_" + str(i+1) + "/chip_%i.csv" %(j+1), sep="\t").reshape((-1,15))[:,6]
		resafter = np.fromfile(path + "/realisation_" + str(i+1) + "/chip_%i.csv" %(j+1), sep="\t").reshape((-1,15))[:,10]

		# Calculating minimum, maximum and sigma of the residuals before and after fitting per chip.
		sigmabefore = np.std(resbefore)
		minimumbefore = np.amin(resbefore)
		maximumbefore = np.amax(resbefore)
		meanbefore = np.mean(resbefore)
		sigmaafter = np.std(resafter)
		minimumafter = np.amin(resafter)
		maximumafter = np.amax(resafter)
		meanafter = np.mean(resafter)

		resbeforeALLCHIPS = np.append(resbeforeALLCHIPS, resbefore)
		resafterALLCHIPS = np.append(resafterALLCHIPS, resafter)

		fresiduals.write("%i %i %f %f %f %f %f %f %f %f\n" %(i+1, j+1, sigmabefore, sigmaafter, minimumbefore, minimumafter, maximumbefore, maximumafter, meanbefore, meanafter))

	# Calculating minimum, maximum and sigma of the residuals before and after fitting per realisation.
	sigmabeforeALLCHIPS = np.std(resbeforeALLCHIPS)
	minimumbeforeALLCHIPS = np.amin(resbeforeALLCHIPS)
	maximumbeforeALLCHIPS = np.amax(resbeforeALLCHIPS)
	meanbeforeALLCHIPS = np.mean(resbeforeALLCHIPS)
	sigmaafterALLCHIPS = np.std(resafterALLCHIPS)
	minimumafterALLCHIPS = np.amin(resafterALLCHIPS)
	maximumafterALLCHIPS = np.amax(resafterALLCHIPS)
	meanafterALLCHIPS = np.mean(resafterALLCHIPS)

	fresiduals.write("%i 0 %f %f %f %f %f %f %f %f\n" %(i+1,sigmabeforeALLCHIPS,sigmaafterALLCHIPS,minimumbeforeALLCHIPS,minimumafterALLCHIPS,maximumbeforeALLCHIPS,maximumafterALLCHIPS,meanbeforeALLCHIPS,meanafterALLCHIPS))

	# Getting the prefactors and center position for one realisation.
	A = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep A | awk '{print $3}'").readlines())[0]).strip())
	B = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep B | awk '{print $3}'").readlines())[0]).strip())
	C = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep C | awk '{print $3}'").readlines())[0]).strip())
	D = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep D | awk '{print $3}'").readlines())[0]).strip())
	E = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep E | awk '{print $3}'").readlines())[0]).strip())

	centerx = (-E/C-2.0*B/C*((2.0*A*E-C*D)/(C*C-4.0*A*B)))*PIXXMAX/2.0
	centery = ((2.0*A*E-C*D)/(C*C-4.0*A*B))*PIXYMAX/2.0
	fcenters.write("%i %.5f %.5f\n" %(i+1,centerx,centery))

fresiduals.close()
fcenters.close()

centers = np.fromfile(path + "/results/results_centers.csv", sep="\t").reshape((-1,3))

# Calculating bootstrapping center positions - "true" center position
cendiffs = centers[1:] - centers[0]

# Calculating minimum, maximum, mean distance of all realisations to "true" center position for one run including sigma.
meandiffx = np.mean(cendiffs[:,1])
meandiffy = np.mean(cendiffs[:,2])
mindiffx = np.amin(cendiffs[:,1])
mindiffy = np.amin(cendiffs[:,2])
maxdiffx = np.amax(cendiffs[:,1])
maxdiffy = np.amax(cendiffs[:,2])
sigmadiffx = np.std(cendiffs[:,1])
sigmadiffy = np.std(cendiffs[:,2])

fcenterprop = open(path + "results/results_center.csv", "w")
fcenterprop.write("mindiffx mindiffy %.5f %.5f\n" %(mindiffx,mindiffy))
fcenterprop.write("maxdiffx maxdiffy %.5f %.5f\n" %(maxdiffx,maxdiffy))
fcenterprop.write("meandiffx meandiffy %.5f %.5f\n" %(meandiffx,meandiffy))
fcenterprop.write("sigmadiffx sigmadiffy %.5f %.5f" %(sigmadiffx,sigmadiffy))
fcenterprop.close()




# Analysis of ellipse shape
def calculatingeps(i, coordinates):
  print("Calculating major and minor axis and (numerical) ellipticity for realisation " + str(i+1) + "...")
  
  # Getting the prefactors and calculate the center position.
  A = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep A | awk '{print $3}'").readlines())[0]).strip())
  B = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep B | awk '{print $3}'").readlines())[0]).strip())
  C = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep C | awk '{print $3}'").readlines())[0]).strip())
  D = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep D | awk '{print $3}'").readlines())[0]).strip())
  E = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep E | awk '{print $3}'").readlines())[0]).strip())

  centerx = (-E/C-2.0*B/C*((2.0*A*E-C*D)/(C*C-4.0*A*B)))*PIXXMAX/2.0
  centery = ((2.0*A*E-C*D)/(C*C-4.0*A*B))*PIXYMAX/2.0

  maxdistance = np.array([])
  area = np.array([])

  # Creating arrays for xred (reduced and resized chip coordinates (for plotting and
  # numerical reasons)) and X (reduced (for plotting)). Having xred and X seperated doesn't
  # cause the problem of transforming the prefactors to the other coordinate system!
  # As soon as possible not longer needed arrays are deleted from memory, otherwise too much
  # memory is occupied.

  for k in range(len(coordinates)):
	xred = 2.0*(np.arange(coordinates[k][0], coordinates[k][1], 1))/PIXXMAX
	yred = 2.0*(np.arange(coordinates[k][2], coordinates[k][3], 1))/PIXYMAX

	# Creating the corresponding meshgrids.
	xxred, yyred = np.meshgrid(xred, yred)
	del xred
	del yred
	# Calculating the position dependend residuals.
	# - epswoZP:		residuals without chip zeropoints in resized chip coordinates (reduced data set),
	#			for plotting
	epswoZP = A * xxred**2 + B * yyred**2 + C * xxred * yyred + D * xxred + E * yyred
	del xxred
	del yyred

	cond=(epswoZP.flatten())>-0.015
	X = np.arange(coordinates[k][0], coordinates[k][1], 1)
	Y = np.arange(coordinates[k][2], coordinates[k][3], 1)
	XX, YY = np.meshgrid(X, Y)
	del X
	del Y
	XXcond = (XX.flatten())[cond]
	del XX
	YYcond = (YY.flatten())[cond]
	del YY
	epscond = (epswoZP.flatten())[cond]
	del epswoZP
	del cond

	cond2=(epscond.flatten())<0.0
	XXcond2 = (XXcond.flatten())[cond2]
	del XXcond
	YYcond2 = (YYcond.flatten())[cond2]
	del YYcond
	epscond2 = (epscond.flatten())[cond2]
	del epscond
	del cond2

	distance = np.sqrt(XXcond2*XXcond2+YYcond2*YYcond2)
	maxdistance = np.append(maxdistance, np.amax(distance))
	area = np.append(area, len(epscond2.flatten()))

	del XXcond2
	del YYcond2
	del epscond2

  maxdistancefinal = np.amax(maxdistance)
  areafinal = np.sum(area)

  print("The center is at (" + str(centerx) + "," + str(centery) + ")")
  print(str(int(areafinal)) + " pixels are within limits.")

  a = np.amax(maxdistancefinal)
  b = areafinal / (np.pi * a)
  e = np.sqrt(a*a-b*b)
  nume = e/a

  print("Length of major axis: " + str(a))
  print("Length of minor axis: " + str(b))
  print("Ellipticity: " + str(e))
  print("Numerical ellipticity: " + str(nume))


coordinates = np.array([])
# Bottom left part of the camera
coordinates = np.append(coordinates, (LL[0],0,LL[1],0))
# Bottom right part of the camera.
coordinates = np.append(coordinates, (0,LR[0],LR[1],0))
# Upper left part of the camera.
coordinates = np.append(coordinates, (UL[0],0,0,UL[1]))
# Upper right part of the camera.
coordinates = np.append(coordinates, (0,UR[0],0,UR[1]))

coordinates = coordinates.reshape((-1,4))


for i in range(NREL):
	calculatingeps(i, coordinates)

