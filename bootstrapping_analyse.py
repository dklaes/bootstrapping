#!/usr/bin/python
# -*- coding: utf-8 -*-
#scipy-0.11 and numpy-1.6.2 required!

import numpy as np
import sys
import os
import multiprocessing

global offset
global NCHIPS
global CHIPXMAX
global CHIPYMAX

path = sys.argv[1] + "/bootstrapping/"
NREL = int(sys.argv[2])
NCHIPS = int(sys.argv[3])

PIXXMAX = int((os.popen("echo ${CHIPGEOMETRY} | awk '{print $1}'").readlines())[0]) * int((os.popen("echo ${CHIPGEOMETRY} | awk '{print $3}'").readlines())[0])
PIXYMAX = int((os.popen("echo ${CHIPGEOMETRY} | awk '{print $2}'").readlines())[0]) * int((os.popen("echo ${CHIPGEOMETRY} | awk '{print $4}'").readlines())[0])
CHIPXMAX = float((os.popen("echo ${CHIPGEOMETRY} | awk '{print $3}'").readlines())[0])
CHIPYMAX = float((os.popen("echo ${CHIPGEOMETRY} | awk '{print $4}'").readlines())[0])

fresiduals = open(path + "results/results_residuals.csv", "w")
fprefactors = open(path + "results/results_prefactors.csv", "w")
fcenters =  open(path + "results/results_centers.csv", "w")


PREFACTORSINPUT = np.loadtxt(path + "/chip_all.dat", delimiter=" ", dtype={'names': ('factorname', 'equal', 'value', 'pm', 'error'), 'formats': ('S3', 'S1', 'S21', 'S2', 'S21')})

PREFACTORS = np.array([])
for j in range(NCHIPS):
	PREFACTORS = np.append(PREFACTORS, (float(PREFACTORSINPUT[j][2]), float(PREFACTORSINPUT[j][4])))
	fprefactors.write("0 %.21f %.21f\n" %(float(PREFACTORSINPUT[j][2]),float(PREFACTORSINPUT[j][4])))
PREFACTORS = PREFACTORS.reshape((-1,2))
A = PREFACTORS[0][0]
B = PREFACTORS[1][0]
C = PREFACTORS[2][0]
D = PREFACTORS[3][0]
E = PREFACTORS[4][0]

centerx = (-E/C-2.0*B/C*((2.0*A*E-C*D)/(C*C-4.0*A*B)))*PIXXMAX/2.0
centery = ((2.0*A*E-C*D)/(C*C-4.0*A*B))*PIXYMAX/2.0
fcenters.write("0 %.5f %.5f\n" %(centerx,centery))



for i in range(NREL):
	resbeforeALLCHIPS = np.array([])
	resafterALLCHIPS = np.array([])
	PREFACTORS = np.array([])
	for j in range(NCHIPS):
		resbefore = np.fromfile(path + "/realisation_" + str(i+1) + "/chip_%i.csv" %(j+1), sep="\t").reshape((-1,15))[:,6]
		resafter = np.fromfile(path + "/realisation_" + str(i+1) + "/chip_%i.csv" %(j+1), sep="\t").reshape((-1,15))[:,10]

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

	sigmabeforeALLCHIPS = np.std(resbeforeALLCHIPS)
	minimumbeforeALLCHIPS = np.amin(resbeforeALLCHIPS)
	maximumbeforeALLCHIPS = np.amax(resbeforeALLCHIPS)
	meanbeforeALLCHIPS = np.mean(resbeforeALLCHIPS)
	sigmaafterALLCHIPS = np.std(resafterALLCHIPS)
	minimumafterALLCHIPS = np.amin(resafterALLCHIPS)
	maximumafterALLCHIPS = np.amax(resafterALLCHIPS)
	meanafterALLCHIPS = np.mean(resafterALLCHIPS)

	fresiduals.write("%i 0 %f %f %f %f %f %f %f %f\n" %(i+1,sigmabeforeALLCHIPS,sigmaafterALLCHIPS,minimumbeforeALLCHIPS,minimumafterALLCHIPS,maximumbeforeALLCHIPS,maximumafterALLCHIPS,meanbeforeALLCHIPS,meanafterALLCHIPS))

	PREFACTORSINPUT = np.loadtxt(path + "/realisation_" + str(i+1) + "/chip_all.dat", delimiter=" ", dtype={'names': ('factorname', 'equal', 'value', 'pm', 'error'), 'formats': ('S3', 'S1', 'S21', 'S2', 'S21')})

	PREFACTORS = np.array([])
	# 5 prefactors
	for j in range(5):
		PREFACTORS = np.append(PREFACTORS, (float(PREFACTORSINPUT[j][2]), float(PREFACTORSINPUT[j][4])))
		fprefactors.write("%i %.21f %.21f\n" %(i+1,float(PREFACTORSINPUT[j][2]),float(PREFACTORSINPUT[j][4])))
	PREFACTORS = PREFACTORS.reshape((-1,2))
	A = PREFACTORS[0][0]
	B = PREFACTORS[1][0]
	C = PREFACTORS[2][0]
	D = PREFACTORS[3][0]
	E = PREFACTORS[4][0]

	centerx = (-E/C-2.0*B/C*((2.0*A*E-C*D)/(C*C-4.0*A*B)))*PIXXMAX/2.0
	centery = ((2.0*A*E-C*D)/(C*C-4.0*A*B))*PIXYMAX/2.0
	fcenters.write("%i %.5f %.5f\n" %(i+1,centerx,centery))

fresiduals.close()
fprefactors.close()
fcenters.close()

