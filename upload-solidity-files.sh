#!/bin/bash

# Copy the solidiy files to the server.
scp -i ~/.ssh/mythril-scan-key.pem ~/Migrations.sol ubuntu@13.126.95.15:/data/delixus/;
scp -i ~/.ssh/mythril-scan-key.pem ~/Adoption.sol ubuntu@13.126.95.15:/data/delixus/;
scp -i ~/.ssh/mythril-scan-key.pem ~/odd_even.sol ubuntu@13.126.95.15:/data/delixus/;