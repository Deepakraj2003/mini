
from dotenv import load_dotenv
import base64
import streamlit as st
import os
import PyPDF2 as pdf
import google.generativeai as genai
from firebase import firebase
from datetime import datetime, timedelta


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

db = firebase.FirebaseApplication('https://aidshackathon-default-rtdb.asia-southeast1.firebasedatabase.app/')

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

st.title("ATS Tracking System")
#input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")


input_prompt_detials="""Note: The domain must be either Fullstack or Data analyst or Data science or Machine Learning or Deep Learning or cloud or testing or cyber security or Android developer or web developer.Pick any one from this as per the person's resume depends on for the domain.
Now you are a investigation person and your role is to gather the basic information of the preson like name,role,email id,contact number and response it in a  structure seperated by the symbol || .for example name||role||email id||contact number. 
Note: The domain must be either Fullstack or Data analyst or Data science or Machine Learning or Deep Learning or cloud or testing or cyber security.Pick anyone from this as per the person's resume depends on"""
input_prompt2="""
read and make the response properly for below statement
you are a investigation person and your role is to gather the information of the preson or candidate like Education Bachelor University,Education Bachelor CGPA,Education Bachelor Major,Top Skills,Suitable Position,Candidate Rating (Out of 10).All these information should be truely based on what on the resume
and resopnd in the formate of only the value seperated by a symbol ||.for example- Education Bachelor University||Education Bachelor CGPA||Education Bachelor Major||Skills||Suitable Position/Domain||Candidate Rating (Out of 10)
note: resopnd in the formate of only the value seperated by a symbol ||.the skills should not be seperated by ||.it should be a single string seperated by the symbole , .
Response formate:Education Bachelor University||Education Bachelor CGPA||Education Bachelor Major||Skills||Suitable Position/Domain||Candidate Rating (Out of 10)
"""
input_prompt3="""You are a Head of Human Resource(HR) of a Leading Software Company and You are provided with a candidates's resume.Your work is to evaluate the resume and form a report about only their strength in a one single paragraph.
Make sure that your analysis is more accurate and only based on the data present on the resume and need of current company society 
"""
input_prompt4="""You are a Head of Human Resource(HR) of a Leading Software Company and You are provided with a candidates's resume.Your work is to evaluate the resume and form a report about only their weakness in a one single paragraph.
Make sure that your analysis is more accurate and only based on the data present on the resume and need of current company society .Note that the response must be a single paragraph.
"""
input_prompt5="""You are a Head of Human Resource(HR) of a Leading Software Company and You are provided with a candidates's resume.Your work is to evaluate the resume and form a report about only the points to improve in resume in one single paragraph.
Make sure that your analysis is more accurate and only based on the data present on the resume and need of current company society .
"""

input_prompt1 = """
You are a human resource specialist who is responsible for reviewing candidates' CVs. You will be given the CV of the candidate and your job is to extract the information mentioned below. Also, you must follow the desired output.
response it in the dictionary formate. for example { key1:value1,key2:value2.....}
1. Education Bachelor University: name of university where bachelor degree was taken
2. Education Bachelor GPA: GPA of bachelor degree (Example: 8.5/10)
3. Education Bachelor Major: major of bachelor degree
4. Education Bachelor Graduation Date: date of graduation from bachelor degree or else calculate it from the starting date (in format: Month_Name, YYYY)
5. Years of Experience: total years of experience in all jobs. calculate it by  given information in experence in the experience  (Example: 3 months )
6. Experience Companies and role: list of all companies and the role that the candidate worked with (Example: [Company1, Company2])
7. Top Skills: list of all technical skills (Example: Skill1, Skill2, Skill3,...)
8. Top Soft Skills: list of Top 4 soft skills (Example: Skill1, Skill2, Skill3,...)
9. Current Employment Status: classify to one of the following (Full-time, Part-Time, Intern, Freelancer, Consultant, Unemployed).calculate is as per the data and the date mentioned in the experience
10.Top Projects Titles: list of top 5 projects titles that the candidate worked on (Example: [Project1, Project2, Project3, Project4, Project5])
11. Top 5 Courses/Certifications Titles: list of top 5 courses/certifications titles that the candidate took (Example: [Course1, Course2, Course3, Course4, Course5])
12. Current Residence: where the candidate currently live
13. Suitable Position: classify to one of the following suitable positions for the candidate (suitable position for the candidate)
14. Candidate Rating (Out of 10): rate the candidate suitability for the classified position in point 15 .(Example: 7.1 or 3.8 etc...).It is necessary to rate the candidate by only using the all above information gained.

response it in the dictionary formate. for example { key1:value1,key2:value2.....}
Desired Output: 
response it in the dictionary formate. for example { key1:value1,key2:value2.....}
Note: if any of the information is not mentioned in the cv, dont show it in the response
"""
# input_prompt3 = """
# You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
# your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
# the job description. First the output should come as percentage and then keywords missing and last final thoughts.
# """

if submit1:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        for i in range(0,10):
            response_detials=get_gemini_response(input_text, text, input_prompt_detials)
        res_detials=list(response_detials.split("||"))
        for i in res_detials:
            i.replace(' ','')

        st.subheader("**Your Basic info**")
        st.text('Name: ' + res_detials[0])
        st.text('Email: ' + res_detials[2])
        st.text('Contact: ' + res_detials[3])
        st.text('Domain: ' + res_detials[1])
        res_id=res_detials[2]
        
        ident=""
        for i in res_detials[2]:
            if i!='@':
                if i==".":
                    continue
                else:
                    ident+=i
            else:
                break
        
       
        for i in range(0,7):
            response1 = get_gemini_response(input_text, text, input_prompt2)
        st.subheader("The Response is")
        res1=response1
        # print(res1)
        res_detials2=list(res1.split("||"))
        st.text('University: ' + res_detials2[0])
        st.text('Branch: ' + res_detials2[2])
        st.text('CGPA: ' + res_detials2[1])
        st.text('Skills: ' + res_detials2[3])
        st.text('Domain: ' + res_detials[1])
        st.text('Rating: ' + res_detials2[5])
        print(res_detials2)
        # st.write(res1)
        
        response3=get_gemini_response(input_text, text, input_prompt3)
        st.subheader("The strength is")
        st.write(response3)
        strength = response3
        response4=get_gemini_response(input_text, text, input_prompt4)
        st.subheader("The weakness is")
        st.write(response4)
        weakness = response4
        response5=get_gemini_response(input_text, text, input_prompt5)
        st.subheader("The area to improve is")
        st.write(response5)
        improve=response5
        st.write("verify wheather all the detials about you is correctly extracted.If any corrections needed rerun the process else click proceed.")
        st.write("Your Portal id is ",ident,".Please remember it")
        # Get the current date
        current_date = datetime.now().date()+ timedelta(days=7)

        # Calculate one week after the current date
        one_week_after = current_date + timedelta(days=7)
        date=str(current_date)
        print("Current Date:", current_date)
        print("One Week After:", one_week_after)
        data={
           "Name":res_detials[0],
            "Email":res_detials[2],
            "Contact":res_detials[3],
            "Domain":res_detials[1],
            "id":ident,
            "University":res_detials2[0],
            "Branch":res_detials2[2],
            "CGPA":res_detials2[1],
            "Skills":res_detials2[3],
            "Domain":res_detials2[4],
            "Rating":res_detials2[5],
            "Date":date,
            "Strength":strength,
            "Weakness":weakness,
            "Areatoimprove":improve
        }
        print(data)
        db.put("/user",data["id"],data)
        
    else:
        st.write("Please upload the resume")


