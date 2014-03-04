# Script for creating condor submission file

# $1 = main directory where the files are
# $2 = number of realisations
# $3 = name of submit file

MAIND=$1
NRELSTART=$2
NRELSTOP=$3
OUTFILE=$4



if [ ! -d "${MAIND}/log" ]; then
  mkdir ${MAIND}/log
  mkdir ${MAIND}/error
  mkdir ${MAIND}/output
fi

echo "Universe   = vanilla" > ${MAIND}/${OUTFILE}
echo "Executable = /vol/users/users/dklaes/git/bootstrapping/convert_data_masterthesis.sh" >> ${MAIND}/${OUTFILE}
echo "" >> ${MAIND}/${OUTFILE}

i=${NRELSTART}
while [ ${i} -le ${NRELSTOP} ]
do
  echo "Arguments  = ${MAIND} ${i}" >> ${MAIND}/${OUTFILE}
  echo "initialdir = ${MAIND}/bootstrapping/realisation_${i}/" >> ${MAIND}/${OUTFILE}
  echo "Log        = ${MAIND}/log/realisation_${i}.log" >> ${MAIND}/${OUTFILE}
  echo "Output     = ${MAIND}/output/realisation_${i}.out" >> ${MAIND}/${OUTFILE}
  echo "Error      = ${MAIND}/error/realisation_${i}.err" >> ${MAIND}/${OUTFILE}
  echo "Queue" >> ${MAIND}/${OUTFILE}
  echo "" >> ${MAIND}/${OUTFILE}
  i=$(( $i + 1 ))
done
