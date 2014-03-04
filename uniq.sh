i=1

while [ ${i} -le 10000 ]
do
	echo $i
	cat /vol/aibn41/aibn41_1/dklaes/bootstrapping_masterthesis/run_12_12_f/bootstrapping/realisation_${i}/chip_all.csv | sort -n | uniq > /vol/aibn41/aibn41_1/dklaes/bootstrapping_masterthesis/run_12_12_f/pre_uniq.txt
	cat /vol/aibn41/aibn41_1/dklaes/bootstrapping_masterthesis/run_12_12_f/pre_uniq.txt /vol/aibn41/aibn41_1/dklaes/bootstrapping_masterthesis/run_12_12_f/pre_uniq2.txt | sort -n | uniq > /vol/aibn41/aibn41_1/dklaes/bootstrapping_masterthesis/run_12_12_f/uniq.txt
	cp /vol/aibn41/aibn41_1/dklaes/bootstrapping_masterthesis/run_12_12_f/uniq.txt /vol/aibn41/aibn41_1/dklaes/bootstrapping_masterthesis/run_12_12_f/pre_uniq2.txt
	i=$(( $i+1 ))
done
