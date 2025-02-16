#!/bin/bash
# Fail on any error
set -e

# Upgrade the database in case of existing old schema
airflow db upgrade

# Create a default user (skip this if you already have a user setup)
airflow users create \
  --username admin \
  --firstname adminf \
  --lastname adminl \
  --role Admin \
  --email zhangzz1218@gmail.com \
  --password 123123

# Start the web server, default port is 8080
# -p option specifies the port on which the webserver will run
airflow webserver -p 8080
