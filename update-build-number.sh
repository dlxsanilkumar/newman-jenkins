#!/bin/bash

sed -i 's/Pipeline/Pipeline-'$BUILD_NUMBER'/g' tests/Delixus.postman_collection.json
