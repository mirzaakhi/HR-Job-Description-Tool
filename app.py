import streamlit as st 
import requests
import openai
import os
import urllib.parse
import json
from io import StringIO, BytesIO
from fpdf import FPDF

# Load OpenAI API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")



# Initialize session state variables
session_variables = ['job_summary_complete', 'job_title', 'department', 'location', 
                     'salary_range', 'additional_comments', 'role_description', 
                     'role_start_date', 'manager_count', 'responsibilities', 
                     'refined_description', 'page']

for var in session_variables:
    if var not in st.session_state:
        if var == 'responsibilities':
            st.session_state[var] = []
        elif var == 'manager_count':
            st.session_state[var] = 1
        else:
            st.session_state[var] = None

if 'page' not in st.session_state:
    st.session_state['page'] = 0

# Define the pages globally
pages = {
    "Job Summary": lambda: job_summary(),
    "Key Responsibilities": lambda: key_responsibilities(),
    "Required Qualifications": lambda: required_qualifications(),
    "Skills & Experience": lambda: skills_experience(),
    "How to Apply": lambda: how_to_apply(),
    "Refine": lambda: refine_job_description()
}


# Function to generate chatbot responses
def generate_response(prompt):
    try:
        with st.spinner('Generating response...'):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Few-shot examples for better prompt engineering for job descriptions
few_shot_prompt = """
Here are some examples of job descriptions for different roles:

Example 1:
**Job Title:** Data Scientist

**Job Summary:**
We are looking for a Data Scientist to join our team. The ideal candidate will have strong analytical skills and experience in data mining, analysis, and predictive modeling. As a Data Scientist, you will work closely with cross-functional teams to understand business requirements and develop data-driven solutions that drive strategic decision-making.

**Responsibilities:**
- Develop, test, and implement data models and algorithms to solve complex business problems.
- Collaborate with data engineers to acquire and prepare datasets for analysis.
- Analyze large datasets to identify trends and insights that can drive business strategies.
- Create visualizations and dashboards to communicate findings to stakeholders.
- Stay current with the latest developments in data science and machine learning technologies.

**Required Skills:**
- Proficiency in Python, R, SQL, and machine learning libraries such as scikit-learn and TensorFlow.
- Strong experience with data visualization tools like Tableau, Power BI, or similar.
- Excellent problem-solving skills and ability to work with complex datasets.
- Strong communication skills to present findings to non-technical audiences.

**Qualifications:**
- Bachelor's or Master's degree in Computer Science, Statistics, Mathematics, or a related field.
- 3+ years of experience in data science, analytics, or a similar role.

Example 2:
**Job Title:** Software Engineer

**Job Summary:**
Our growing tech company is seeking a skilled Software Engineer to join our development team. The successful candidate will have experience in software development, excellent problem-solving abilities, and a strong knowledge of coding languages. As a Software Engineer, you will design, build, and maintain scalable applications that power our customer-facing platforms.

**Responsibilities:**
- Design, build, and maintain efficient, reusable, and reliable code.
- Collaborate with product managers and cross-functional teams to develop software solutions.
- Conduct code reviews and provide constructive feedback to team members.
- Optimize applications for maximum speed and scalability.
- Participate in the entire application lifecycle, from concept to deployment and support.

**Required Skills:**
- Proficiency in Java, C++, Python, or JavaScript.
- Experience with web frameworks such as React, Angular, or Django.
- Familiarity with RESTful APIs and microservices architecture.
- Knowledge of cloud platforms like AWS, Azure, or GCP.

**Qualifications:**
- Bachelor’s degree in Computer Science, Software Engineering, or a related field.
- 2+ years of experience in software development.

Using these examples as a reference, create a comprehensive job description for a [JOB_TITLE] role at a [COMPANY_TYPE]. Ensure the job description includes a Job Summary, Responsibilities, Required Skills, and Qualifications.
"""

