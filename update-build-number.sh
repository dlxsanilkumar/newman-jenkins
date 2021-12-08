#!/bin/bash

sed -i 's/Migration/Migration-'$BUILD_NUMBER'/g' tests/Delixus.postman_collection.json
