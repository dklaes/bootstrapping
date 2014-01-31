# Script for creating condor submission file

# $1 = main directory where the files are
# $2 = number of realisations
# $3 = name of submit file

MAIND=$1
NREL=$2
OUTFILE=$3

if [ ! -d "${MAIND}/bootstrapping" ]; then
  mkdir ${MAIND}/bootstrapping
  mkdir ${MAIND}/log
  mkdir ${MAIND}/error
  mkdir ${MAIND}/output
fi

echo "Universe   = vanilla" > ${MAIND}/${OUTFILE}
echo "initialdir     = /vol/users/users/dklaes/git/bootstrapping" >> ${MAIND}/${OUTFILE}
echo "transfer_input_files = ldac.py, bootstrapping.py, illum_correction_fit.py, illum_ldactools.py" >> ${MAIND}/${OUTFILE}
echo "Executable = /vol/users/users/dklaes/git/bootstrapping/bootstrapping.sh" >> ${MAIND}/${OUTFILE}
echo 'Requirements = (Memory > 1500)' >> ${MAIND}/${OUTFILE}
echo "" >> ${MAIND}/${OUTFILE}

echo "Arguments  = ${MAIND} \$(Cluster).\$(Process)" >> ${MAIND}/${OUTFILE}
echo "Log        = ${MAIND}/log/realisation_\$(Cluster).\$(Process).log" >> ${MAIND}/${OUTFILE}
echo "Output     = ${MAIND}/output/realisation_\$(Clutser).\$(Process).out" >> ${MAIND}/${OUTFILE}
echo "Error      = ${MAIND}/error/realisation_\$(Cluster).\$(Process).err" >> ${MAIND}/${OUTFILE}
echo "Queue ${NREL}" >> ${MAIND}/${OUTFILE}
