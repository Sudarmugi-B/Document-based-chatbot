# Document-based Chatbot

This project implements a document-based chatbot using Streamlit and Ollama. Users can upload documents (PDF, DOCX, or TXT) and ask questions about the content. The chatbot uses the Ollama API to generate responses based on the document content and user questions.

## Features

- Document upload support for PDF, DOCX, and TXT files
- Text extraction from uploaded documents
- Chatbot interface for asking questions about the document
- Integration with Ollama API for natural language processing

## Screenshots

### Document Upload
![Document Upload](<images/pic2.png> "Document Upload Interface")

### Chat Interface
![Chat Interface](<images/pic1.png> "Chat Interface with Document Context")

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Sudarmugi-B/Document-based-chatbot
   cd document-based-chatbot
   ```

2. Install the required dependencies:
   ```
   pip install streamlit python-docx PyMuPDF requests
   ```

3. Set up Ollama:
   - Follow the instructions at [Ollama's official website](https://ollama.ai/) to install and set up Ollama on your system.
   - Make sure the Ollama API is running and accessible at `http://localhost:11434/v1`.

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Upload a document (PDF, DOCX, or TXT) using the file uploader.

4. Once the document is uploaded and processed, you can start asking questions about its content in the chat interface.

## Configuration

- The Ollama API base URL is set to `http://localhost:11434/v1` by default. If your Ollama instance is running on a different address, update the `base_url` in the `Conversation` class.
- The current implementation uses the "llama3" model. You can change this by modifying the `model` parameter in the API requests.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
