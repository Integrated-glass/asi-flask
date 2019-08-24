#!/bin/bash

db_service_name="ustart-db"

# If container is not already running - run it
if ! docker ps --format "{{.Names}}" | grep -w $db_service_name &> /dev/null; then

  get_env_var_val () {
    IFS="=" read -ra parsed <<< $1

    echo ${parsed[1]}
  }

  # Export environment variables for the docker service
  export $(cat ../docker/.env | xargs)

  # Start DB service
  docker-compose -f ../docker/docker-compose.yml run -d --name $db_service_name $db_service_name

  # Get IP address of the DB container
  containerIP=$(docker inspect --format="{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" $db_service_name)

  # Set up connection string
  export DATABASE_URL="postgresql://${LIBR_DB_LOGIN}:${LIBR_DB_PASSWORD}@${containerIP}:${LIBR_DB_PORT}/${LIBR_DB_NAME}"

  # Await until the DB starts
  ../docker/wait-for/wait-for "${containerIP}:${LIBR_DB_PORT}" -- echo "DB container initialized with address ${containerIP}"
fi
