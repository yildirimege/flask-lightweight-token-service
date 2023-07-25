# Flask Token Provider

## Introduction
The Flask Token Provider is a lightweight Flask application that provides two endpoints for generating and validating tokens. This project is designed to offer a simple and secure way to generate tokens with specified expiration times and verify their validity.

## Requirements
To run this project, you need to have Docker installed on your system.

## How to Start the Project
1. Clone the repository to your local machine.
2. In the root directory of the project, run the following command to start the containers using Docker Compose:


 ```bash
docker-compose up --build -d
```

3. The project uses PostgreSQL as the database. Make sure to provide the required PostgreSQL credentials as environment variables in the `docker-compose.yml` file.

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
- Implement an autodeploy bash script to deploy the Flask Token Provider to a remote machine automatically.
- Implement IP Blacklist & Whitelist to restrict or allow specific IP addresses from accessing the endpoints.
- Add api-level tests besides of function level tests for the Flask application to ensure the functionality is working as expected.
- Implement rate limiting to prevent abuse and ensure fair usage of the endpoints.
- Enhance the logging mechanism to provide more detailed information about the application's behavior.

Feel free to contribute to the project and help improve its functionality and security. If you have any suggestions or feature requests, please open an issue or submit a pull request.

