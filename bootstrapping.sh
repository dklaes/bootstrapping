#!/bin/bash

# Bootstrapping script

# $1 = main directory where the files are
# $2 = number of chips
# $3 = destination directory
# $4 = number of realisations

# including some important files
# # # . ${INSTRUMENT:?}.ini
. /vol/aibn41/aibn41_1/dklaes/data/reduce_KIDS/OMEGACAM.ini
. /vol/aibn41/aibn41_1/dklaes/data/reduce_KIDS/bash_functions.include
. /vol/aibn41/aibn41_1/dklaes/data/reduce_KIDS/progs.ini

MAIND=$1
NCHIPS=$2
NREL=$3

PIXXMAX=`echo ${CHIPGEOMETRY} | ${P_GAWK} '{print $1*$3}'`
PIXYMAX=`echo ${CHIPGEOMETRY} | ${P_GAWK} '{print $2*$4}'`

# Creating the subfolders with data...

if [ ! -d "${MAIND}/bootstrapping" ]; then
  mkdir ${MAIND}/bootstrapping
else
  rm -r ${MAIND}/bootstrapping
  mkdir ${MAIND}/bootstrapping
fi

i=1
while [ ${i} -le ${NREL} ]
do
  mkdir ${MAIND}/bootstrapping/realisation_${i}
  i=$(( $i + 1 ))
done

./bootstrapping.py ${MAIND} ${NCHIPS} ${NREL}

A=`grep A ${MAIND}/chip_all.dat | ${P_GAWK} '{print $3}'`
B=`grep B ${MAIND}/chip_all.dat | ${P_GAWK} '{print $3}'`
C=`grep C ${MAIND}/chip_all.dat | ${P_GAWK} '{print $3}'`
D=`grep D ${MAIND}/chip_all.dat | ${P_GAWK} '{print $3}'`
E=`grep E ${MAIND}/chip_all.dat | ${P_GAWK} '{print $3}'`

echo $A $B $C $D $E ${PIXXMAX} ${PIXYMAX} | ${P_GAWK} '{print (-$5/$3-2*$2/$3*((2*$1*$5-$3*$4)/($3*$3-4*$1*$2)))*$6/2, ((2*$1*$5-$3*$4)/($3*$3-4*$1*$2))*$7/2}' > ${MAIND}/bootstrapping/true_position.csv

i=1
while [ ${i} -le ${NREL} ]
do
  A=`grep A ${MAIND}/bootstrapping/realisation_${i}/chip_all.dat | ${P_GAWK} '{print $3}'`
  B=`grep B ${MAIND}/bootstrapping/realisation_${i}/chip_all.dat | ${P_GAWK} '{print $3}'`
  C=`grep C ${MAIND}/bootstrapping/realisation_${i}/chip_all.dat | ${P_GAWK} '{print $3}'`
  D=`grep D ${MAIND}/bootstrapping/realisation_${i}/chip_all.dat | ${P_GAWK} '{print $3}'`
  E=`grep E ${MAIND}/bootstrapping/realisation_${i}/chip_all.dat | ${P_GAWK} '{print $3}'`

  echo $A $B $C $D $E ${PIXXMAX} ${PIXYMAX} | ${P_GAWK} '{print (-$5/$3-2*$2/$3*((2*$1*$5-$3*$4)/($3*$3-4*$1*$2)))*$6/2, ((2*$1*$5-$3*$4)/($3*$3-4*$1*$2))*$7/2}' >> ${MAIND}/bootstrapping/bootstrapping.csv
  i=$(( $i + 1 ))
done
rm ${MAIND}/bootstrapping/bootstrapping_distance.csv
rm ${MAIND}/bootstrapping/bootstrapping_X.dat
rm ${MAIND}/bootstrapping/bootstrapping_Y.dat
TRUE=`cat ${MAIND}/bootstrapping/true_position.csv`

while read LINE
do
  X=`echo ${LINE} ${TRUE} | ${P_GAWK} '{print $1-$3}'`
  Y=`echo ${LINE} ${TRUE} | ${P_GAWK} '{print $2-$4}'`
  echo ${LINE} ${X} ${Y} >> ${MAIND}/bootstrapping/bootstrapping_distance.csv
done < ${MAIND}/bootstrapping/bootstrapping.csv

