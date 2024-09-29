import streamlit as st
from docx import Document
import fitz  # PyMuPDF
import requests

if 'message_list' not in st.session_state:
    st.session_state.message_list = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

class Conversation:
    def __init__(self):
        self.base_url = 'http://localhost:11434/v1'  # Change to your Ollama base URL if different
        self.api_key = 'ollama'  # API key placeholder

    def message(self, question):
        q = {
            "role": "user",
            "content": question
        }

        st.session_state.message_list.append(q)

        response = self.query_ollama_model(st.session_state.message_list)

        if response and response.get('choices'):
            answer = response['choices'][0]['message']['content']
            q = {
                "role": "assistant",
                "content": answer
            }

            st.session_state.message_list.append(q)
            return answer

        return "No response from the model."

    def query_ollama_model(self, messages):
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama3",
            "messages": messages
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error querying the model: {e}")
            return None

def extract_text_from_pdf(file):
    document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    text = [paragraph.text for paragraph in doc.paragraphs]
    return "\n".join(text)

def extract_text_from_txt(file):
    return file.read().decode('utf-8')

def upload_and_extract_text():
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            return extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return extract_text_from_docx(uploaded_file)
        elif uploaded_file.type == "text/plain":
            return extract_text_from_txt(uploaded_file)
    return None

def ask_question(document_text, question):
    # Replace with actual Ollama client API call
    url = "https://api.ollama.com/query"
    headers = {
        "Authorization": "ollama",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3",
        "document": document_text,
        "question": question
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get('answer', 'No answer found.')
    except requests.exceptions.RequestException as e:
        return f"Error querying the model: {e}"

if __name__ == "__main__":
    st.title('Document-based Chatbot')

    document_text = upload_and_extract_text()

    if document_text:
        st.text_area("Extracted Document Text", document_text, height=300)
        
        conversation = Conversation()
        
        prompt = st.chat_input("Ask a question about the document")
        if prompt:
            with st.spinner('Thinking...'):
                answer = ask_question(document_text, prompt)
                response_message = conversation.message(prompt + " " + document_text)
                
                for msg in st.session_state.message_list:
                    if msg['role'] == 'user':
                        with st.chat_message("user"):
                            st.write(msg['content'])
                    elif msg['role'] == 'assistant':
                        with st.chat_message("assistant"):
                            st.write(msg['content'])
