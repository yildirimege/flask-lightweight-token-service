#!/bin/bash

# Parse the config.xml file and set environment variables
CONFIG_FILE="config.xml"

# Function to extract value of an XML tag
get_xml_value() {
    echo "$(grep "<$1>" "$CONFIG_FILE" | sed -E "s#.*<$1>(.*)</$1>.*#\1#")"
}

# Set environment variables
export POSTGRESQL_USERNAME=$(get_xml_value "POSTGRESQL_USERNAME")
export POSTGRESQL_PASSWORD=$(get_xml_value "POSTGRESQL_PASSWORD")
export POSTGRESQL_DB_NAME=$(get_xml_value "POSTGRESQL_DB_NAME")
export POSTGRESQL_HOST=$(get_xml_value "POSTGRESQL_HOST")
export POSTGRESQL_DB_PORT=$(get_xml_value "POSTGRESQL_DB_PORT")
export TOKEN_EXPIRATION_TIME=$(get_xml_value "TOKEN_EXPIRATION_TIME")
export TOKEN_CLEAR_FREQUENCY=$(get_xml_value "TOKEN_CLEAR_FREQUENCY")
export POSTGRESQL_SSL_MODE=$(get_xml_value "POSTGRESQL_SSL_MODE")
export BACKEND_APP_PORT=$(get_xml_value "BACKEND_APP_PORT")


# Print the parsed environment variables
echo "DB_USER: $POSTGRESQL_USERNAME"
echo "DB_PASSWORD: $POSTGRESQL_PASSWORD"
echo "DB_NAME: $POSTGRESQL_DB_NAME"
echo "DB_HOST: $POSTGRESQL_HOST"
echo "DB_PORT: $POSTGRESQL_DB_PORT"
echo "BACKEND_APP_PORT: $BACKEND_APP_PORT"
echo "TOKEN_EXPIRATION_TIME: $TOKEN_EXPIRATION_TIME"
echo "TOKEN_CLEAR_FREQUENCY: $TOKEN_CLEAR_FREQUENCY"
echo "POSTGRESQL_SSL_MODE: $POSTGRESQL_SSL_MODE"


# Run docker-compose
docker-compose up --build -d
