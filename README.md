# Flask Token Provider

## Introduction
The Flask Token Provider is a lightweight Flask application that provides two endpoints for generating and validating tokens. This project is designed to offer a simple and secure way to generate tokens with specified expiration times and verify their validity.

## Requirements
- Docker
- Docker Compose

## How to Start the Project
1. Clone the repository to your local machine.
2. This project contains a "config.xml" file, modify the config file with your preferred variables.
3. Build and start the containers by executing the start.sh bash script.

 ```bash
bash start.sh
```
4. Verify containers are running
 ```bash
docker-compose ps
```
   
## Configuration Variables

The `config.xml` file contains the following environmental variables used in the Flask Lightweight Token Service:

- `POSTGRESQL_USERNAME`: The username for the PostgreSQL database.
- `POSTGRESQL_PASSWORD`: The password for the PostgreSQL database.
- `POSTGRESQL_DB_NAME`: The name of the PostgreSQL database.
- `POSTGRESQL_HOST`: The hostname or IP address of the PostgreSQL database. (this must be same with service name of postgresql image in docker-compose or bridge ip of docker.
- `POSTGRESQL_DB_PORT`: The port number for the PostgreSQL database.
- `TOKEN_EXPIRATION_TIME`: The time, in seconds, until the generated token expires.
- `TOKEN_CLEAR_FREQUENCY`: The frequency, in seconds, for the token clearer job to run and remove expired tokens from the database.
- `LOG_LEVEL`: The logging level for the Flask app (e.g., DEBUG, INFO, WARNING, ERROR).
- `POSTGRESQL_SSL_MODE`: The SSL mode for the PostgreSQL connection (e.g., require, verify-ca, verify-full).
- `BACKEND_APP_PORT`: The port number on which the Flask app runs.

Make sure to set these variables with appropriate values to configure the Flask Lightweight Token Service according to your needs.

## Endpoints
1. **Generate Token**

- Endpoint: `/generate_token`
- Method: POST
- Parameters: None
- Description: This endpoint generates a new token and returns it as a response.

2. **Verify Token**

- Endpoint: `/verify_token`
- Method: GET
- Authorization Layer: The `Authorization` header should be in the format `"Bearer xxx-xxx"`, where `xxx-xxx` is the token to be verified.
- Description: This endpoint verifies the validity of the provided token. It checks if the token exists in the database and if it has not expired.

## Return Types
1. **Generate Token**

- On success: Returns a JSON object containing the generated token.  
  Example:
  ```
  {"token": "f26c57d9-ec8c-b2dc-b90d-5891ee72ef6a"}
  ```

2. **Verify Token**

- On success: Returns a JSON object indicating if the token is valid.  
  Example:
  ```
  {"valid": true}
  ```

## TO-DO List
- Store token hashes instead of UUIDs
- Enforce secure communication using TLS/SSL
- Implement optional one time use mechanism.
- Use HTTPS
- Sanitize and validate user inputs to prevent SQL Injection.
- Implement an autodeploy bash script to deploy the Flask Token Provider to a remote machine automatically.
- Implement IP Blacklist & Whitelist to restrict or allow specific IP addresses from accessing the endpoints.
- Add api-level tests besides of function level tests for the Flask application to ensure the functionality is working as expected.
- Implement rate limiting to prevent abuse and ensure fair usage of the endpoints.
- Enhance the logging mechanism to provide more detailed information about the application's behavior.
- Stress testings, make sure gunicorn is sufficient
- Proxying
- Create log files and log security events there.

Feel free to contribute to the project and help improve its functionality and security. If you have any suggestions or feature requests, please open an issue or submit a pull request.

