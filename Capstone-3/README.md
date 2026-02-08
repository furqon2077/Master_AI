# Customer Support RAG System

A Customer Support solution powered by AI that can answer questions from datasources and create support tickets.

## Features

- AI-powered question answering from PDF documents
- Document citations with filename and page numbers
- Support ticket creation via GitHub Issues
- Conversation history management
- Company context awareness
- Web interface built with Streamlit

## Tech Stack

- **LLM**: Google Gemini Pro with function calling
- **Vector Database**: ChromaDB
- **Issue Tracker**: GitHub Issues
- **Web Framework**: Streamlit
- **Python Version**: 3.11.9

## Prerequisites

- Python 3.10 or higher
- Google Gemini API key
- GitHub personal access token
- GitHub repository for storing support tickets

## Installation

1. Clone this repository or download the files

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

4. Configure your environment variables in `.env`:
```
GOOGLE_API_KEY=your_google_api_key
GITHUB_TOKEN=your_github_token
GITHUB_REPO_OWNER=your_username
GITHUB_REPO_NAME=support-tickets
COMPANY_NAME=Your Company Name
COMPANY_EMAIL=support@company.com
COMPANY_PHONE=+1-800-123-4567
```

5. Add your PDF documents to the `data/documents` folder:
   - At least 3 documents required
   - At least 2 PDF files
   - At least 1 PDF with 400+ pages

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will:
1. Load and process all PDF documents
2. Create embeddings and store in ChromaDB
3. Start the web interface at http://localhost:8501

## How It Works

1. **Document Processing**: PDFs are loaded and parsed with page tracking
2. **Text Chunking**: Documents are split into chunks while preserving metadata
3. **Vector Storage**: Chunks are embedded and stored in ChromaDB
4. **AI Agent**: Google Gemini processes queries using function calling to:
   - Search documents for answers
   - Create support tickets when needed
   - Provide company information
5. **Citations**: Responses include source document and page numbers
6. **Ticket Creation**: When answers aren't found, tickets are created in GitHub Issues

## Project Structure

```
.
├── app.py                          # Streamlit web application
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (create from .env.example)
├── src/
│   ├── document_processor.py      # PDF loading and parsing
│   ├── chunking.py                # Text chunking utilities
│   ├── vector_store.py            # ChromaDB vector storage
│   ├── agent.py                   # AI agent with Gemini
│   ├── functions.py               # Function calling definitions
│   ├── ticket_manager.py          # Ticket management
│   └── integrations/
│       └── github_issues.py       # GitHub Issues integration
├── data/
│   ├── documents/                 # PDF documents (add your files here)
│   └── vector_db/                 # ChromaDB storage (auto-generated)
└── tests/                         # Test files
```

## Deployment to HuggingFace Spaces

1. Create a new Space on HuggingFace
2. Select "Streamlit" as the SDK
3. Upload your code files
4. Add secrets in Space settings:
   - `GOOGLE_API_KEY`
   - `GITHUB_TOKEN`
   - `GITHUB_REPO_OWNER`
   - `GITHUB_REPO_NAME`
5. Upload your PDF documents to `data/documents`

## Requirements

### Data Requirements
- At least 3 documents as datasources
- At least 2 PDF files
- At least 1 PDF with 400+ pages

### Technical Requirements
- Python with version specification
- Function calling implementation
- Vector storage for document retrieval
- Document citations with page numbers
- Conversation history support
