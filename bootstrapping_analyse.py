#!/usr/bin/python
# -*- coding: utf-8 -*-
#scipy-0.11 and numpy-1.6.2 required!

# Importing needed packages
import numpy as np
import sys
import os
import multiprocessing
from scipy.optimize import curve_fit

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
fprefactors = open(path + "results/results_prefactors.csv", "w")

# Getting the prefactors of the true solution.
A = float(((os.popen("cat " + path + "/chip_all.dat | grep A | awk '{print $3}'").readlines())[0]).strip())
B = float(((os.popen("cat " + path + "/chip_all.dat | grep B | awk '{print $3}'").readlines())[0]).strip())
C = float(((os.popen("cat " + path + "/chip_all.dat | grep C | awk '{print $3}'").readlines())[0]).strip())
D = float(((os.popen("cat " + path + "/chip_all.dat | grep D | awk '{print $3}'").readlines())[0]).strip())
E = float(((os.popen("cat " + path + "/chip_all.dat | grep E | awk '{print $3}'").readlines())[0]).strip())
F1 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F1 | awk '{print $3}'").readlines())[0]).strip())
F2 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F2 | awk '{print $3}'").readlines())[0]).strip())
F3 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F3 | awk '{print $3}'").readlines())[0]).strip())
F4 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F4 | awk '{print $3}'").readlines())[0]).strip())
F5 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F5 | awk '{print $3}'").readlines())[0]).strip())
F6 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F6 | awk '{print $3}'").readlines())[0]).strip())
F7 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F7 | awk '{print $3}'").readlines())[0]).strip())
F8 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F8 | awk '{print $3}'").readlines())[0]).strip())
F9 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F9 | awk '{print $3}'").readlines())[0]).strip())
F10 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F10 | awk '{print $3}'").readlines())[0]).strip())
F11 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F11 | awk '{print $3}'").readlines())[0]).strip())
F12 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F12 | awk '{print $3}'").readlines())[0]).strip())
F13 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F13 | awk '{print $3}'").readlines())[0]).strip())
F14 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F14 | awk '{print $3}'").readlines())[0]).strip())
F15 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F15 | awk '{print $3}'").readlines())[0]).strip())
F16 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F16 | awk '{print $3}'").readlines())[0]).strip())
F17 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F17 | awk '{print $3}'").readlines())[0]).strip())
F18 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F18 | awk '{print $3}'").readlines())[0]).strip())
F19 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F19 | awk '{print $3}'").readlines())[0]).strip())
F20 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F20 | awk '{print $3}'").readlines())[0]).strip())
F21 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F21 | awk '{print $3}'").readlines())[0]).strip())
F22 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F22 | awk '{print $3}'").readlines())[0]).strip())
F23 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F23 | awk '{print $3}'").readlines())[0]).strip())
F24 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F24 | awk '{print $3}'").readlines())[0]).strip())
F25 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F25 | awk '{print $3}'").readlines())[0]).strip())
F26 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F26 | awk '{print $3}'").readlines())[0]).strip())
F27 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F27 | awk '{print $3}'").readlines())[0]).strip())
F28 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F28 | awk '{print $3}'").readlines())[0]).strip())
F29 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F29 | awk '{print $3}'").readlines())[0]).strip())
F30 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F30 | awk '{print $3}'").readlines())[0]).strip())
F31 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F31 | awk '{print $3}'").readlines())[0]).strip())
F32 = float(((os.popen("cat " + path + "/chip_all.dat | grep -m1 F32 | awk '{print $3}'").readlines())[0]).strip())
fprefactors.write("0 %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f\n" %(A, B, C, D, E, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14, F15, F16, F17, F18, F19, F20, F21, F22, F23, F24, F25, F26, F27, F28, F29, F30, F31, F32))

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

	fresiduals.write("%i 0 %f %f %f %f %f %f %f %f\n" %(i+1, sigmabeforeALLCHIPS, sigmaafterALLCHIPS, minimumbeforeALLCHIPS, minimumafterALLCHIPS, maximumbeforeALLCHIPS, maximumafterALLCHIPS, meanbeforeALLCHIPS, meanafterALLCHIPS))

	# Getting the prefactors and center position for one realisation.
	A = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep A | awk '{print $3}'").readlines())[0]).strip())
	B = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep B | awk '{print $3}'").readlines())[0]).strip())
	C = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep C | awk '{print $3}'").readlines())[0]).strip())
	D = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep D | awk '{print $3}'").readlines())[0]).strip())
	E = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep E | awk '{print $3}'").readlines())[0]).strip())
	F1 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F1 | awk '{print $3}'").readlines())[0]).strip())
	F2 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F2 | awk '{print $3}'").readlines())[0]).strip())
	F3 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F3 | awk '{print $3}'").readlines())[0]).strip())
	F4 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F4 | awk '{print $3}'").readlines())[0]).strip())
	F5 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F5 | awk '{print $3}'").readlines())[0]).strip())
	F6 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F6 | awk '{print $3}'").readlines())[0]).strip())
	F7 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F7 | awk '{print $3}'").readlines())[0]).strip())
	F8 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F8 | awk '{print $3}'").readlines())[0]).strip())
	F9 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F9 | awk '{print $3}'").readlines())[0]).strip())
	F10 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F10 | awk '{print $3}'").readlines())[0]).strip())
	F11 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F11 | awk '{print $3}'").readlines())[0]).strip())
	F12 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F12 | awk '{print $3}'").readlines())[0]).strip())
	F13 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F13 | awk '{print $3}'").readlines())[0]).strip())
	F14 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F14 | awk '{print $3}'").readlines())[0]).strip())
	F15 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F15 | awk '{print $3}'").readlines())[0]).strip())
	F16 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F16 | awk '{print $3}'").readlines())[0]).strip())
	F17 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F17 | awk '{print $3}'").readlines())[0]).strip())
	F18 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F18 | awk '{print $3}'").readlines())[0]).strip())
	F19 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F19 | awk '{print $3}'").readlines())[0]).strip())
	F20 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F20 | awk '{print $3}'").readlines())[0]).strip())
	F21 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F21 | awk '{print $3}'").readlines())[0]).strip())
	F22 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F22 | awk '{print $3}'").readlines())[0]).strip())
	F23 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F23 | awk '{print $3}'").readlines())[0]).strip())
	F24 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F24 | awk '{print $3}'").readlines())[0]).strip())
	F25 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F25 | awk '{print $3}'").readlines())[0]).strip())
	F26 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F26 | awk '{print $3}'").readlines())[0]).strip())
	F27 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F27 | awk '{print $3}'").readlines())[0]).strip())
	F28 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F28 | awk '{print $3}'").readlines())[0]).strip())
	F29 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F29 | awk '{print $3}'").readlines())[0]).strip())
	F30 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F30 | awk '{print $3}'").readlines())[0]).strip())
	F31 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F31 | awk '{print $3}'").readlines())[0]).strip())
	F32 = float(((os.popen("cat " + path + "/realisation_" + str(i+1) + "/chip_all.dat | grep -m1   F32 | awk '{print $3}'").readlines())[0]).strip())
	fprefactors.write("%i %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f\n" %(i+1, A, B, C, D, E, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14, F15, F16, F17, F18, F19, F20, F21, F22, F23, F24, F25, F26, F27, F28, F29, F30, F31, F32))

	centerx = (-E/C-2.0*B/C*((2.0*A*E-C*D)/(C*C-4.0*A*B)))*PIXXMAX/2.0
	centery = ((2.0*A*E-C*D)/(C*C-4.0*A*B))*PIXYMAX/2.0
	fcenters.write("%i %.5f %.5f\n" %(i+1,centerx,centery))

