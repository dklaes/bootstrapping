#!/bin/bash
# Script to convert CSV files from the master thesis into LDAC catalogs.

# including some important files
. /vol/euclid1/euclid1_raid1/dklaes/reduce_KIDS_1.7.6_test/OMEGACAM.ini
. /vol/euclid1/euclid1_raid1/dklaes/reduce_KIDS_1.7.6_test/bash_functions.include
. /vol/euclid1/euclid1_raid1/dklaes/reduce_KIDS_1.7.6_test/progs.ini

MD=$1
i=$2
FILTER=r
BOOT_SCRIPTS=/vol/users/users/dklaes/git/bootstrapping/

FOLDER=${MD}/bootstrapping/realisation_${i}
cp ${MD}/chip_all.csv ./chip_all_original.csv

{
mv ${FOLDER}/chip_all.dat ./coeffs.txt
NUM=`grep -c datapoints ./coeffs.txt`
echo ${FOLDER} ${NUM} >> ${MD}/nums.txt
} &

mv ${FOLDER}/chip_all.csv ./


${P_ASCTOLDAC} -i ./chip_all.csv -o ./chip_all.cat -t PSSC -c /vol/users/users/dklaes/git/bootstrapping/asctoldac_tmp.conf -b 1 -n "sdss ldac cat"
${P_LDACCALC} -i ./chip_all.cat -o ./tmp.cat -t PSSC -c "(Xpos*0.0+0.00001);" -n Residual_Err "" -k FLOAT
${P_LDACCALC} -i ./tmp.cat -o ./chip_all_filtered_fitted.cat -t PSSC -c "(Xpos*0.0+0.00001);" -n Residual_fitted_Err "" -k FLOAT
rm ./chip_all.cat ./tmp.cat &


{
while read LINE
do
	NLINE=`grep -m1 -n "${LINE}" ./chip_all_original.csv | awk -F":" '{print $1}'`
	echo ${NLINE} >> ./objects.txt
done < ./chip_all.csv
mv ./objects.txt ${FOLDER}/
} &



${P_PYTHON} ${BOOT_SCRIPTS}/illum_ldactools.py -i chip_all_filtered_fitted.cat -t PSSC \
			-a STATISTICS -e "./coeffs.txt 10 10" \
			-o ${FOLDER}/stats.txt

mv ./coeffs.txt ${FOLDER}/coeffs.txt


${P_PYTHON} ${BOOT_SCRIPTS}/illum_ldactools.py -i chip_all_filtered_fitted.cat -t PSSC \
			-o ${FOLDER}/fitting.txt -a MAG_DEPENDENCY

rm ./chip_all_filtered_fitted.cat ./chip_all.csv ./chip_all_original.csv

wait
