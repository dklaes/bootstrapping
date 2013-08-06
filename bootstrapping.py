#!/usr/bin/python
# -*- coding: utf-8 -*-
#scipy-0.11 and numpy-1.6.2 required!

#Importing packages
from __future__ import division, print_function
import matplotlib.pyplot as plt
import matplotlib.pylab as lab
import numpy as np
import os
import sys
import multiprocessing
from time import *
import random
import csv

#Reading command line arguments
path = sys.argv[1]
nchips = int(sys.argv[2])
nrel = int(sys.argv[3])

t1=time()

def bootstrapping(i):
  global nchips
  for j in range(nchips):
    a = np.fromfile(path + "chip_%i.csv" %(j+1), sep="\t")
    a = a.reshape((-1,15))
    lena = int(len(a))
    b = np.array([])
    k=1
    for k in range(lena):
      l = random.randrange(0,lena,1)
      b = np.append(b, a[l])
    b = b.reshape(-1,15)
    np.savetxt(path + "/bootstrapping/realisation_" + str(i+1) + "/chip_" + str(j+1) + ".csv", b, fmt='%f', delimiter=" ")
    os.popen("cat " + path + "bootstrapping/realisation_" + str(i+1) + "/chip_" + str(j+1) + ".csv >> " + path + "/bootstrapping/realisation_" + str(i+1) + "/chip_all.csv")
  os.popen("NUMCHIPS=32 && ./illum_correction_fit_bootstrap.py " + path + "/bootstrapping/realisation_" + str(i+1) + "/")

totalcpus = multiprocessing.cpu_count()

# Initialise process pool:
pool = multiprocessing.Pool(totalcpus)


# execute the conversion with a 'pool-map' command:
catlist = []
for h in range(nrel):
        catlist.append(h)

pool.map(bootstrapping, catlist)

t2=time()

print("Dauer: " + str(t2-t1) + " Sekunden")
