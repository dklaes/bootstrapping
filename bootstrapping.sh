#!/bin/bash
# New bootstrapping script
# To reduce traffic, please use the following commands before starting:
# mv chip_all_filtered.cat original_chip_all_filtered.cat
# ldacdelkey -i original_chip_all_filtered.cat -o chip_all_filtered_original_small.cat -t PSSC -k Mag MagErr AIRMASS IMAGEID IMAFLAGS_ISO GABODSID EXPTIME A_WCS B_WCS Dec Dec_err Epoch FIELD_POS Flag Ra Ra_err SeqString THETAWCS gmag gmag_err gmr imag imag_err imz rmi umag umag_err umg zmag zmag_err Xpos Ypos N_00 N_01 gmr_err

# $1 = main directory where the files are
# $2 = number of realisation

MAIND=$1
NUMREL=$2
FILTER=r
BOOT_SCRIPTS=/vol/users/users/dklaes/git/bootstrapping/

# including some important files
. /vol/euclid1/euclid1_raid1/dklaes/reduce_KIDS_1.7.6_test/OMEGACAM.ini
. /vol/euclid1/euclid1_raid1/dklaes/reduce_KIDS_1.7.6_test/bash_functions.include
. /vol/euclid1/euclid1_raid1/dklaes/reduce_KIDS_1.7.6_test/progs.ini

# Creating the subfolders with data...
${P_PYTHON} ${BOOT_SCRIPTS}/bootstrapping.py -i ${MAIND}/chip_all_filtered_original_small.cat -n ${NUMREL} -p ./ -t PSSC

# Fitting the data
${P_PYTHON} ${BOOT_SCRIPTS}/illum_correction_fit.py -i chip_all_filtered.cat \
				-t PSSC -p ./

#Applying the fit-parameter to our catalog data...
${P_PYTHON} ${BOOT_SCRIPTS}/illum_ldactools.py -i chip_all_filtered.cat \
			-o chip_all_filtered_fitted.cat -t PSSC \
			-a CALCS_AFTER_FITTING \
			-e "./coeffs.txt ${FILTER}"

${P_PYTHON} ${BOOT_SCRIPTS}/illum_ldactools.py -i chip_all_filtered_fitted.cat -t PSSC \
			-a STATISTICS -e "./coeffs.txt 10 10" \
			-o ./stats.txt

${P_PYTHON} ${BOOT_SCRIPTS}/illum_ldactools.py -i chip_all_filtered_fitted.cat -t PSSC \
			-o ./fitting.txt -a MAG_DEPENDENCY

${P_PYTHON} ${BOOT_SCRIPTS}/illum_ldactools.py -i chip_all_filtered.cat -t PSSC -k SeqNr \
			-o ./objects.txt -a KEYTOASC

rm chip_all_filtered.cat chip_all_filtered_fitted.cat