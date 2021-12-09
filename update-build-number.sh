#!/bin/bash

sed -i 's/scanName=Migration/scanName=Migration-'$BUILD_NUMBER'/g' tests/Delixus.postman_collection.json
