#!/bin/bash

psql -h 13.126.95.15 -p 5432 -U postgres -d solidityscan -w -c "SELECT status FROM build_ids ORDER BY id DESC LIMIT `cat count.txt`" > build.log 2>&1;
BUILD_STATUS=`awk 'FNR == 3 {print $1}' build.log;`

# Fail build, if vulnPresent.
res=`grep ERROR: build.log | awk '{ print $1 }' | tail -1`

if [ "$BUILD_STATUS" = "FAILURE"  ]; then
   echo "BUILD FAILURE !"
   exit 1;
else
   echo "BUILD SUCCESS"
fi