# Function to generate a job description based on few-shot prompt engineering
# Function to generate a job description based on user input
def generate_job_description(job_title, company_type):
    # Use provided arguments or fall back to session state values
    job_title = job_title or st.session_state.get('job_title', 'Software Engineer')
    company_type = company_type or 'Example Company Type'
    department = st.session_state.get('department', 'Engineering')
    location = st.session_state.get('location', 'Remote or On-site in New York, NY')
    salary_range = st.session_state.get('salary_range', '70,000 - 100,000 USD per year')
    role_description = st.session_state.get('role_description', 'We are looking for a dedicated Software Engineer to join our dynamic team.')
    role_start_date = st.session_state.get('role_start_date', 'As soon as possible')
    responsibilities = "\n- ".join(st.session_state.get('responsibilities', ['Develop, test, and maintain software applications.', 'Collaborate with cross-functional teams to deliver high-quality software solutions.']))
    required_qualifications = st.session_state.get('required_qualifications', 'Bachelor’s degree in Computer Science or related field. 3+ years of experience in software development.')
    skills_experience = st.session_state.get('skills_experience', 'Proficiency in Java, Python, or JavaScript. Experience with web frameworks such as React or Django.')
    application_email = st.session_state.get('application_email', 'apply@company.com')
    application_deadline = st.session_state.get('application_deadline', '31st December 2024')
    additional_instructions = st.session_state.get('additional_info', 'Please include a cover letter and resume with your application.')

   # Create a comprehensive prompt for the job description generation
    # Create a comprehensive prompt for the job description generation
    prompt = f"""
    Generate a comprehensive job description for the following role:

    **Job Title:** {job_title}
    **Department:** {department}
    **Location:** {location}
    **Salary Range:** {salary_range}
    **Role Description:** {role_description}
    **Role Start Date:** {role_start_date}

    **Key Responsibilities:**
    - {responsibilities}

    **Required Qualifications:**
    {required_qualifications}

    **Skills & Experience:**
    {skills_experience}

    **How to Apply:**
    - Email: {application_email}
    - Application Deadline: {application_deadline}
    - Additional Instructions: {additional_instructions}

    Ensure that the description is well-organized, clear, and aligns with industry standards for a job posting. Use the examples provided earlier as a style guide.
    """

    # Generate response using OpenAI API
    return generate_response(prompt)


# Function to generate a PDF from text
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf_output = pdf.output(dest='S').encode('latin1')
    return pdf_output

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

# Function to handle Job Summary input
def job_summary():
    st.subheader("Job Summary")
    
    # Display sample questions first
    st.markdown("""
    ### Sample Questions to Consider:
    - What are the primary responsibilities and functions of this role?
    - What are the key objectives for someone in this role over the first 6 months?
    - How does this role contribute to the organization's overall goals?
    - Are there specific skills or experiences critical for success in this role?
    """)
    
    # Provide instructions below sample questions
    st.write("Provide a brief overview of the role, its primary functions, and its impact within the organization.")
    
    # Adding fields for Job Title, Department, Location, Salary Range without submit button
    st.session_state['job_title'] = st.text_input("Job Title", value=st.session_state['job_title'])
    st.session_state['department'] = st.text_input("Department", value=st.session_state['department'])
    st.session_state['location'] = st.text_input("Location", value=st.session_state['location'])
    st.session_state['salary_range'] = st.text_input("Salary Range", value=st.session_state['salary_range'])

   # Adding fields for Job Title, Department, Location, Salary Range without submit button
    st.session_state['additional_comments'] = st.text_input(  # Add this line here
        "Please provide additional comments or summary details:", 
        value=st.session_state['additional_comments']
    )
    st.session_state['role_description'] = st.text_area(
        "Describe the role more elaborately:", 
        value=st.session_state['role_description']
    )
    st.session_state['role_start_date'] = st.date_input(
        "When is the role starting?", 
        value=st.session_state['role_start_date']
    )
    st.session_state['manager_count'] = st.number_input(
        "How many professionals are required for this role?", 
        min_value=1, 
        value=st.session_state['manager_count']
    )

    # Navigation buttons: use a single st.empty() and st.columns() for proper alignment
    nav_buttons_placeholder = st.empty()

    with nav_buttons_placeholder:
        col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
        with col1:
            if st.button("Back", key="job_summary_back"):
                # Ensure 'Back' does not go below zero
                st.session_state['page'] = max(st.session_state['page'] - 1, 0)
        with col3:
            # Navigate to next when "Next" button is clicked
            if st.button("Next", key="job_summary_next"):
                # Ensure 'Next' does not exceed the number of pages
                st.session_state['page'] = min(st.session_state['page'] + 1, len(pages) - 1)
                st.stop()  # Stop the script here

# Initialize session state for responsibilities
if 'responsibilities' not in st.session_state:
    st.session_state['responsibilities'] = []

