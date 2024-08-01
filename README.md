# Cloud Resume API Project

Welcome to my project for the Cloud Resume API Challenge. This project provides an opportunity to build and deploy a serverless API using different cloud providers (GCP in this case), integrated with GitHub Actions for CI/CD. The primary goal? Construct an API that can serve resume data in JSON format.

## Challenge Objective 🎯

The task is to create a Serverless function that fetches resume data stored in a NoSQL Database and returns it in JSON format. Integrate GitHub Actions to automatically deploy updates to your Cloud Serverless function whenever you push to your repository.

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) installed. (Or OpenTofu)
- A Google Cloud Platform (GCP) account with the necessary permissions
- Service account with the necessary IAM roles
- S3-compatible storage for Terraform state (e.g., Linode Object Storage)

## Project Structure

- `terraform/`: Directory containing the terraform code for the resources.
- `main.tf`: The main Terraform configuration file.
- `iam.tf`: The main Terraform IAM configuration file.
- `lambda.tf`: Contains the lambda configuration file.
- `vars.tf`: Contains the variable definitions.
- `lambda/`: Directory containing the source code for the cloud function.
- `lambda/main.py`: file containing the source code for the cloud function.
- `lambda/requirements.txt`: file containing the source code dependencies for the cloud function.

