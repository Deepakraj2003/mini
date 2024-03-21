from dotenv import load_dotenv
import base64

import os
import PyPDF2 as pdf
import google.generativeai as genai

load_dotenv()
# GOOGLE_API_KEY="AIzaSyBLPKwFs52FYOmYu-OSPKDPUvEiMowmbuo"
genai.configure(api_key=os.getenv("OOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfFileReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text
input_text = "Need a fullstack developer"
upload_file= "C:/Users/rajd3/Downloads/S_DEEPAKRAJ_Resume.pdf" 
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
input_prompt3 = "You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matchethe job description. First the output should come as percentage and then keywords missing and last final thoughts."
if upload_file is not None:
    print("PDF Uploaded Successfully")
c=2
if c==1:
    if upload_file is not None:
        text = input_pdf_text(upload_file)
        response = get_gemini_response(input_text, text, input_prompt1)
        print(response)
        
    else:
        print("Please upload the resume")
elif c==2:
    if upload_file is not None:
        text = input_pdf_text(upload_file)
        response = get_gemini_response(input_text, text, input_prompt3)
        response = get_gemini_response(input_text, text, input_prompt1)
        print(response)
    
    else:
        print("Please upload the resume")