centers = np.fromfile(path + "/results/results_centers.csv", sep="\t").reshape((-1,3))

# Bootstrapping - true position
cendiffs = centers[1:] - centers[0]

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
def calculatingeps(i):
#  print("Start calculating data for chip " + str(i+1) + "/" + str(NCHIPS) + "...")
  
  # Getting the prefactors.
  A = float(((os.popen("cat " + path + "chip_all.dat | grep A | awk '{print $3}'").readlines())[0]).strip())
  B = float(((os.popen("cat " + path + "chip_all.dat | grep B | awk '{print $3}'").readlines())[0]).strip())
  C = float(((os.popen("cat " + path + "chip_all.dat | grep C | awk '{print $3}'").readlines())[0]).strip())
  D = float(((os.popen("cat " + path + "chip_all.dat | grep D | awk '{print $3}'").readlines())[0]).strip())
  E = float(((os.popen("cat " + path + "chip_all.dat | grep E | awk '{print $3}'").readlines())[0]).strip())

  # Creating arrays for xred (reduced and resized chip coordinates (for plotting and
  # numerical reasons)) and X (reduced (for plotting)). Having xred and X seperated doesn't
  # cause the problem of transforming the prefactors to the other coordinate system!
#  xred = 2.0*(np.arange(0, int(CHIPXMAX), 10)+offset[i][1])/PIXXMAX
#  X = np.arange(0, int(CHIPXMAX), 10)+offset[i][1]
  xred = 2.0*(np.arange(-8552, 8472, 10))/PIXXMAX
  X = np.arange(-8552, 8472, 10)

  # Now the same for y, yred and Y.
#  yred = 2.0*(np.arange(0, int(CHIPYMAX), 10)+offset[i][2])/PIXYMAX
#  Y = np.arange(0, int(CHIPYMAX), 10)+offset[i][2]
  yred = 2.0*(np.arange(-8583, 8430, 10))/PIXYMAX
  Y = np.arange(-8583, 8430, 10)

  # Creating the corresponding meshgrids.
  xxred, yyred = np.meshgrid(xred, yred)
  XX, YY = np.meshgrid(X, Y)

  # Calculating the position dependend residuals.
  # - epswoZP:		residuals without chip zeropoints in resized chip coordinates (reduced data set),
  #			for plotting
  epswoZP = A * xxred**2 + B * yyred**2 + C * xxred * yyred + D * xxred + E * yyred

  cond=(epswoZP.flatten())>-0.015
  XXcond = (XX.flatten())[cond]
  YYcond = (YY.flatten())[cond]
  epscond = (epswoZP.flatten())[cond]

  cond2=(epscond.flatten())<0.0
  XXcond2 = (XXcond.flatten())[cond2]
  YYcond2 = (YYcond.flatten())[cond2]
  epscond2 = (epscond.flatten())[cond2]

#  if len(epscond2) == 0:
#	return(0,0)

  centerx = (-E/C-2.0*B/C*((2.0*A*E-C*D)/(C*C-4.0*A*B)))*PIXXMAX/2.0
  centery = ((2.0*A*E-C*D)/(C*C-4.0*A*B))*PIXYMAX/2.0

  distance = np.sqrt(XXcond2*XXcond2+YYcond2*YYcond2)
  maxdistance = np.amax(distance)
  area = len(epscond2.flatten())*100
  print(centerx,centery)
  print(maxdistance, area)

  a = np.amax(maxdistance)
  b = area / (np.pi * a)
  e = np.sqrt(a*a-b*b)
  nume = e/a

  print(a,b,e,nume)

  # Returning data for plotting.
  return(maxdistance, area)


# Reading chip offsets from config file
offset=([])
for k in range(NCHIPS):
  a = int((os.popen("echo ${OFFSETX} | awk '{print $%i}'" %(k+1)).readlines())[0])
  b = int((os.popen("echo ${OFFSETY} | awk '{print $%i}'" %(k+1)).readlines())[0])
  offset = np.append(offset,[k,a,b])
offset = offset.reshape((-1,3))

#get the number of CPUs / cores
totalcpus = multiprocessing.cpu_count()
#maxcpus = int((os.popen("echo ${NPARA}").readlines())[0])
maxcpus = 4
usedcpus = maxcpus

# Use only as many cores as chips are avaiable
if NCHIPS < usedcpus:
  usedcpus = NCHIPS


print("Start calculating with " + str(usedcpus) + "/" + str(totalcpus) + " CPUs...")

# Initialise process pool:
pool = multiprocessing.Pool(usedcpus)

# execute the calculating with a 'pool-map' command:
catlist = []
#for h in range(NCHIPS):
for h in range(1):
	catlist.append(h)

#ALL = pool.map(calculatingeps, catlist)
pool.map(calculatingeps, catlist)

# Split the returning "ALL" array from "calculatingeps" into components:
# - XXALL:		X meshgrid of reduced chip coordinates
# - YYALL:		Y meshgrid of reduced chip coordinates
# - epswoZPALL:	residuals without chip zeropoint offsets for reduced chip coordinates
#maxdistance = np.array([])
#area = np.array([])


#for i in range(NCHIPS):
#  maxdistance = np.append(maxdistance,ALL[i][0])
#  area = np.append(area,ALL[i][1])

# Area = Pi * a * b with a is major axis and b is minor axis. a is given by maxdistance so for b: b = Area / (Pi * a)
#a = np.amax(maxdistance)
#totalarea = np.sum(area)
#totalarea = area
#b = totalarea / (np.pi * a)
#e = np.sqrt(a*a-b*b)

#print (a,b,totalarea,e)

