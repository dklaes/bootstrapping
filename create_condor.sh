# Script for creating condor submission file

# $1 = main directory where the files are
# $2 = start number of realisations
# $3 = end number of realisations

MAIND=$1
NRELSTART=$2
NRELSTOP=$3

if [ ! -d "${MAIND}/bootstrapping" ]; then
  mkdir ${MAIND}/bootstrapping
  mkdir ${MAIND}/log
  mkdir ${MAIND}/error
  mkdir ${MAIND}/output
else
  rm -r ${MAIND}/bootstrapping
  rm -r ${MAIND}/log
  rm -r ${MAIND}/error
  rm -r ${MAIND}/output
  mkdir ${MAIND}/bootstrapping
  mkdir ${MAIND}/log
  mkdir ${MAIND}/error
  mkdir ${MAIND}/output
  echo ""
fi

echo "Universe   = vanilla" > submit
echo "Executable = /vol/users/users/dklaes/git/bootstrapping/bootstrapping.sh" >> submit
echo "transfer_input_files = /vol/users/users/dklaes/git/bootstrapping/ldac.py" >> submit
echo "initialdir     = /vol/users/users/dklaes/git/bootstrapping" >> submit
echo "remote_initialdir     = /vol/users/users/dklaes/git/bootstrapping" >> submit
echo 'Requirements = (Memory > 1500)' >> submit
echo "" >> submit

i=${NRELSTART}
while [ ${i} -le ${NRELSTOP} ]
do
 echo "Arguments  = ${MAIND} ${i}" >> submit
 echo "Log        = ${MAIND}/log/realisation_${i}.log" >> submit
 echo "Output     = ${MAIND}/output/realisation_${i}.out" >> submit
 echo "Error      = ${MAIND}/error/realisation_${i}.err" >> submit
 echo "Queue" >> submit
 echo "" >> submit
  
  i=$(( $i + 1 ))
done
