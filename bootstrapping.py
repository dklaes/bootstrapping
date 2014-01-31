# -*- coding: utf-8 -*-
#scipy-0.11 and numpy-1.6.2 required!

#Importing packages
from __future__ import division, print_function
import numpy as np
import sys
import getopt
from time import *
import random
import pyfits

#Reading command line arguments
opts, args = getopt.getopt(sys.argv[1:], "i:p:t:n:", ["input=", "path=", "table=", "nrel="])

infile = path = table = nrel = None
for o, a in opts:
    if o in ("-i"):
        infile = a.split()
    elif o in ("-p"):
        path = a
    elif o in ("-t"):
        table = a
    elif o in ("-n"):
	nrel = a

t1=time()

firstfile = pyfits.open(infile[0])
nrows = firstfile[table].data.shape[0]
hdu = pyfits.new_table(firstfile[table].columns, nrows=nrows)
  

for k in range(nrows):
  l = random.randrange(0,nrows,1)
  for i in range(len(firstfile[table].columns)):
    hdu.data.field(i)[k]=firstfile[table].data.field(i)[l]

hdu.header = firstfile[table].header
hdu.columns = firstfile[table].columns
hdu.writeto(path + "chip_all_filtered.cat", clobber=True)
  
t2=time()

print("Dauer: " + str(t2-t1) + " Sekunden")
