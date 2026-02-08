# Scripture Assistant (Divine Wisdom)

An AI-powered spiritual guide dedicated to searching God's Word across the **Torah, Bible, and Quran**. It provides scholarly answers with transparent citations and allows users to submit formal inquiries to human scholars.

## Features

- **3-Script Search:** Simultaneously searches the Torah, Bible, and Quran to provide comparative wisdom.
- **Transparent Citations:** Every response lists the specific books and versions used (e.g., *King James Bible, John 3:16*).
- **Conversational Inquiries:** If you report an error or provide feedback, the Assistant intelligently asks for your Name/Email and creates a formal support ticket.
- **Divine Light UI:** A premium, forced Light Mode interface designed for readability and aesthetic beauty.
- **GitHub Integration:** Inquiries are automatically tracked as GitHub Issues.

## Tech Stack

- **AI Model:** OpenAI `gpt-4o-mini`
- **Vector Database:** ChromaDB (Local)
- **Interface:** Streamlit
- **Issue Tracking:** GitHub API

## Quick Start

1.  **Clone & Install**
    ```bash
    git clone <repository-url>
    pip install -r requirements.txt
    ```

2.  **Configure Environment**
    Create a `.env` file with your credentials (optional, or enter in UI):
    ```ini
    GITHUB_TOKEN=ghp_...
    GITHUB_REPO_OWNER=your_username
    GITHUB_REPO_NAME=your_repo_name
    ```
    *Note: OpenAI API Key can be entered directly in the App Sidebar.*

3.  **Add Holy Books**
    Place your PDF files (Torah, Bible, Quran) in the `data/documents` folder.
    *Note: The system requires at least 3 documents to function correctly.*

4.  **Run the App**
    ```bash
    streamlit run app.py
    ```

## Usage Guide

- **Ask Questions:** "What do the scriptures say about patience?"
- **Report Errors:** "I believe this verse citation is incorrect." -> System will ask for details and create a ticket.
- **View Sources:** Check the "Sources Used" section at the bottom of every response.

## Deployment to HuggingFace Spaces

This application is ready for HuggingFace Spaces.

1.  **Create New Space:**
    *   Go to [HuggingFace Spaces](https://huggingface.co/spaces) and create a new Space.
    *   Select **Streamlit** as the SDK.

2.  **Upload Files:**
    *   Upload all files from this repository (excluding `.env`, `.git`, `__pycache__`).
    *   Ensure `requirements.txt` is present.

3.  **Configure Secrets:**
    *   Go to **Settings** > **Variables and secrets**.
    *   Add the following **Secrets**:
        *   `OPENAI_API_KEY`: Your OpenAI Key.
        *   `GITHUB_TOKEN`: Your GitHub Token.
    *   Add the following **Variables** (optional overrides):
        *   `GITHUB_REPO_OWNER`
        *   `GITHUB_REPO_NAME`

4.  **Documents:**
    *   Ensure your `data/documents` folder containing the holy books (PDFs) is uploaded.

The app will build and launch automatically!
