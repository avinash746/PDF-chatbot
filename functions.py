import os
import uuid
import json
import PyPDF2
import streamlit as st
import openai

# Initialize OpenAI API
openai.api_key = "YOUR_API_KEY"

# Function to learn from PDF
def learn_pdf(file_path):
    content_chunks = []
    try:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                content = page.extract_text()
                obj = {
                    "id": str(uuid.uuid4()),
                    "text": content,
                    "embedding": openai.Embedding.create(data=content, model="text-embedding-ada-002").object
                }
                content_chunks.append(obj)

        json_file_path = 'my_knowledgebase.json'
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []

        data.extend(content_chunks)
        
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Error learning from PDF: {e}")

# Function to get answer from documents
def answer_from_documents(user_query):
    try:
        with open('my_knowledgebase.json', 'r', encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)
            
            user_query_embedding = openai.Embedding.create(data=user_query, model="text-embedding-ada-002").object
            
            for item in data:
                item['similarities'] = openai.CosineSimilarity.compare(item['embedding'], user_query_embedding).object
            
            sorted_data = sorted(data, key=lambda x: x['similarities'], reverse=True)
            
            context = ''
            for item in sorted_data[:2]:
                context += item['text']

            myMessages = [
                {"role": "system", "content": "You're a helpful Assistant."},
                {"role": "user", "content": "The following is a Context:\n{}\n\n Answer the following user query according to the above given context.\n\nquery: {}".format(context, user_query)}
            ]
            
            response = openai.ChatCompletion.create(
                model='text-davinci-003',
                messages=myMessages,
                max_tokens=200
            )

        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"Error getting answer from documents: {e}")

# Function to save uploaded file
def save_uploaded_file(uploaded_file):
    try:
        with open('uploaded_file.pdf', "wb") as f:
            f.write(uploaded_file.getbuffer())
    except Exception as e:
        st.error(f"Error saving uploaded file: {e}")