# Function to handle Key Responsibilities input
def key_responsibilities():
    st.subheader("Key Responsibilities")
    st.write("Define the key responsibilities for the role. You can add, edit, or remove items as needed.")
    
    with st.expander("Add Responsibilities"):
        new_responsibility = st.text_area("List a new responsibility:")
        if st.button("Add Responsibility"):
            if new_responsibility.strip():
                st.session_state['responsibilities'].append(new_responsibility.strip())
                st.success("Responsibility added.")
                st.session_state['update'] = not st.session_state.get('update', False)
            else:
                st.warning("Please enter a valid responsibility.")
    
    if st.session_state['responsibilities']:
        st.subheader("Edit or Remove Responsibilities")
        for i, responsibility in enumerate(st.session_state['responsibilities']):
            st.write(f"**Responsibility {i + 1}:** {responsibility}")

            edit_col, remove_col = st.columns([1, 1])
            edit_button = edit_col.button("Edit", key=f"edit_{i}")
            remove_button = remove_col.button("Remove", key=f"remove_{i}")
            
            if edit_button:
                st.session_state['edit_index'] = i
                st.session_state['edit_text'] = responsibility
                
            if 'edit_index' in st.session_state and st.session_state['edit_index'] == i:
                new_text = st.text_area("Edit Responsibility:", value=st.session_state['edit_text'], key=f"edit_area_{i}")
                save_button = st.button("Save", key=f"save_{i}")
                cancel_button = st.button("Cancel", key=f"cancel_{i}")
                
                if save_button:
                    st.session_state['responsibilities'][i] = new_text
                    st.success(f"Responsibility {i + 1} updated.")
                    del st.session_state['edit_index']
                    st.session_state['update'] = not st.session_state.get('update', False)
                    st.write(f"**Responsibility {i + 1}:** {new_text}")
                
                if cancel_button:
                    del st.session_state['edit_index']
                    st.session_state['update'] = not st.session_state.get('update', False)
            
            if remove_button:
                st.session_state['responsibilities'].pop(i)
                st.success(f"Responsibility {i + 1} removed.")
                st.session_state['update'] = not st.session_state.get('update', False)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
    with col1:
        if st.button("Back", key="responsibilities_back"):
            st.session_state['page'] -= 1
    with col3:
        if st.button("Next", key="responsibilities_next"):
            st.session_state['page'] += 1
    
    add_footer()

# Function to handle Required Qualifications input
def required_qualifications():
    st.subheader("Required Qualifications")
    st.write("Specify the education, experience, and certifications required for the role.")
    
    with st.expander("Add Qualifications"):
        st.session_state['required_qualifications'] = st.text_area(
            "Education Requirement:", value=st.session_state.get('required_qualifications', '')
        )
        st.session_state['experience'] = st.text_area(
            "Experience Requirements:", value=st.session_state.get('experience', '')
        )
        st.session_state['certifications'] = st.text_area(
            "Certifications (if any):", value=st.session_state.get('certifications', '')
        )
    
    # Navigation buttons
    col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
    with col1:
        if st.button("Back", key="qualifications_back"):
            st.session_state['page'] -= 1
    with col3:
        if st.button("Next", key="qualifications_next"):
            st.session_state['page'] += 1
    
    add_footer()

# Function to handle Skills & Experience input
def skills_experience():
    st.subheader("Skills & Experience")
    st.write("List the essential skills and experience needed for success in the role.")
    
    st.session_state['skills'] = st.multiselect(
        "Select Required Skills:", ["Communication", "Teamwork", "Leadership", "Programming", "Data Analysis"],
        default=st.session_state.get('skills', [])
    )
    st.session_state['additional_skills'] = st.text_area(
        "Add any additional skills:", value=st.session_state.get('additional_skills', '')
    )

    # Navigation buttons
    col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
    with col1:
        if st.button("Back", key="skills_back"):
            st.session_state['page'] -= 1
    with col3:
        if st.button("Next", key="skills_next"):
            st.session_state['page'] += 1
    
    add_footer()

# Function to handle How to Apply instructions
def how_to_apply():
    st.subheader("How to Apply")
    st.write("Provide instructions on how candidates can apply for the role.")
    
    with st.expander("Application Instructions"):
        st.session_state['application_email'] = st.text_input("Application Email Address:", value=st.session_state.get('application_email', ''))
        st.session_state['application_deadline'] = st.date_input("Application Deadline:", value=st.session_state.get('application_deadline'))
        st.session_state['additional_info'] = st.text_area("Additional Instructions:", value=st.session_state.get('additional_info', ''))

    # Generate Job Description button
    if st.button("Generate Job Description", key="generate_description"):
        job_title = st.session_state.get('job_title', "Example Job Title")  
        company_type = st.session_state.get('company_type', "Example Company Type")
        job_description = generate_job_description(job_title, company_type)  # Generate the job description
        st.session_state['generated_job_description'] = job_description  # Store in session state
        st.success("Job description generated and saved.")

    # Navigation buttons
    col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
    with col1:
        if st.button("Back", key="apply_back"):
            st.session_state['page'] -= 1
    with col3:
        if st.button("Next", key="apply_next"):
            st.session_state['page'] += 1
    
    add_footer()


