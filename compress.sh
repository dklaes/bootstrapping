#!/bin/bash

MAIND=$1
RUN=$2

cd ${MAIND}/${RUN}/bootstrapping
mkdir /media/BACKUP/bootstrapping_with_error/${RUN}

for FOLDER in `ls`
do
	echo ${FOLDER}
	tar -czf /media/BACKUP/bootstrapping_with_error/${RUN}/${FOLDER}.tar.gz ${FOLDER}

	rm ${FOLDER}/*.cat &
done

tar -czf /media/BACKUP/bootstrapping_with_error/${RUN}/error.tar.gz error && rm -r error &
tar -czf /media/BACKUP/bootstrapping_with_error/${RUN}/output.tar.gz output && rm -r output &
tar -czf /media/BACKUP/bootstrapping_with_error/${RUN}/log.tar.gz log && rm -r log &

