import streamlit as st
import requests

# Function to call the API
def call_api(job_details):
    url = "https://d0bob824og.execute-api.eu-north-1.amazonaws.com/dev"  # Your API's invoke URL
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=job_details, headers=headers)
    return response.json()

# Set page configuration for better visualization
st.set_page_config(page_title="HR Job Description Tool", layout="wide")

# Sidebar for feature selection
st.sidebar.title("Feature Selection Menu")
feature = st.sidebar.radio("Select Required Feature", ["Job Summary", "Key Responsibilities", "Required Qualifications", "Skills & Experience", "How to Apply", "Generate Custom Job Description"])

# Main content area
st.title("HR Job Description Tool")

if feature == "Job Summary":
    st.subheader("Job Summary")
    st.write("""
    The HR Manager will lead and direct the routine functions of the Human Resources (HR) department including hiring and interviewing staff, 
    administering pay, benefits, and leave, and enforcing company policies and practices.
    """)

    # Create a form for user input
    with st.form(key='job_summary_form'):
        additional_comments = st.text_input("Please provide additional comments or summary details:")
        hr_role_description = st.text_area("Describe the HR role more elaborately:")
        role_start_date = st.date_input("When is the HR Manager role starting?")
        hr_manager_count = st.number_input("How many HR Managers are required?", min_value=1)

        # Submit button to handle input
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        # Process the user inputs here
        st.success("Details submitted successfully!")
        st.write("Additional Comments:", additional_comments)
        st.write("HR Role Description:", hr_role_description)
        st.write("Role Start Date:", role_start_date)
        st.write("HR Manager Count:", hr_manager_count)

elif feature == "Key Responsibilities":
    st.subheader("Key Responsibilities")
    st.write("""
    - Recruits, interviews, hires, and trains new staff in the department.
    - Oversees the daily workflow of the department.
    - Provides constructive and timely performance evaluations.
    - Handles discipline and termination of employees in accordance with company policy.
    """)

elif feature == "Required Qualifications":
    st.subheader("Required Qualifications")
    st.write("""
    - Bachelor’s degree in Human Resources, Business Administration, or related field required.
    - A minimum of three years of human resource management experience preferred.
    - SHRM-CP or SHRM-SCP highly desired.
    """)

elif feature == "Skills & Experience":
    st.subheader("Skills & Experience")
    st.write("""
    - Excellent verbal and written communication skills.
    - Excellent interpersonal, negotiation, and conflict resolution skills.
    - Excellent organizational skills and attention to detail.
    - Strong analytical and problem-solving skills.
    - Ability to prioritize tasks and to delegate them when appropriate.
    """)

elif feature == "How to Apply":
    st.subheader("How to Apply")
    st.write("""
    Please send your resume and cover letter to [hr@company.com](mailto:hr@company.com).
    """)

elif feature == "Generate Custom Job Description":
    st.subheader("Generate Custom Job Description")
    
    # Input form for custom job description
    with st.form(key='job_description_form'):
        job_title = st.text_input("Job Title")
        department = st.text_input("Department")
        location = st.text_input("Location")
        salary_range = st.text_input("Salary Range")
        
        # Submit button
        submit_button = st.form_submit_button(label='Generate Job Description')
    
    # Display the generated job description after form submission
    if submit_button:
        job_details = {
            "job_title": job_title,
            "department": department,
            "location": location,
            "salary_range": salary_range
        }

        # Call the API
        result = call_api(job_details)

        # Display the API result
        st.subheader("Generated Job Description:")
        st.json(result)
