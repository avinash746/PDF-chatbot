import os
import streamlit as st
from functions import *
# Set OpenAI API key
openai.api_key = "OPENAI_API_KEY"





def main():
    st.title(" Pdf+ChatGPT ")

    uploaded_file = st.file_uploader("Choose a PDF file to upload", type="pdf")
    if uploaded_file is not None:
        if st.button("Read PDF"):
            save_uploaded_file(uploaded_file)
            st.write("Please wait while we learn the PDF.")
            learn_pdf('uploaded_file.pdf')
            st.write("PDF reading completed! Now you may ask a question")
            os.remove('uploaded_file.pdf')  # Remove the temporary uploaded file
    
    user_input = st.text_input("Enter your Query:")
    if st.button("Send"):
        st.write("You:", user_input)
        response = answer_from_documents(user_input)
        if response is not None:
            st.write("Bot: " + response)
       

if __name__ == "__main__":
    main()
