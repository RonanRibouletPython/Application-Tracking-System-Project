from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
from pdf2image import convert_from_path, convert_from_bytes
import google.generativeai as genai
import io
import base64

gemini_15_api_key = os.getenv("GOOGLE_AI_API_KEY")

genai.configure(api_key=gemini_15_api_key)

vision_model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input, pdf_content, prompt):
        
    response = vision_model.generate_content([input, pdf_content[0], prompt])

    return response.text
  
def input_pdf_setup(_uploaded_pdf):
    pop_path = r'C:\\Program Files\\poppler-24.02.0\\Library\bin'
    #pdf_path="CV_Riboulet_Ronan_Software_Engineer.pdf"
    #images = pdf_to_images(pdf_path)
    if _uploaded_pdf is not None:
        # Conversion of the pdf into an image that can read by the gemini pro vision model
        images = pdf2image.convert_from_bytes(_uploaded_pdf.read(), poppler_path = pop_path)
            
        first_page = images[0]

        # Convert to bytes
        img_byte_array = io.BytesIO()
        first_page.save(img_byte_array, format='JPEG')
        img_byte_array = img_byte_array.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_array).decode()  # encode to base64
            }
        ]

        return pdf_parts  
    
    #else:
        #raise FileNotFoundError("No PDF file uploaded")
       
# Web app 
st.set_page_config(page_title="ATS Resume Expert powered by Gemini Pro 1.5")

st.header("Application Tracking System")

input_text = st.text_area("Job Description", key=input)

uploaded_pdf = st.file_uploader("Upload your resume as PDF file", type=["pdf"])

if uploaded_pdf is not None:
    st.write("Resume uploaded successfully !!!")

submit1 = st.button("What is interesting about your resume")
input_prompt1 = """
                You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
                Please share your professional evaluation on whether the candidate's profile aligns with the role. 
                Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
                """

submit2 = st.button("How well does your resume match the offer")
input_prompt2 = """
                You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of ATS functionality. 
                Your task is to evaluate the resume against the provided job description.
                Give me the percentage of match between the resume provided and the job description.
                As an output, you should first display the percentage of the match and explain why you chose this pourcentage with a few bullet points.
                Then you give keywords that are missing and give last final thoughts with some motivational speech.
                """

if submit1:
    if uploaded_pdf is not None:
        pdf_content = input_pdf_setup(uploaded_pdf)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if uploaded_pdf is not None:
        pdf_content = input_pdf_setup(uploaded_pdf)
        response = get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please upload the resume")
        


