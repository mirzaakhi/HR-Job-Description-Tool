# Job Description Tool with Chatbot

## Overview
The Job Description Tool with Chatbot is a Streamlit-based application designed to generate comprehensive job descriptions using ChatGPT. Users can create, refine, and download job descriptions customized to specific criteria, such as responsibilities, qualifications, and skills.

## Features
- **Job Summary**: Overview of the job position.
- **Key Responsibilities**: Define the major duties of the role.
- **Required Qualifications**: Specify essential qualifications and certifications.
- **Skills & Experience**: Highlight the required skills and experience for the role.
- **Refine Job Description**: Fine-tune job descriptions using ChatGPT.
- **Download as PDF**: Export the final job description as a PDF.

## AWS Infrastructure Components

- **EC2 (Elastic Compute Cloud)**: Hosts the application on a virtual machine instance. The public IP for accessing the deployed app is [http://54.224.25.176:8501](http://54.224.25.176:8501).
- **ALB (Application Load Balancer)**: Distributes traffic across the application, ensuring scalability and high availability.
- **ECS (Elastic Container Service)**: Manages and conducts Docker containers for future deployments with **Fargate**.
- **ECR (Elastic Container Registry)**: Stores Docker images for deployment in **ECS**.
- **IAM Role**: Manages access and permissions for AWS resources used by the application.

## Installation on AWS EC2

To set up the HR Job Description Tool on an **AWS EC2 instance**, follow these high-level steps:

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
- Use the sidebar to navigate through the different sections of the job description.
- Generate a job description based on input criteria and download it as a PDF.

## License

This project is licensed under the MIT License.