# Function to handle job description refinement
def refine_job_description():
    st.subheader("Refine Job Description")

    # Display the generated job description if it exists
    if 'generated_job_description' in st.session_state:
        st.write("### Generated Job Description:")

        # Properly formatted display
        job_description = st.session_state['generated_job_description']

        # Split the job description for better formatting
        st.markdown(f"**Job Title:** {st.session_state.get('job_title', '')}")
        st.markdown(f"**Department:** {st.session_state.get('department', '')}")
        st.markdown(f"**Location:** {st.session_state.get('location', '')}")
        st.markdown(f"**Salary Range:** {st.session_state.get('salary_range', '')}")
        st.markdown(f"**Role Description:** {st.session_state.get('role_description', '')}")
        st.markdown(f"**Role Start Date:** {st.session_state.get('role_start_date', '')}")

        st.write("**Key Responsibilities:**")
        responsibilities = st.session_state.get('responsibilities', [])
        for responsibility in responsibilities:
            st.markdown(f"- {responsibility}")

        st.markdown(f"**Required Qualifications:** {st.session_state.get('required_qualifications', '')}")
        st.markdown(f"**Skills & Experience:** {st.session_state.get('skills_experience', '')}")
        st.markdown(f"**How to Apply:**")
        st.markdown(f"- **Email:** {st.session_state.get('application_email', '')}")
        st.markdown(f"- **Application Deadline:** {st.session_state.get('application_deadline', '')}")
        st.markdown(f"- **Additional Instructions:** {st.session_state.get('additional_info', '')}")
    else:
        st.write("No job description generated yet. Please go back to the 'How to Apply' page and click 'Generate Job Description'.")

    # Refinement input area
    st.write("### Refine the Job Description Below")
    refinement_instructions = st.text_area("Enter refinement instructions here:")

    if st.button("Submit Refinement"):
        if refinement_instructions.strip():
            # Include context in the refinement prompt
            context = st.session_state['generated_job_description']
            
            # Updated prompt to ensure all fields are included
            prompt = (f"Refine the following job description to be more concise and specific, ensuring that the skills, "
          f"qualifications, and responsibilities are relevant to a machine learning engineer role. "
          f"Remove any irrelevant programming languages or technologies that are not typically required for this role, "
          f"such as web development frameworks. Keep the focus on machine learning algorithms, data science tools, "
          f"and relevant programming languages like Python and R. \n\n{context}\n\n"
          f"Refinement Instructions: {refinement_instructions}")

            
            refined_text = generate_response(prompt)
            st.session_state['refined_description'] = refined_text
            st.write("### Refined Job Description:")

            # Properly format refined job description
            refined_description_lines = refined_text.split("\n")  # Split lines for better formatting
            for line in refined_description_lines:
                st.write(line)

    if st.session_state.get('refined_description'):
        pdf_file = create_pdf(st.session_state['refined_description'])
        st.download_button(
            label="Download Refined Job Description",
            data=pdf_file,
            file_name='refined_job_description.pdf',
            mime='application/pdf'
        )
    
    # Navigation buttons
    col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
    with col1:
        if st.button("Back", key="refine_back"):
            st.session_state['page'] -= 1
    
    add_footer()

# Function to store inputs from previous pages in session state
def store_inputs_in_session_state():
    if 'job_summary' not in st.session_state:
        st.session_state['job_summary'] = ""
    if 'key_responsibilities' not in st.session_state:
        st.session_state['key_responsibilities'] = []
    if 'required_qualifications' not in st.session_state:
        st.session_state['required_qualifications'] = ""
    if 'skills_experience' not in st.session_state:
        st.session_state['skills_experience'] = ""

# Main function to handle page navigation
def main():
    st.title("Job Description Tool with Chatbot")

    # Define pages and their respective functions
    pages = {
        "Job Summary": job_summary,
        "Key Responsibilities": key_responsibilities,
        "Required Qualifications": required_qualifications,
        "Skills & Experience": skills_experience,
        "How to Apply": how_to_apply,
        "Refine": refine_job_description  # Directly go to the refine page
    }

    # Initialize session state for page index if not already done
    if 'page' not in st.session_state or st.session_state['page'] is None:
        st.session_state['page'] = 0  # Set to 0 if not initialized or if it's None

    # Ensure the page index is within valid bounds and is an integer
    total_pages = len(pages)
    try:
        st.session_state['page'] = int(st.session_state['page'])  # Ensure it's an integer
    except ValueError:
        st.session_state['page'] = 0  # Reset to 0 if conversion fails

    # Check bounds to prevent out-of-range errors
    if st.session_state['page'] < 0:
        st.session_state['page'] = 0
    elif st.session_state['page'] >= total_pages:
        st.session_state['page'] = total_pages - 1

    # Display the current page
    page = list(pages.values())[st.session_state['page']]
    page()

    add_footer()

if __name__ == "__main__":
    main()
