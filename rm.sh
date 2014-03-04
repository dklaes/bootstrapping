MD=$1

i=1
while [ ${i} -le 10000 ]
do
	echo ${i}
	FOLDER=${MD}/bootstrapping/realisation_${i}
	rm ${FOLDER}/chip_?.csv ${FOLDER}/chip_??.csv ${FOLDER}/chip_all.cov
	i=$(( ${i}+1 ))
done
