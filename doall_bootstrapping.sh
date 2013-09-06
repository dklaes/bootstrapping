for FOLDER in `ls -1 /vol/euclid1/euclid1_raid1/dklaes/data/bootstrapping/ | grep run`
do
	echo ${FOLDER}
	./bootstrapping.sh /vol/euclid1/euclid1_raid1/dklaes/data/bootstrapping/${FOLDER}/ 32 10000
done
