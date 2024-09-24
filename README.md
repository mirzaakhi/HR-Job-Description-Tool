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
- **ECS (Elastic Container Service)**: Manages and orchestrates Docker containers for future deployments with **Fargate**.
- **ECR (Elastic Container Registry)**: Stores Docker images for deployment in **ECS**.
- **IAM Role**: Manages access and permissions for AWS resources used by the application.

## Installation on AWS EC2

### Step-by-step Guide to Set up EC2 and Deploy Application:

1. **Log into an EC2 instance**:
    - Access the instance via SSH using an EC2 key pair.

2. **Switch to root**:
    ```bash
    sudo su
    ```

3. **Update the EC2 instance**:
    ```bash
    yum upgrade -y
    yum update -y
    ```

4. **Install Git**:
    ```bash
    yum install git -y
    ```

5. **Clone the Repository**:
    ```bash
    git clone <REPO_LINK>
    cd <PROJECT_REPO>
    ```

6. **Install Python and Pip**:
    ```bash
    yum install python3-pip -y
    ```

### Initial Testing Without Docker:
7. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

8. **Run the Streamlit App**:
    ```bash
    streamlit run <PATH_TO_STREAMLIT_PY_FILE>
    ```
    - Now access the app in the browser using the EC2 public IP: [http://54.224.25.176:8501](http://54.224.25.176:8501)

9. **Stop the Streamlit App**:
    - Press `Ctrl + C` to stop the app running in the terminal.

### Testing with Docker:
10. **Install Docker**:
    ```bash
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    ```

11. **Verify Docker Installation**:
    ```bash
    docker --version
    ```

12. **Start Docker**:
    ```bash
    systemctl start docker
    ```

13. **Check Docker Status**:
    ```bash
    systemctl status docker
    ```
    - Press `Ctrl + C` to exit after confirming Docker is running.

14. **Build Docker Image**:
    ```bash
    docker build -t project-image .
    ```
    - Ensure the Dockerfile is present in your project directory.

15. **List Docker Images**:
    ```bash
    docker images -a
    ```

16. **Run the Docker Container**:
    ```bash
    docker run -d -p 8501:8501 --name project-container project-image
    ```

17. **Verify Running Containers**:
    ```bash
    docker ps
    ```
    - The Streamlit app should now be accessible at the EC2 public IP: [http://54.224.25.176:8501](http://54.224.25.176:8501).

### Stopping the Application and EC2 Instance:
18. **Stop Docker Container**:
    ```bash
    docker stop <CONTAINER_ID>
    ```
    - The container ID can be found in the output of `docker ps`.

19. **Stop the EC2 Instance**:
    - From the AWS Management Console, stop the EC2 instance to save costs.

## Docker Setup

If necessary to work directly with Docker, follow these steps to run the app:

1. **Build the Docker image**:
    ```bash
    docker build -t job-description-tool .
    ```

2. **Run the Docker container**:
    ```bash
    docker run -d -p 8501:8501 job-description-tool
    ```

3. **Access the app**:
    - Use the EC2 public IP: [http://54.224.25.176:8501](http://54.224.25.176:8501) to open the app in a web browser.

## Usage
1. Open the app in the browser using the public IP and port.
2. Navigate through the job description sections using the **Next/Back navigation buttons**.
3. Input relevant details for each section (Job Summary, Key Responsibilities, Required Qualifications, Skills & Experience).
4. Generate a job description based on user input and download it as a PDF.

## License
This project is licensed under the MIT License.