fresiduals.close()
fcenters.close()
fprefactors.close()

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
  x = np.array([])
  y = np.array([])
  eps = np.array([])

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

	x = np.append(x, XXcond2[distance==maxdistance[k]])
	y = np.append(y, YYcond2[distance==maxdistance[k]])
	eps = np.append(eps, epscond2[distance==maxdistance[k]])

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

  Xmax = x[maxdistance == maxdistancefinal][0]
  Ymax = y[maxdistance == maxdistancefinal][0]
  angle = np.arcsin((Xmax-centerx)/maxdistancefinal) * 180 / np.pi

  print("Length of major axis: " + str(a))
  print("Length of minor axis: " + str(b))
  print("Angle between (0,y) and major axis: " + str(angle))
  print("Ellipticity: " + str(e))
  print("Numerical ellipticity: " + str(nume) + "\n")

  fellipse.write("%i %f %f %f %f %f\n" %(i+1, a, b, e, nume, angle))

  


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

fellipse = open(path + "results/results_ellipses.csv", "w")

for i in range(NREL):
	calculatingeps(i, coordinates)

fellipse.close()











# Magnitude - residual dependency

def function_linear_plusOffset(x, A, B):
	return A*x + B

def function_linear(x, A):
	return A*x

fmagdependency = open(path + "results/results_magdependency.csv", "w")

