# DevOps Challenge Project

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Features](#features)
- [Security Measures](#security-measures)
- [API Endpoints](#api-endpoints)
- [Continuous Integration](#continuous-integration)
- [Docker Compose](#docker-compose)
- [Logs](#logs)

## Introduction

This project serves as a proof-of-concept Flask API that securely fetches a secret code from a local DynamoDB table and exposes it via a web server. The service is containerized with Docker and is designed to be scalable and secure.

## Getting Started

To get the application running:

1. Clone the repository.
2. Run `docker-compose up` from the root directory.

## Features

- **Health Check:** Allows monitoring of the API's status.
- **Rate Limiting:** Adds a rate limit to API requests to prevent abuse.
- **Logging:** Captures all activities and logs them to `audit.log`.

## Security Measures

- **JWT Authentication:** Uses JWT (JSON Web Tokens) for secure, stateless authentication.
- **Environment Variables:** Sensible defaults are overridden by environment variables for better security.
- **Rate Limiting:** Limits the number of requests to the API, preventing abuse.
- **HTTPS:** (Optional) Can be deployed with HTTPS to ensure data encryption in transit.

## API Endpoints

- **GET /health:** Returns the health status of the application.
- **GET /token:** Generates and returns a JWT token.
- **GET /secret:** Fetches the secret from the DynamoDB table, requires JWT token for authentication.

## Continuous Integration

We use a CI pipeline to ensure the quality and security of the code. Every commit triggers automated tests and code scans for vulnerabilities. For details, refer to the `.yml` configuration file in the repository.

Note: If you need further information or code snippets, feel free to ask.

## Docker Compose

The `docker-compose.yml` file is used to define and run the multi-container Docker applications. This makes it easier to manage both the Flask application and the DynamoDB instance in a secure and isolated environment.

Note: If you need the docker-compose code explained, feel free to ask.

## Logs

The service logs all the important activities and saves them to `audit.log`. Check this log file for historical data and auditing.
