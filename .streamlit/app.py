import streamlit as st
import requests
import openai
import os
import urllib.parse  # Import the urllib module for encoding/decoding
import json  # Import the json module to handle JSON parsing

# Define the footer function
def add_footer():
    footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        color: #333;
    }
    </style>
    <div class="footer">
        &copy; 2024 Mirza Akhi, PhD Intern | Tata Consultancy Services
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

# Load OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # Fetch from environment variable


# Define the function to generate chatbot responses using the newer OpenAI API
def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or any other model you prefer, like "gpt-4"
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Function to call the API
def call_api(job_details):
    url = "https://d0bob824og.execute-api.eu-north-1.amazonaws.com/dev"  # Your API's invoke URL
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=job_details, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except ValueError:
        return {"error": "Failed to parse JSON response from API."}

# Function to handle Job Summary input
def job_summary():
    st.subheader("Job Summary")
    st.write("Provide a brief overview of the role, its primary functions, and its impact within the organization.")

    # Add sample guiding questions for users to consider
    st.markdown("""
    ### Sample Questions to Consider:
    - What are the primary responsibilities and functions of this role?
    - What are the key objectives for someone in this role over the first 6 months?
    - How does this role contribute to the organization's overall goals?
    - Are there specific skills or experiences critical for success in this role?
    """)

    # Create a form for user input
    with st.form(key='job_summary_form'):
        additional_comments = st.text_input("Please provide additional comments or summary details:")
        role_description = st.text_area("Describe the role more elaborately:")
        role_start_date = st.date_input("When is the role starting?")
        manager_count = st.number_input("How many professionals are required for this role?", min_value=1)
        
        # Submit button to handle input
        submit_job_summary = st.form_submit_button(label='Submit')
    
    if submit_job_summary:
        st.success("Details submitted successfully!")
        st.write("Additional Comments:", additional_comments)
        st.write("Role Description:", role_description)
        st.write("Role Start Date:", role_start_date)
        st.write("Number of Professionals Required:", manager_count)

    # Add footer at the end of the page
    add_footer()

# Initialize session state for responsibilities if it doesn't exist
if 'responsibilities' not in st.session_state:
    st.session_state['responsibilities'] = []

# Function to handle Key Responsibilities input
def key_responsibilities():
    st.subheader("Key Responsibilities")
    st.write("Define the key responsibilities for the role. You can add, edit, or remove items as needed.")
    
    # Add responsibilities form
    with st.expander("Add Responsibilities"):
        new_responsibility = st.text_area("List a new responsibility:")
        if st.button("Add Responsibility"):
            if new_responsibility.strip():
                st.session_state['responsibilities'].append(new_responsibility.strip())
                st.success("Responsibility added.")
                # Manually trigger a rerun by modifying a session state variable
                st.session_state['update'] = not st.session_state.get('update', False)
            else:
                st.warning("Please enter a valid responsibility.")
    
    # Display existing responsibilities with edit and delete options
    if st.session_state['responsibilities']:
        st.subheader("Edit or Remove Responsibilities")
        
        # Track which responsibility is being edited
        for i, responsibility in enumerate(st.session_state['responsibilities']):
            st.write(f"**Responsibility {i + 1}:** {responsibility}")

            # Edit and Remove Buttons
            edit_col, remove_col = st.columns([1, 1])
            edit_button = edit_col.button("Edit", key=f"edit_{i}")
            remove_button = remove_col.button("Remove", key=f"remove_{i}")
            
            # Editing functionality
            if edit_button:
                # Set the currently editing responsibility in session state
                st.session_state['edit_index'] = i
                st.session_state['edit_text'] = responsibility
                
            # If editing, show the text area and buttons
            if 'edit_index' in st.session_state and st.session_state['edit_index'] == i:
                new_text = st.text_area("Edit Responsibility:", value=st.session_state['edit_text'], key=f"edit_area_{i}")
                save_button = st.button("Save", key=f"save_{i}")
                cancel_button = st.button("Cancel", key=f"cancel_{i}")
                
                if save_button:
                    # Update the responsibility with the new text
                    st.session_state['responsibilities'][i] = new_text
                    st.success(f"Responsibility {i + 1} updated.")
                    # Clear editing state
                    del st.session_state['edit_index']
                    st.session_state['update'] = not st.session_state.get('update', False)  # Trigger rerun
                    # Display the updated responsibility
                    st.write(f"**Responsibility {i + 1}:** {new_text}")
                
                if cancel_button:
                    # Cancel editing
                    del st.session_state['edit_index']
                    st.session_state['update'] = not st.session_state.get('update', False)  # Trigger rerun
            
            # Remove functionality
            if remove_button:
                st.session_state['responsibilities'].pop(i)
                st.success(f"Responsibility {i + 1} removed.")
                st.session_state['update'] = not st.session_state.get('update', False)  # Trigger rerun

    # Add footer at the end of the page
    add_footer()