for i in range(NREL):

	a = np.array([])
	b = np.array([])
	c = np.array([])
	d = np.array([])
	for k in range(NCHIPS):
		# Importing catalogues.
		a = np.fromfile(path + "/realisation_" + str(i+1) + "/chip_%i.csv" %(k+1), sep="\t")
		b = np.append(b,a)
		c = a.reshape((-1,15))

		# Linear fit with offset before illumination correction
		p0 = np.array([0.0, 0.0])
		best_par_before_Offset, cov_fit_before_Offset = curve_fit(function_linear_plusOffset, c[:,14], c[:,6], p0, sigma=np.std(c[:,6]))

		# Linear fit with offset after illumination correction
		p0 = np.array([0.0, 0.0])
		best_par_after_Offset, cov_fit_after_Offset = curve_fit(function_linear_plusOffset, c[:,9], c[:,10], p0, sigma=np.std(c[:,10]))

		# Linear fit without offset before illumination correction
		p0 = np.array([0.0])
		best_par_before_withoutOffset, cov_fit_before_withoutOffset = curve_fit(function_linear, c[:,14], c[:,6], p0, sigma=np.std(c[:,6]))

		# Linear fit without offset after illumination correction
		p0 = np.array([0.0])
		best_par_after_withoutOffset, cov_fit_after_withoutOffset = curve_fit(function_linear, c[:,9], c[:,10], p0, sigma=np.std(c[:,10]))

		# Writing to file
		# Format: realisation chip A_before_Offset B_before_Offset A_after_Offset B_after_Offset A_before_withoutOffset A_after_withoutOffset
		fmagdependency.write("%i %i %f %f %f %f %f %f\n" %(i+1, k+1, best_par_before_Offset[0], best_par_before_Offset[1], best_par_after_Offset[0], best_par_after_Offset[1], best_par_before_withoutOffset[0], best_par_after_withoutOffset[0]))

	d = b.reshape((-1,15))

	# Linear fit with offset before illumination correction
	p0 = np.array([0.0, 0.0])
	best_par_before_Offset, cov_fit_before_Offset = curve_fit(function_linear_plusOffset, d[:,14], d[:,6], p0, sigma=np.std(d[:,6]))

	# Linear fit with offset after illumination correction
	p0 = np.array([0.0, 0.0])
	best_par_after_Offset, cov_fit_after_Offset = curve_fit(function_linear_plusOffset, d[:,9], d[:,10], p0, sigma=np.std(d[:,10]))

	# Linear fit without offset before illumination correction
	p0 = np.array([0.0])
	best_par_before_withoutOffset, cov_fit_before_withoutOffset = curve_fit(function_linear, d[:,14], d[:,6], p0, sigma=np.std(d[:,6]))

	# Linear fit without offset after illumination correction
	p0 = np.array([0.0])
	best_par_after_withoutOffset, cov_fit_after_withoutOffset = curve_fit(function_linear, d[:,9], d[:,10], p0, sigma=np.std(d[:,10]))

	# Writing to file
	# Format: realisation chip=0(ALL) A_before_Offset B_before_Offset A_after_Offset B_after_Offset A_before_withoutOffset A_after_withoutOffset
	fmagdependency.write("%i 0 %f %f %f %f %f %f\n" %(i+1, best_par_before_Offset[0], best_par_before_Offset[1], best_par_after_Offset[0], best_par_after_Offset[1], best_par_before_withoutOffset[0], best_par_after_withoutOffset[0]))

fmagdependency.close()
