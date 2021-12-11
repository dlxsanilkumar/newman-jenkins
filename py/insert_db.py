import os
import csv
import sys
import time
import psycopg2

'''
-- Install psycopg2 from Ubuntu repo --
* How to execute.
* cd into the project root directory. 
python3 py/insert-db.py

-- Set environment variable if they are not exists --
* Below is the example to create one variable for "HOSTNAME", similarly create all variables.
* Example:
export HOSTNAME=localhost

-- Jenkins variables --
* The BUILD_NUMBER and JOB_NAME are already been set in Jenkins by default.
* So, no need to create them again.
'''

# Get environment variables.
DB_HOSTNAME = 'HOSTNAME'
DB_NAME = 'DATABASE'
DB_USERNAME = 'USER'
DB_PASSWORD = 'PASSWORD'
DB_PORT = 'PORT'
JENKINS_BUILD_NUMBER = 'BUILD_NUMBER'
JENKINS_JOB_NAME = 'JOB_NAME'

conn = None
cur = None

def BUILD_SUCCESS_MESSAGE():
    return '''Build is completed successfully...\n'''

def BUILD_FAILURE_MESSAGE ():
    return '''Build failed, because there is one or more vulnerabilities found during the scan.
See the details below for more information.\n'''

def DATA_FROM_SOLIDITYSCANS_TABLE():
    return '''-- Data from solidityscans table --'''

def DATA_FROM_BUILD_IDS_TABLE():
    return '''\n-- Data from build_ids table --'''

def NO_STATUS():
    return '''ERROR: No vulnStatus found!\n'''

with open("count.txt", "r") as file:
    SQL_QUERY_NUMBER = file.read()
    CHECK_SQL_QUERY_NUMBER = int(SQL_QUERY_NUMBER)
    if CHECK_SQL_QUERY_NUMBER == 0:
        print("ERROR : SQL_QUERY_NUMBER -", + CHECK_SQL_QUERY_NUMBER)
        sys.exit()
    else:
        pass

try:
    # Database connection
    conn = psycopg2.connect(
        host = os.getenv(DB_HOSTNAME),
        dbname = os.getenv(DB_NAME),
        user = os.getenv(DB_USERNAME),
        password = os.getenv(DB_PASSWORD),
        port = os.getenv(DB_PORT))

    print("Database connected successfully")

    cur = conn.cursor()

    # Delete the filename.txt if exists.
    if os.path.exists("vulnData.txt"):
        print("Deleting vulnData.txt")
        os.remove("vulnData.txt")    

    ''' Get the scan result from this table.
    The result will be "vulnPresent" or "vulnNotPresent".
    If both are not found, it will exit with error message 
    as `ERROR: No vulnStatus found!`'''
    
    #print(SQL_QUERY_NUMBER)
    # cur.execute("SELECT result FROM solidityscans ORDER BY scanid DESC LIMIT " + SQL_QUERY_NUMBER)
    # for result in cur.fetchall():
    #     vulndata = str(result[0])
    #     print(vulndata)
    # vulndata = "delete"
    # sql = """SELECT result FROM solidityscans ORDER BY scanid DESC LIMIT 2"""
        
    cur.execute("SELECT result FROM solidityscans ORDER BY scanid DESC LIMIT " + SQL_QUERY_NUMBER)
    with open("vulnData.txt", "w", newline='') as f:
        wrtr = csv.writer(f)
        for result in cur.fetchall():
            vulndata = result
            wrtr.writerow(vulndata)

    # Execute this block if 'vulnPresent' in vulnData.txt
    with open('vulnData.txt') as f:
        if 'vulnPresent' in f.read():
            print(BUILD_FAILURE_MESSAGE())
            # Insert data into this table if vulnerabilities found during the scan. 
            print("-- Insert into build_ids --")
            INSERT_INTO_BUILD_IDS = "INSERT INTO build_ids (build_id, jobname, status) VALUES (%s, %s, %s)"
            INSERT_VALUES_INTO_BUILD_IDS = [os.getenv(JENKINS_BUILD_NUMBER), os.getenv(JENKINS_JOB_NAME),  'FAILURE']
            cur.execute(INSERT_INTO_BUILD_IDS, INSERT_VALUES_INTO_BUILD_IDS)

            print(DATA_FROM_SOLIDITYSCANS_TABLE())
            cur.execute("SELECT * FROM solidityscans ORDER BY scanid DESC LIMIT " + SQL_QUERY_NUMBER)
            for solidityscans in cur.fetchall():            
                print(solidityscans)

            print(DATA_FROM_BUILD_IDS_TABLE())
            cur.execute("SELECT * FROM build_ids ORDER BY id DESC LIMIT 1")
            for build_ids in cur.fetchall():
                print(build_ids)
                

    # Execute this block if 'vulnNotPresent' in vulnData.txt file.
    with open('vulnData.txt') as f:
        if 'vulnNotPresent' in f.read():
            print(BUILD_SUCCESS_MESSAGE())
            # Insert data into this table if no vulnerabilities found during the scan. 
            print("-- Insert into build_ids --")
            INSERT_INTO_BUILD_IDS = "INSERT INTO build_ids (build_id, jobname, status) VALUES (%s, %s, %s)"
            INSERT_VALUES_INTO_BUILD_IDS = [os.getenv(JENKINS_BUILD_NUMBER), os.getenv(JENKINS_JOB_NAME), 'SUCCESS']
            cur.execute(INSERT_INTO_BUILD_IDS, INSERT_VALUES_INTO_BUILD_IDS)

            print(DATA_FROM_SOLIDITYSCANS_TABLE())
            cur.execute("SELECT * FROM solidityscans ORDER BY scanid DESC LIMIT " + SQL_QUERY_NUMBER)
            for solidityscans in cur.fetchall():            
                print(solidityscans)

            print(DATA_FROM_BUILD_IDS_TABLE())
            cur.execute("SELECT * FROM build_ids ORDER BY id DESC LIMIT 1")
            for build_ids in cur.fetchall():
                print(build_ids)
                sys.exit()

    # Execute this block if 'vulnNotPresent' in vulnData.txt file.
    with open('vulnData.txt') as f:
        if "" in f.read():
            print("ERROR: vulnStatus not found!")

except Exception as error:
    print(error)
finally:
    if cur is not None:    
        cur.close()
    if conn is not None:    
        conn.close()
