#!/bin/bash

# Script to convert CSV files from the master thesis into LDAC catalogs.
FILE=$1
FILTER=r

echo "VERBOSE = DEBUG"		>  ./asctoldac_tmp.conf
echo "#"			>> ./asctoldac_tmp.conf
echo "COL_NAME  = Xpos"		>> ./asctoldac_tmp.conf
echo "COL_TTYPE = DOUBLE"	>> ./asctoldac_tmp.conf
echo "COL_HTYPE = FLOAT"	>> ./asctoldac_tmp.conf
echo 'COL_COMM = ""'		>> ./asctoldac_tmp.conf
echo "COL_UNIT = ''"		>> ./asctoldac_tmp.conf
echo 'COL_DEPTH = 1'		>> ./asctoldac_tmp.conf
echo "#"			>> ./asctoldac_tmp.conf
echo "COL_NAME  = Ypos"		>> ./asctoldac_tmp.conf
echo "COL_TTYPE = DOUBLE"	>> ./asctoldac_tmp.conf
echo "COL_HTYPE = FLOAT"	>> ./asctoldac_tmp.conf
echo 'COL_COMM = ""'		>> ./asctoldac_tmp.conf
echo "COL_UNIT = ''"		>> ./asctoldac_tmp.conf
echo 'COL_DEPTH = 1'		>> ./asctoldac_tmp.conf
echo "#"			>> ./asctoldac_tmp.conf
echo "COL_NAME  = Mag"		>> ./asctoldac_tmp.conf
echo "COL_TTYPE = DOUBLE"	>> ./asctoldac_tmp.conf
echo "COL_HTYPE = FLOAT"	>> ./asctoldac_tmp.conf
echo 'COL_COMM = ""'		>> ./asctoldac_tmp.conf
echo "COL_UNIT = ''"		>> ./asctoldac_tmp.conf
echo 'COL_DEPTH = 1'		>> ./asctoldac_tmp.conf
echo "#"
echo "COL_NAME  = MagErr"	>> ./asctoldac_tmp.conf
echo "COL_TTYPE = DOUBLE"	>> ./asctoldac_tmp.conf
echo "COL_HTYPE = FLOAT"	>> ./asctoldac_tmp.conf
echo 'COL_COMM = ""'		>> ./asctoldac_tmp.conf
echo "COL_UNIT = ''"		>> ./asctoldac_tmp.conf
echo 'COL_DEPTH = 1'		>> ./asctoldac_tmp.conf
echo "#"
echo "COL_NAME  = ${FILTER}mag"	>> ./asctoldac_tmp.conf
echo "COL_TTYPE = DOUBLE"	>> ./asctoldac_tmp.conf
echo "COL_HTYPE = FLOAT"	>> ./asctoldac_tmp.conf
echo 'COL_COMM = ""'		>> ./asctoldac_tmp.conf
echo "COL_UNIT = ''"		>> ./asctoldac_tmp.conf
echo 'COL_DEPTH = 1'		>> ./asctoldac_tmp.conf
echo "#"			>> ./asctoldac_tmp.conf
echo "COL_NAME  = IMAGEID"	>> ./asctoldac_tmp.conf
echo "COL_TTYPE = LONG"		>> ./asctoldac_tmp.conf
echo "COL_HTYPE = INT"		>> ./asctoldac_tmp.conf
echo 'COL_COMM = ""'		>> ./asctoldac_tmp.conf
echo "COL_UNIT = ''"		>> ./asctoldac_tmp.conf
echo 'COL_DEPTH = 1'		>> ./asctoldac_tmp.conf
echo "#"			>> ./asctoldac_tmp.conf
echo "COL_NAME  = Residual"	>> ./asctoldac_tmp.conf
echo "COL_TTYPE = DOUBLE"	>> ./asctoldac_tmp.conf
echo "COL_HTYPE = FLOAT"	>> ./asctoldac_tmp.conf
echo 'COL_COMM = ""'		>> ./asctoldac_tmp.conf
echo "COL_UNIT = ''"		>> ./asctoldac_tmp.conf
echo 'COL_DEPTH = 1'		>> ./asctoldac_tmp.conf
echo "#"			>> ./asctoldac_tmp.conf
echo "COL_NAME  = Xpos_mod"	>> ./asctoldac_tmp.conf
echo "COL_TTYPE = DOUBLE"	>> ./asctoldac_tmp.conf
echo "COL_HTYPE = FLOAT"	>> ./asctoldac_tmp.conf
echo 'COL_COMM = ""'		>> ./asctoldac_tmp.conf
echo "COL_UNIT = ''"		>> ./asctoldac_tmp.conf
echo 'COL_DEPTH = 1'		>> ./asctoldac_tmp.conf
echo "#"			>> ./asctoldac_tmp.conf
echo "COL_NAME  = Ypos_mod"	>> ./asctoldac_tmp.conf
echo "COL_TTYPE = DOUBLE"	>> ./asctoldac_tmp.conf
echo "COL_HTYPE = FLOAT"	>> ./asctoldac_tmp.conf
echo 'COL_COMM = ""'		>> ./asctoldac_tmp.conf
echo "COL_UNIT = ''"		>> ./asctoldac_tmp.conf
echo 'COL_DEPTH = 1'		>> ./asctoldac_tmp.conf
echo "#"			>> ./asctoldac_tmp.conf
echo "COL_NAME  = Mag_fitted"	>> ./asctoldac_tmp.conf
echo "COL_TTYPE = DOUBLE"	>> ./asctoldac_tmp.conf
echo "COL_HTYPE = FLOAT"	>> ./asctoldac_tmp.conf
echo 'COL_COMM = ""'		>> ./asctoldac_tmp.conf
echo "COL_UNIT = ''"		>> ./asctoldac_tmp.conf
echo 'COL_DEPTH = 1'		>> ./asctoldac_tmp.conf
echo "#"			>> ./asctoldac_tmp.conf
echo "COL_NAME  = Residual_fitted">> ./asctoldac_tmp.conf
echo "COL_TTYPE = DOUBLE"	>> ./asctoldac_tmp.conf
echo "COL_HTYPE = FLOAT"	>> ./asctoldac_tmp.conf
echo 'COL_COMM = ""'		>> ./asctoldac_tmp.conf
echo "COL_UNIT = ''"		>> ./asctoldac_tmp.conf
echo 'COL_DEPTH = 1'		>> ./asctoldac_tmp.conf
echo "#"			>> ./asctoldac_tmp.conf
echo "COL_NAME  = AIRMASS"	>> ./asctoldac_tmp.conf
echo "COL_TTYPE = DOUBLE"	>> ./asctoldac_tmp.conf
echo "COL_HTYPE = FLOAT"	>> ./asctoldac_tmp.conf
echo 'COL_COMM = ""'		>> ./asctoldac_tmp.conf
echo "COL_UNIT = ''"		>> ./asctoldac_tmp.conf
echo 'COL_DEPTH = 1'		>> ./asctoldac_tmp.conf
echo "#"			>> ./asctoldac_tmp.conf
echo "COL_NAME  = Xpos_global"	>> ./asctoldac_tmp.conf
echo "COL_TTYPE = DOUBLE"	>> ./asctoldac_tmp.conf
echo "COL_HTYPE = FLOAT"	>> ./asctoldac_tmp.conf
echo 'COL_COMM = ""'		>> ./asctoldac_tmp.conf
echo "COL_UNIT = ''"		>> ./asctoldac_tmp.conf
echo 'COL_DEPTH = 1'		>> ./asctoldac_tmp.conf
echo "#"			>> ./asctoldac_tmp.conf
echo "COL_NAME  = Ypos_global"	>> ./asctoldac_tmp.conf
echo "COL_TTYPE = DOUBLE"	>> ./asctoldac_tmp.conf
echo "COL_HTYPE = FLOAT"	>> ./asctoldac_tmp.conf
echo 'COL_COMM = ""'		>> ./asctoldac_tmp.conf
echo "COL_UNIT = ''"		>> ./asctoldac_tmp.conf
echo 'COL_DEPTH = 1'		>> ./asctoldac_tmp.conf
echo "#"			>> ./asctoldac_tmp.conf

OUTFILE=`basename ${FILE} .csv`
asctoldac -i ${FILE} -o ${OUTFILE}.cat -t PSSC -c asctoldac_tmp.conf -b 1 -n "sdss ldac cat"
