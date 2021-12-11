import os
import requests

class Scan:

    def __init__(self, filename, count):
        self.filename = "filename.txt"
        self.count = "count.txt"

    # Delete the filename.txt if exists.
    def delete_file(filename):
        if os.path.exists(filename):
            print ("Deleting", filename, "\n")
            os.remove(filename)

    # Copy name of the solidity files into filename.txt
    def name_of_solidity_files(filename):
        for files in os.scandir("./contracts"):
            if files.is_file():
                with open(filename, "a") as file:
                    file.write(files.name + "\n")

    # Read the file.
    def get_number_of_solidity_files(filename, count):
        line_count = 1
        print("-- Searching for the solidity files --\n")
        with open(filename, "r") as f:
            for line in f:
                file_name = line.split()
                print("Solidity file", line_count, ":", file_name[0])
                # Get the number of files scanned.
                with open(count, "w") as file:
                    file.write(str(line_count))
                # print(line_count)
                line_count += 1
        print("\n-- Search completed --")

    # Scan solidity files.
    def start_scan(filename):
        with open(filename, "r") as f:
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

Scan.delete_file("filename.txt")
Scan.name_of_solidity_files("filename.txt")
Scan.get_number_of_solidity_files("filename.txt", "count.txt")
Scan.start_scan("filename.txt")
