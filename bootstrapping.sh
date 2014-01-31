#!/bin/bash
# New bootstrapping script

# $1 = main directory where the files are
# $2 = number of realisation

MAIND=$1
NUMREL=$2
FILTER=r

# including some important files
. /vol/euclid1/euclid1_raid1/dklaes/reduce_KIDS_1.7.6_test/OMEGACAM.ini
. /vol/euclid1/euclid1_raid1/dklaes/reduce_KIDS_1.7.6_test/bash_functions.include
. /vol/euclid1/euclid1_raid1/dklaes/reduce_KIDS_1.7.6_test/progs.ini

# Creating the subfolders with data...
mkdir ${MAIND}/bootstrapping/realisation_${NUMREL}

${P_PYTHON} bootstrapping.py -i ${MAIND}/chip_all_filtered.cat -n ${NUMREL} -p ./ -t PSSC

# Fitting the data
${P_PYTHON} illum_correction_fit.py -i ./chip_all_filtered.cat \
				-t PSSC -p ./

#Applying the fit-parameter to our catalog data...
${P_PYTHON} illum_ldactools.py -i ./chip_all_filtered.cat \
			-o ./chip_all_filtered_fitted.cat -t PSSC \
			-a CALCS_AFTER_FITTING \
			-e "./coeffs.txt ${FILTER}"

${P_PYTHON} illum_ldactools.py -i ./chip_all_filtered_fitted.cat -t PSSC \
			-a STATISTICS -e "./coeffs.txt 10 10" \
			-o ./stats.txt

${P_PYTHON} illum_ldactools.py -i ./chip_all_filtered_fitted.cat -t PSSC \
			-o ./fitting.txt -a MAG_DEPENDENCY

cp *.txt *.cat ${MAIND}/bootstrapping/realisation_${NUMREL}/
rm *.txt *.cat *.pyc