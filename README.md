# Job Description Tool with Chatbot

## Overview
The **Job Description Tool with Chatbot** is a Streamlit-based application designed to generate comprehensive job descriptions using ChatGPT. It integrates with OpenAI's GPT model to help refine job descriptions, making it easy to create and modify job postings efficiently. Users can generate, refine, and download customized job descriptions based on specific criteria such as responsibilities, qualifications, and skills.

## Features
- **Job Summary**: Overview of the job position.
- **Key Responsibilities**: Define the significant duties of the role.
- **Required Qualifications**: Specify essential qualifications and certifications.
- **Skills & Experience**: Highlight the required skills and experience for the role.
- **How to Apply**: Provide instructions on how candidates can apply for the role, including application email, deadline, and additional instructions.
- **Refine Job Description**: Fine-tune job descriptions using ChatGPT.
- **Download as PDF**: Export the final job description as a PDF.

## Required Tools and Platforms

Before starting, ensure the following tools and platforms are set up and available:

- **Python 3.8+**: This is for running the application locally or on an EC2 instance.
- **Docker**: This is for containerizing and running the application in a Docker environment.
- **VSCode**: This is for development purposes. Make sure to install the necessary extensions:
  - Python Extension
  - Docker Extension
- **AWS Account**: Required for deploying the application to AWS services (EC2, ECR, ECS, ALB, IAM).


## AWS Infrastructure Components

- **EC2 (Elastic Compute Cloud)**: Hosts the application on a virtual machine instance. The public IP for accessing the deployed app is [http://54.224.25.176:8501](http://54.224.25.176:8501).
- **ALB (Application Load Balancer)**: Distributes traffic across the application, ensuring scalability and high availability.
- **ECS (Elastic Container Service)**: Manages and conducts Docker containers for future deployments with **Fargate**.
- **ECR (Elastic Container Registry)**: Stores Docker images for deployment in **ECS**.
- **IAM Role**: Manages access and permissions for AWS resources used by the application.

## Installation on AWS EC2

To set up the Job Description Tool with Chatbot on an **AWS EC2 instance**, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone <REPO_LINK>
    cd <PROJECT_REPO>
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**:
    ```bash
    streamlit run app.py
    ```
## Docker Setup

To run the application inside a Docker container:

1. **Build the Docker image**:
    ```bash
    docker build -t hr-job-description-tool .
    ```

2. **Run the Docker container**:
    ```bash
    docker run -d -p 8501:8501 hr-job-description-tool
    ```
    
## Usage

- Access the application using the public IP address of the EC2 instance on port **8501**.
- Use the Next and Back buttons to navigate through sections such as 'Job Summary,' 'Key Responsibilities,' and 'Skills & Experience.'
- Generate a job description based on user input using OpenAI/ChatGPT, refine it further with ChatGPT, and download the final refined version as a PDF

## License

This project is licensed under the MIT License.
