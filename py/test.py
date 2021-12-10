import os
  
# environment variable
db_hostname = 'HOSTNAME'
db_name = 'DATABASE'
db_port = 'PORT'
db_user = 'USER'

print('Database hostname: ' + os.getenv(db_hostname))
print('Database port: ' + os.getenv(db_port))
print('Database name: ' + os.getenv(db_name))
print('Database user: ' + os.getenv(db_user))
