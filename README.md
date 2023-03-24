<br />
<div align="center">
  <h1 align="center">DRF-API-ML-Template</h1>

  <p align="center">
    ( Version 1.0.0 )
    <br>
    <a href="http://0.0.0.0:8000/redoc">Redoc</a>
    ·
    <a href="http://0.0.0.0:8000/swagger">Swagger</a>
    ·
    <a href="https://github.com/Y4rd13/DRF-API-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/Y4rd13/DRF-API-Template/issues">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation-&-deployment">Installation & Deployment</a></li>
      </ul>
    </li>
    <li>
        <a href="#usage-of-the-api">Usage of the API</a>
        <ul>
            <li><a href="#endpoints">Endpoints</a></li>
              <ul>
                <li><a href="#post-apitoken">/token</a></li>
                <li><a href="#post-apitokenrefresh">/token/refresh</a></li>
                <li><a href="#post-apiusercreate">/user/create</a></li>
                <li><a href="#post-custom-service">/v1/custom/service</a></li>
              </ul>
        </ul>
    </li>
  </ol>
</details>

# About the Project

This project is a Custom Template for DRF Rest-API for ML/DL purpose, with using a custom service for the endpoint. The API is built in Django REST framework, Redis, Celery, MongoDB, Simple-JWT and Docker (docker-compose).
Using this template, you can easily create a new API with a custom service with a few steps.

# Getting Started

## Prerequisites

- Docker
- Docker Compose
- Ubuntu 20.04 LTS or higher

## Installation & Deployment

1. Clone the repository:
   ```sh
   git clone https://github.com/Y4rd13/DRF-API-Template.git
   ```
2. Set the environment variables
3. Deploy the application using Docker Compose
   ```sh
   docker-compose -f docker-compose up
   ```

# Usage of the API

## Authentication

This API uses authentication through API Key. The security scheme type is API Key and the header parameter name is Authorization. There are two types of tokens: token and token_create, both are required.

## **Endpoints**

### **POST /api/token**

Create a new access token.

**Request Body**

- AUTHORIZATIONS: `Auth_Token_Bearer_JWT_`
- REQUEST BODY SCHEMA: `application/json`

```json
{
  "username": "string",
  "password": "string"
}
```

**Responses**

- 201: Success response:
  - `username`: required, string (Username) non-empty
  - `password`: required, string (Password) non-empty
- 400:
  - Error response

### **POST api/token/refresh**

Create a new access token from a refresh token.

**Request Body**

- AUTHORIZATIONS: `Auth_Token_Bearer_JWT_`
- REQUEST BODY SCHEMA: `application/json`

```json
{
  "refresh": "string"
}
```

**Responses**

- 201: Success response:
  - `refresh`: required, string (Refresh) non-empty
  - `access`: string (Access) non-empty
- 400:
  - Error response

### **POST api/user/create**

Create a new user account.

**Request Body**

- AUTHORIZATIONS: `Auth_Token_Bearer_JWT_`
- REQUEST BODY SCHEMA: `application/json`

```json
{
  "email": "user@example.com", // non-empty
  "username": "string", // [ 1 .. 150 ] characters
  "password": "string", // [ 1 .. 50 ] characters
  "account_type": "string",
  "token": "string" // non-empty
}
```

**Responses**

- 201: Success response:
  ```json
  {
    "data": "string",
    "code": 0,
    "status": "string"
  }
  ```
- 400: Error response:
  ```json
  {
    "message": "string",
    "code": 0,
    "status": "string",
    "error": "string"
  }
  ```

### **POST /api/v1/custom/service**

Custom service endpoint.

**Query Parameters**

- AUTHORIZATIONS: `Auth_Token_Bearer_JWT`

```json
{
  "my_variable": "string", # required
  "other_variable_1": "JsonField", # not required (allow_blank=True)
  "other_variable_2" "string" # not required (allow_blank=True)
}
```

**CURL**

```bash
curl --location 'http://0.0.0.0:8000/api/v1/custom/service' \
--header 'Authorization: Bearer {jtw_token}' \
--header 'Content-Type: application/json' \
--data '{
    "my_variable": "string",
    "other_variable_1": {
        "key": "value"
    },
    "other_variable_2": "string"
}'
```

**Python**

```python
import requests
import json

url = "http://0.0.0.0:8000/api/v1/custom/service"

payload = json.dumps({
   "my_variable": "string",
    "other_variable_1": {
        "key": "value"
    },
    "other_variable_2": "string"
})
headers = {
  'Authorization': 'Bearer {jtw_token}',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

**JavaScript - Fetch**

```javascript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer {jtw_token}");
myHeaders.append("Content-Type", "application/json");

var raw = JSON.stringify({
  custom_variable: "string",
  other_variable_1: {
    key: "value",
  },
  other_variable_2: "string",
});

var requestOptions = {
  method: "POST",
  headers: myHeaders,
  body: raw,
  redirect: "follow",
};

fetch("http://0.0.0.0:8000/api/v1/custom/service", requestOptions)
  .then((response) => response.text())
  .then((result) => console.log(result))
  .catch((error) => console.log("error", error));
```

**Responses**

- 200: Success response:
  ```json
  {
    "data": "string",
    "code": 0,
    "status": "string"
  }
  ```
- 400: Error response:
  ```json
  {
    "message": "string",
    "code": 0,
    "status": "string",
    "error": "string"
  }
  ```