# Function to handle Required Qualifications input
def required_qualifications():
    st.subheader("Required Qualifications")
    st.write("Specify the education, experience, and certifications required for the role.")
    
    with st.expander("Add Qualifications"):
        education = st.text_input("Education Requirement:")
        experience = st.text_area("Experience Requirements:")
        certifications = st.text_area("Certifications (if any):")
        if st.button("Submit Qualifications"):
            st.write("Education:", education)
            st.write("Experience:", experience)
            st.write("Certifications:", certifications)

    # Add footer at the end of the page
    add_footer()

# Function to handle Skills & Experience input
def skills_experience():
    st.subheader("Skills & Experience")
    st.write("List the essential skills and experience needed for success in the role.")
    
    with st.form(key='skills_experience_form'):
        skills = st.multiselect("Select Required Skills:", ["Communication", "Teamwork", "Leadership", "Programming", "Data Analysis"])
        additional_skills = st.text_area("Add any additional skills:")
        submit_skills = st.form_submit_button(label='Submit Skills')
    
    if submit_skills:
        st.write("Selected Skills:", skills)
        st.write("Additional Skills:", additional_skills)

    # Add footer at the end of the page
    add_footer()

# Function to handle How to Apply instructions
def how_to_apply():
    st.subheader("How to Apply")
    st.write("Provide instructions on how candidates can apply for the role.")
    
    with st.expander("Application Instructions"):
        application_email = st.text_input("Application Email Address:")
        application_deadline = st.date_input("Application Deadline:")
        additional_info = st.text_area("Additional Instructions:")
        if st.button("Submit Application Instructions"):
            st.write("Email to:", application_email)
            st.write("Deadline:", application_deadline)
            st.write("Instructions:", additional_info)

    # Add footer at the end of the page
    add_footer()

# Function to handle custom job description generation
def generate_custom_job_description():
    st.subheader("Generate Custom Job Description")
    
    # Input form for custom job description
    with st.form(key='job_description_form'):
        job_title = st.text_input("Job Title")
        department = st.text_input("Department")
        location = st.text_input("Location")
        salary_range = st.text_input("Salary Range")
        
        # Submit button
        submit_job_description = st.form_submit_button(label='Generate Job Description')

    if submit_job_description:
        if job_title and department and location and salary_range:  # Ensure all inputs are filled
            job_details = {
                "job_title": job_title,
                "department": department,
                "location": location,
                "salary_range": salary_range
            }

            # Call the API
            result = call_api(job_details)

            # Check for errors in API response
            if "error" in result:
                st.error(result["error"])
            else:
                # Ensure the body is parsed correctly
                if "body" in result:
                    try:
                        # Parse the JSON string in the "body" if it's a string
                        body_content = result["body"]
                        if isinstance(body_content, str):
                            body_content = json.loads(body_content)  # Import json at the top of your script
                        
                        # Check if 'message' is in the parsed body
                        if "message" in body_content:
                            st.write(body_content["message"])
                        else:
                            st.warning("No 'message' found in the API response.")
                    except json.JSONDecodeError:
                        st.error("Failed to decode JSON response from API.")
                else:
                    st.json(result)
        else:
            st.warning("Please fill all the fields to generate a job description.")

    # Add footer at the end of the page
    add_footer()

# Function to handle Chat with Chatbot
def chat_with_chatbot():
    st.header("Chat with Chatbot")
    
    # Text input box for user input
    user_input = st.text_input("Enter your question or prompt here:", "")

    # Button to submit the input
    submit_chatbot = st.button("Submit")
    
    if submit_chatbot:
        if user_input:
            # Generate a response from the chatbot
            response = generate_response(user_input)
            # Display the response
            st.write("Chatbot Response:", response)
        else:
            st.warning("Please enter a question or prompt.")

    # Add footer at the end of the page
    add_footer()

# Main function to display the sidebar and sections
def main():
    # **Add the Title for the App**
    st.title("Job Description Tool with Chatbot")  # Add this line to display the title at the top

    # Sidebar for feature selection
    st.sidebar.title("Quick Links")
    feature = st.sidebar.radio(
        "Select Required Feature",
        [
            "Job Summary",
            "Key Responsibilities",
            "Required Qualifications",
            "Skills & Experience",
            "How to Apply",
            "Generate Custom Job Description",
            "Chat with Chatbot"
        ]
    )
    
    # Show the selected feature page
    if feature == "Job Summary":
        job_summary()
    elif feature == "Key Responsibilities":
        key_responsibilities()
    elif feature == "Required Qualifications":
        required_qualifications()
    elif feature == "Skills & Experience":
        skills_experience()
    elif feature == "How to Apply":
        how_to_apply()
    elif feature == "Generate Custom Job Description":
        generate_custom_job_description()
    elif feature == "Chat with Chatbot":
        chat_with_chatbot()

if __name__ == "__main__":
    main()
