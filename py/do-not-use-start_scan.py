import os
import requests

# Delete the filename.txt if exists.
if os.path.exists("filename.txt"):
    print("Deleting filename.txt")
    os.remove("filename.txt")

# Copy name of the solidity files into filename.txt
for files in os.scandir('./contracts'):
    if files.is_file():
        # print(files.name)
        with open("filename.txt", "a") as file:
            file.write(files.name + "\n")

# Read the file.
line_count = 1
print("-- Searching for the solidity files --\n")
with open("filename.txt", "r") as f:
    for line in f:
        file_name = line.split()
        print("Solidity file", line_count, ":", file_name[0])
        # Get the number of files scanned.
        with open("count.txt", "w") as file:
            file.write(str(line_count))
        # print(line_count)
        line_count += 1
print("\n-- Search completed --")

# Scan solidity files.
with open("filename.txt", "r") as f:
    for line in f:
        file_name=line.split()
        # print("Solidity file", line_count, ":", file_name[0])
        print("\n** Scanning :", file_name[0])
        # response = requests.get("http://13.126.95.15/api/startScan?solidityFile=delixus-contact.sol&basePath=/data/delixus&scanName=Delixus")
        API = "http://13.126.95.15/api/startScan?solidityFile=" + file_name[0] + "&basePath=/data/delixus&scanName=Delixus"
        response = requests.get(API)
        print(response.text)
        if response.status_code != 200:
            print("ERROR:",response.status_code,":", file_name[0], "file not scanned successfully.")
            break
        else:
            print("RESPONSE CODE:",response.status_code,":", file_name[0], "file scanned successfully.")
