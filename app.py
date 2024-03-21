# # import streamlit as st
# # import google.generativeai as genai
# # import os
# # import PyPDF2 as pdf
# # from dotenv import load_dotenv
# # import json

# # load_dotenv() ## load all our environment variables

# # genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # def get_gemini_repsonse(input):
# #     model=genai.GenerativeModel('gemini-pro')
# #     response=model.generate_content(input)
# #     return response.text

# # def input_pdf_text(uploaded_file):
# #     reader=pdf.PdfReader(uploaded_file)
# #     text=""
# #     for page in range(len(reader.pages)):
# #         page=reader.pages[page]
# #         text+=str(page.extract_text())
# #     return text

# # #Prompt Template

# # input_prompt="""
# # Hey Act Like a skilled or very experience ATS(Application Tracking System)
# # with a deep understanding of tech field,software engineering,data science ,data analyst
# # and big data engineer. Your task is to evaluate the resume based on the given job description.
# # You must consider the job market is very competitive and you should provide 
# # best assistance for improving thr resumes. Assign the percentage Matching based 
# # on Jd and
# # the missing keywords with high accuracy
# # resume:{text}
# # description:{jd}

# # I want the response in one single string having the structure
# # {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
# # """

# # ## streamlit app
# # st.title("Smart ATS")
# # st.text("Improve Your Resume ATS")
# # jd=st.text_area("Paste the Job Description")
# # uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

# # submit = st.button("Submit")

# # if submit:
# #     if uploaded_file is not None:
# #         text=input_pdf_text(uploaded_file)
# #         response=get_gemini_repsonse(input_prompt)
# #         st.subheader(response)

# from dotenv import load_dotenv
# import base64
# import streamlit as st
# import os
# import PyPDF2 as pdf
# import google.generativeai as genai

# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(input, pdf_content, prompt):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content([input, pdf_content, prompt])
#     return response.text

# def input_pdf_text(uploaded_file):
#     reader = pdf.PdfReader(uploaded_file)
#     text = ""
#     for page in range(len(reader.pages)):
#         page = reader.pages[page]
#         text += str(page.extract_text())
#     return text

# st.set_page_config(page_title="ATS Resume Expert")
# st.header("ATS Tracking System")
# input_text = st.text_area("Job Description: ", key="input")
# uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

# if uploaded_file is not None:
#     st.write("PDF Uploaded Successfully")

# submit1 = st.button("Tell Me About the Resume")
# submit2 = st.button("How Can I Improve my Skills")
# submit3 = st.button("Percentage match")

# input_prompt1 = """
#  You are an experienced Technical Human Resource Manager With Tech experence in Data Science,Fullstack,Big Data engineering,devops,Data Analyst,your task is to review the provided resume against the job description for these profiles. 
#   Please share your professional evaluation on whether the candidate's profile aligns with the role. 
#  Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
# """
# input_prompt3 = """
# You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
# your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
# the job description. First the output should come as percentage and then keywords missing and last final thoughts.
# """

# if submit1:
#     if uploaded_file is not None:
#         text = input_pdf_text(uploaded_file)
#         response = get_gemini_response(input_text, text, input_prompt1)
#         st.subheader("The Response is")
#         st.write(response)
#     else:
#         st.write("Please upload the resume")

# elif submit3:
#     if uploaded_file is not None:
#         text = input_pdf_text(uploaded_file)
#         response = get_gemini_response(input_text, text, input_prompt3)
#         st.subheader("The Response is")
#         st.write(response)
#     else:
#         st.write("Please upload the resume")


from dotenv import load_dotenv
import base64
import streamlit as st
import os
import PyPDF2 as pdf
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

st.set_page_config(page_title="ATS Resume Expert")

# Define colors
primary_color = '#1f77b4'
secondary_color = '#ff7f0e'
bg_color = '#f0f0f0'

# Custom CSS styles
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: {bg_color};
    }}
    .sidebar .sidebar-content {{
        background: {primary_color};
        color: white;
    }}
    .Widget.stButton>button {{
        background-color: {secondary_color};
        color: white;
    }}
    .stTextInput>div>div>input {{
        color: {primary_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are a human resource specialist who is responsible for reviewing candidates' CVs. You will be given the CV of the candidate and your job is to extract the information mentioned below. Also, you must follow the desired output.

Information To Extract in the list formate:
1. Education Bachelor University: name of university where bachelor degree was taken
2. Education Bachelor GPA: GPA of bachelor degree (Example: 4.5/5)
3. Education Bachelor Major: major of bachelor degree
4. Education Bachelor Graduation Date: date of graduation from bachelor degree (in format: Month_Name, YYYY)
5. Education Masters University: name of university where masters degree was taken
6. Education Masters GPA: GPA of masters degree (Example: 4.5/5)
7. Education Masters Major: major of masters degree
8. Education Masters Graduation Date: date of graduation from masters degree (in format: Month_Name, YYYY)
9. Education PhD University: name of university where PhD degree was taken
10. Education PhD GPA: GPA of PhD degree (Example: 4.5/5)
11. Education PhD Major: major of PhD degree
12. Education PhD Graduation Date: date of graduation from PhD degree (in format: Month_Name, YYYY)
13. Years of Experience: total years of experience in all jobs (Example: 3)
14. Experience Companies: list of all companies that the candidate worked with (Example: [Company1, Company2])
15. Top 5 Responsibilities/Projects Titles: list of top 5 responsibilities/projects titles that the candidate worked on (Example: [Project1, Project2, Project3, Project4, Project5])
16. Top 5 Courses/Certifications Titles: list of top 5 courses/certifications titles that the candidate took (Example: [Course1, Course2, Course3, Course4, Course5])
17. Top Skills: list of top 3 technical skills (Example: [Skill1, Skill2, Skill3,...])
18. Top Soft Skills: list of top 3 soft skills (Example: [Skill1, Skill2, Skill3,...])
19. Current Employment Status: classify to one of the following (Full-time, Part-Time, Intern, Freelancer, Consultant, Unemployed)
20. Nationality: nationality of the candidate
21. Current Residence: where the candidate currently live
22. Suitable Position: classify to one of the following suitable positions for the candidate (suitable position for the candidate)
23. Candidate Rating (Out of 10): rate the candidate suitability for the classified position in point 19 (Example: 7.5)


Desired Output: 
show in the table formate of all the information extracted from the resume


Note: if any of the information is not mentioned in the cv, dont show it in the response
"""
input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_text, text, input_prompt1)
        st.subheader("The Response is")
       
        st.write(response)
        
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_text, text, input_prompt3)
        st.subheader("The Response is")
      
        st.write(response)
    
    else:
        st.write("Please upload the resume")
