#!/bin/bash

MAIND=$1
RUN=$2

cd ${MAIND}
mkdir /media/BACKUP/bootstrapping_with_error/${RUN}

for FOLDER in `ls ${MAIND}`
do
	echo ${FOLDER}
	tar -czf /media/BACKUP/bootstrapping_with_error/${RUN}/${FOLDER}.tar.gz ${FOLDER}

	rm ${FOLDER}/*.cat &
done
