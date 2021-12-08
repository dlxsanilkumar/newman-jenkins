#!/bin/bash

psql -h 13.126.95.15 -p 5432 -U postgres -d solidityscan -w -c "SELECT result FROM solidityscans ORDER BY scanid DESC LIMIT 1" > result.log 2>&1;
GET_VULN_DATA=`awk 'FNR == 3 {print $1}' result.log;`

case $GET_VULN_DATA in
     *vulnPresent*) 
     echo "Build failed, because there is one or more vulnerabilities found during the scan."
	 echo "See the details below for more information."

	 echo "--- insert into build_ids table ---"
	 psql -h 13.126.95.15 -p 5432 -U postgres -d solidityscan -w -c "INSERT INTO build_ids (build_id, jobname_TEST, status) VALUES (${BUILD_NUMBER}, '${JOB_NAME}', 'FAILURE');" > db.log 2>&1;
	 psql -h 13.126.95.15 -p 5432 -U postgres -d solidityscan -w -c "SELECT * FROM solidityscans ORDER BY scanid DESC LIMIT 1";
	 psql -h 13.126.95.15 -p 5432 -U postgres -d solidityscan -w -c "SELECT * FROM build_ids ORDER BY id DESC LIMIT 1"; exit 1;
	 ;;
     *)
     echo Build is completed successfully...
	 
	 echo "--- insert into build_ids table ---"
	 psql -h 13.126.95.15 -p 5432 -U postgres -d solidityscan -w -c "INSERT INTO build_ids (build_id, jobname, status) VALUES (${BUILD_NUMBER}, '${JOB_NAME}', 'SUCCESS');" > db.log 2>&1;
	 psql -h 13.126.95.15 -p 5432 -U postgres -d solidityscan -w -c "SELECT * FROM solidityscans ORDER BY scanid DESC LIMIT 1";
	 psql -h 13.126.95.15 -p 5432 -U postgres -d solidityscan -w -c "SELECT * FROM build_ids ORDER BY id DESC LIMIT 1"; exit 0;
	 ;;
esac

# Fail build, if database update fails.
res=`grep ERROR: db.log | awk '{ print $1 }' | tail -1`

if [ "$res" = "ERROR:"  ]; then
   echo "Database error!"
   exit 1;
else
   echo "Database updated."
   # exit 0;
fi

