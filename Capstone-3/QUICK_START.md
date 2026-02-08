# STEP-BY-STEP: Running Your Customer Support System

## Current Status Check

Before running anything, let's verify your setup:

1. **Check if PDFs are in the right place:**
   - Open: `data\documents\` folder
   - You should see your PDF files there
   - If PDFs are in the `Sources` folder instead, move them to `data\documents\`

2. **Check if vector database exists:**
   - Look for: `data\vector_db\` folder
   - If it has files inside = database already created
   - If it's empty = you need to run initialization

---

## THE CORRECT WAY TO RUN

### Option 1: If Vector Database Doesn't Exist Yet

**Step 1:** Make sure PDFs are in `data\documents\`

**Step 2:** Run initialization (ONE TIME):
```bash
python init_database.py
```

Wait for it to complete. You'll see:
- Loading documents
- Generating embeddings (this is the "batching" - it's normal HERE)
- "Initialization complete!"

**Step 3:** Now run Streamlit:
```bash
streamlit run app.py
```

This time it should start FAST (no batching).

---

### Option 2: If Vector Database Already Exists

Just run:
```bash
streamlit run app.py
```

It should load instantly without any batching.

---

## If You Still See Batching in Streamlit

If you run `streamlit run app.py` and STILL see batching/embedding generation:

1. **Stop Streamlit** (Ctrl+C)

2. **Delete the vector database:**
```bash
rmdir /s /q data\vector_db
```

3. **Run initialization:**
```bash
python init_database.py
```

4. **Run Streamlit:**
```bash
streamlit run app.py
```

---

## What Each Command Does

### `python init_database.py`
- Loads all PDF files from `data\documents\`
- Extracts text with page numbers
- Creates text chunks
- Generates embeddings (the "batching" you see)
- Saves everything to `data\vector_db\`
- **Run this ONCE** or when you add new documents

### `streamlit run app.py`
- Loads the EXISTING vector database from `data\vector_db\`
- Starts the web interface
- **Should be FAST** (no processing)
- Run this every time you want to use the app

---

## Quick Troubleshooting

**Problem:** "Vector database is empty" error in Streamlit
**Solution:** Run `python init_database.py` first

**Problem:** Still seeing batching in Streamlit
**Solution:** The old vector_db might be corrupted. Delete it and reinitialize:
```bash
rmdir /s /q data\vector_db
python init_database.py
streamlit run app.py
```

**Problem:** No PDF files found
**Solution:** Move your PDFs from `Sources` folder to `data\documents\` folder

---

## Expected Behavior

### FIRST TIME (Initialization):
```bash
> python init_database.py
Loading PDF: manual1.pdf (450 pages)
Loading PDF: manual2.pdf (120 pages)
Loading PDF: manual3.pdf (50 pages)
Generating embeddings: 100%|████████| 620/620  ← THIS IS NORMAL HERE
Initialization complete!
```

### EVERY TIME AFTER (Running Streamlit):
```bash
> streamlit run app.py
Loading embedding model...  ← Quick!
Embedding model loaded      ← Fast!

  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

No batching or progress bars should appear in Streamlit anymore!