${P_GAWK} '{print $3}' ${MAIND}/bootstrapping/bootstrapping_distance.csv | ${P_GAWK} -f /vol/aibn41/aibn41_1/dklaes/data/reduce_KIDS/meanvar.awk >> ${MAIND}/bootstrapping/bootstrapping_X.dat
${P_GAWK} '{print $4}' ${MAIND}/bootstrapping/bootstrapping_distance.csv | ${P_GAWK} -f /vol/aibn41/aibn41_1/dklaes/data/reduce_KIDS/meanvar.awk >> ${MAIND}/bootstrapping/bootstrapping_Y.dat



j=1
while [ ${j} -le ${NREL} ]
do
  i=1
  while [ ${i} -le ${NCHIPS} ]
  do
    echo "" >> ${MAIND}/bootstrapping/realisation_${j}/chip_${i}.dat
    echo "Statistics of residuals before fitting:" >> ${MAIND}/bootstrapping/realisation_${j}/chip_${i}.dat
    ${P_GAWK} '{if ($1!="#") {print $5}}' ${MAIND}/bootstrapping/realisation_${j}/chip_${i}.csv | ${P_GAWK} -f /vol/aibn41/aibn41_1/dklaes/data/reduce_KIDS/meanvar.awk >> ${MAIND}/bootstrapping/realisation_${j}/chip_${i}.dat
    echo "" >> ${MAIND}/bootstrapping/realisation_${j}/chip_${i}.dat
    echo "Statistics of residuals after fitting:" >> ${MAIND}/bootstrapping/realisation_${j}/chip_${i}.dat
    ${P_GAWK} '{if ($1!="#") {print $7}}' ${MAIND}/bootstrapping/realisation_${j}/chip_${i}.csv | ${P_GAWK} -f /vol/aibn41/aibn41_1/dklaes/data/reduce_KIDS/meanvar.awk >> ${MAIND}/bootstrapping/realisation_${j}/chip_${i}.dat
    cat ${MAIND}/bootstrapping/realisation_${j}/chip_${i}.csv >> ${MAIND}/bootstrapping/realisation_${j}/chip_all.csv
    i=$(( $i + 1 ))
  done
  echo "" >> ${MAIND}/bootstrapping/realisation_${j}/chip_all.dat
  echo "Statistics of residuals before fitting:" >> ${MAIND}/bootstrapping/realisation_${j}/chip_all.dat
  ${P_GAWK} '{if ($1!="#") {print $5}}' ${MAIND}/bootstrapping/realisation_${j}/chip_all.csv | ${P_GAWK} -f /vol/aibn41/aibn41_1/dklaes/data/reduce_KIDS/meanvar.awk >> ${MAIND}/bootstrapping/realisation_${j}/chip_all.dat
  echo "" >> ${MAIND}/bootstrapping/realisation_${j}/chip_all.dat
  echo "Statistics of residuals after fitting:" >> ${MAIND}/bootstrapping/realisation_${j}/chip_all.dat
  ${P_GAWK} '{if ($1!="#") {print $7}}' ${MAIND}/bootstrapping/realisation_${j}/chip_all.csv | ${P_GAWK} -f /vol/aibn41/aibn41_1/dklaes/data/reduce_KIDS/meanvar.awk >> ${MAIND}/bootstrapping/realisation_${j}/chip_all.dat
  ${P_GAWK} '{print $5, $7}' ${MAIND}/bootstrapping/realisation_${j}/chip_all.csv >> ${MAIND}/bootstrapping/all.csv
  j=$(( $j + 1 ))
done


echo "Statistics of residuals before fitting:" >> ${MAIND}/bootstrapping/all.dat
${P_GAWK} '{if ($1!="#") {print $1}}' ${MAIND}/bootstrapping/all.csv | ${P_GAWK} -f /vol/aibn41/aibn41_1/dklaes/data/reduce_KIDS/meanvar.awk >> ${MAIND}/bootstrapping/all.dat
echo "" >> ${MAIND}/bootstrapping/all.dat
echo "Statistics of residuals after fitting:" >> ${MAIND}/bootstrapping/all.dat
${P_GAWK} '{if ($1!="#") {print $2}}' ${MAIND}/bootstrapping/all.csv | ${P_GAWK} -f /vol/aibn41/aibn41_1/dklaes/data/reduce_KIDS/meanvar.awk >> ${MAIND}/bootstrapping/all.dat