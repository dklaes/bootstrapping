# Script for creating condor submission file

# $1 = main directory where the files are
# $2 = number of realisations
# $3 = name of submit file

MAIND=$1
NRELSTART=$2
NRELSTOP=$3
OUTFILE=$4

rm ${OUTFILE}

if [ ! -d "${MAIND}/bootstrapping" ]; then
  mkdir ${MAIND}/bootstrapping
fi

i=${NRELSTART}
while [ ${i} -le ${NRELSTOP} ]
do
  mkdir ${MAIND}/bootstrapping/realisation_${i}/
  echo ${i} >> ${OUTFILE}
  i=$(( $i + 1 ))
done

NREL=$(( $NRELSTOP - $NRELSTART ))
NPROC=16
i=0
while [ ${i} -lt ${NPROC} ]
do
  FILES[$i]=`cat ${OUTFILE} | awk '(NR % '${NPROC}' == '$i')'`
  NFILES[$i]=`echo ${FILES[$i]} | wc -w`

  j=$(( $i + 1 ))

  echo -e "Starting Job ${j}. It has ${NFILES[$i]} realisations to process!\n"

  {
    k=1
    for REALISATION in ${FILES[$i]}
    do
      echo "Starting realisation ${REALISATION}..."
      cd ${MAIND}/bootstrapping/realisation_${REALISATION}/
      /users/dklaes/git/bootstrapping/bootstrapping.sh ${MAIND} ${REALISATION}
      echo "Finished realisation ${REALISATION}..."
      k=$(( $k + 1 ))
    done
  } &
  i=$(( $i + 1 ))
done

# only finish the script if all lauched background jobs
# are finished!
wait

echo "" | mail -s "science finished" dklaes@astro.uni-bonn.de
