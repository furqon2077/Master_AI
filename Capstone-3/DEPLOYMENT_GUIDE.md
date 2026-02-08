# Deployment and Running Guide

## Prerequisites

1. **Google Gemini API Key**
   - Go to https://makersuite.google.com/app/apikey
   - Create a new API key
   - Copy the key for later use

2. **GitHub Personal Access Token**
   - Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
   - Generate new token with `repo` scope
   - Create a repository for support tickets (e.g., "support-tickets")

3. **PDF Documents**
   - Place at least 3 PDF documents in `data/documents` folder
   - At least 2 must be PDFs
   - At least 1 PDF must have 400+ pages

## Local Deployment

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

Edit the `.env` file with your actual credentials:

```
GOOGLE_API_KEY=AIzaSy...your_actual_key
GITHUB_TOKEN=ghp_...your_actual_token
GITHUB_REPO_OWNER=your_username
GITHUB_REPO_NAME=support-tickets
COMPANY_NAME=Your Company Name
COMPANY_EMAIL=support@yourcompany.com
COMPANY_PHONE=+1-800-123-4567
```

### Step 3: Add PDF Documents

Move your PDF files to the documents folder:
- Windows: `data\documents\`
- The system will automatically detect all PDF files in this folder

### Step 4: Initialize the Database

Run the initialization script to process documents and create embeddings:

```bash
python init_database.py
```

This will:
- Load all PDF files
- Extract text with page numbers
- Create embeddings
- Store in ChromaDB

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## HuggingFace Spaces Deployment

### Step 1: Prepare Files

Create a requirements.txt file specifically for HuggingFace if needed (the current one should work).

### Step 2: Create HuggingFace Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose:
   - Space name: `customer-support-rag`
   - SDK: **Streamlit**
   - Hardware: Free CPU (or upgrade if needed)

### Step 3: Upload Files

Upload these files to your HuggingFace Space:
```
app.py
config.py
init_database.py
requirements.txt
.python-version
src/
├── __init__.py
├── agent.py
├── chunking.py
├── document_processor.py
├── functions.py
├── ticket_manager.py
├── vector_store.py
└── integrations/
    ├── __init__.py
    └── github_issues.py
data/
└── documents/
    └── [your PDF files here]
```

### Step 4: Configure Secrets

In your HuggingFace Space settings, add these secrets:

```
GOOGLE_API_KEY = your_google_api_key
GITHUB_TOKEN = your_github_token
GITHUB_REPO_OWNER = your_username
GITHUB_REPO_NAME = support-tickets
COMPANY_NAME = Your Company Name
COMPANY_EMAIL = support@company.com
COMPANY_PHONE = +1-800-123-4567
```

### Step 5: Deploy

HuggingFace will automatically build and deploy your app. The build process will:
1. Install dependencies from `requirements.txt`
2. Run your `app.py`

### Step 6: Initialize Database (First Time)

After deployment, you need to initialize the database once. You have two options:

**Option A: Run init script via Space**
- Create a simple toggle in the Streamlit app to run initialization
- Or run it manually through the Space's terminal (if available)

**Option B: Pre-build the vector database**
- Run `python init_database.py` locally
- Upload the entire `data/vector_db/` folder to HuggingFace Space

## Troubleshooting

### Common Issues

**1. "No PDF files found"**
- Ensure PDF files are in `data/documents/` folder
- Check file extensions are `.pdf` (lowercase)

**2. "GOOGLE_API_KEY is not set"**
- Verify `.env` file exists (local) or secrets are set (HuggingFace)
- Check for typos in variable names

**3. "Failed to connect to GitHub"**
- Verify GitHub token has `repo` scope
- Ensure repository exists and is accessible
- Check repository owner and name are correct

**4. ChromaDB initialization errors**
- Delete `data/vector_db/` folder and reinitialize
- Ensure sufficient disk space

**5. Streamlit connection errors (HuggingFace)**
- Check Space logs for detailed error messages
- Verify all dependencies are in `requirements.txt`
- Ensure Python version matches `.python-version`

## Testing the Application

Once running, test these features:

1. **Ask a question** from your documents
   - Verify it returns an answer with citation
   - Check format: `[Document Name, Page X]`

2. **Test ticket creation**
   - Ask a question not in documents
   - System should suggest creating a ticket
   - Or directly request: "I want to create a support ticket"
   - Fill in your name and email in sidebar
   - Verify ticket appears in GitHub Issues

3. **Company information**
   - Ask: "How can I contact support?"
   - Should return company name, email, phone

4. **Conversation history**
   - Ask multiple related questions
   - Verify context is maintained
   - Test "Clear Conversation" button

## Performance Optimization

For better performance:

1. **Reduce chunk size** if processing is slow:
   ```python
   # In config.py
   CHUNK_SIZE = 500
   CHUNK_OVERLAP = 100
   ```

2. **Limit search results**:
   ```python
   # In config.py
   TOP_K_RESULTS = 2
   ```

3. **Use smaller embedding model** (trade-off with accuracy):
   ```python
   # In src/vector_store.py
   self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Current (fast)
   # or
   self.embedding_model = SentenceTransformer('paraphrase-MiniLM-L3-v2')  # Faster
   ```

## Updating Documents

To add or update PDF documents:

1. Add new PDFs to `data/documents/`
2. Run initialization again:
   ```bash
   python init_database.py
   ```
3. Restart the Streamlit app

## Monitoring

Monitor your application:

- **Local**: Check terminal logs
- **HuggingFace**: Check Space logs in the UI
- **GitHub Issues**: Monitor created tickets in your repository
- **Google Gemini**: Check API usage in Google Cloud Console

## Next Steps

After successful deployment:

1. Customize the UI styling in `app.py`
2. Add more function calling capabilities
3. Implement analytics tracking
4. Set up automated testing
5. Configure custom domain (HuggingFace Pro)
