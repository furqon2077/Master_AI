# API Keys Setup Guide

## 1. Google Gemini API Key

### Steps to Get Google Gemini API Key:

1. **Visit Google AI Studio**
   - Go to: https://aistudio.google.com/app/apikey
   - Sign in with your Google account

2. **Create API Key**
   - Click "Get API Key" or "Create API Key" button
   - Select "Create API key in new project" (recommended) or use existing project
   - Copy the generated API key

3. **Important Notes**
   - Keep your API key secure and never share it publicly
   - Free tier includes: 60 requests per minute
   - The key starts with `AIzaSy...`

4. **Add to .env file**
   ```
   GOOGLE_API_KEY=AIzaSy...your_actual_key_here
   ```

---

## 2. GitHub Personal Access Token

### Steps to Get GitHub Token:

1. **Go to GitHub Settings**
   - Visit: https://github.com/settings/tokens
   - Or: GitHub Profile > Settings > Developer settings > Personal access tokens > Tokens (classic)

2. **Generate New Token**
   - Click "Generate new token" > "Generate new token (classic)"
   - Give it a descriptive name: "Customer Support RAG System"
   - Set expiration: Choose based on your preference (30 days, 90 days, or no expiration)

3. **Select Scopes**
   - Check the `repo` scope (this gives full control of private repositories)
   - This includes: repo:status, repo_deployment, public_repo, repo:invite

4. **Generate and Copy**
   - Click "Generate token" at the bottom
   - **IMPORTANT**: Copy the token immediately - you won't be able to see it again!
   - The token starts with `ghp_...`

5. **Add to .env file**
   ```
   GITHUB_TOKEN=ghp_...your_actual_token_here
   ```

---

## 3. Create GitHub Repository for Support Tickets

1. **Create New Repository**
   - Go to: https://github.com/new
   - Repository name: `support-tickets` (or any name you prefer)
   - Make it Private or Public (your choice)
   - Click "Create repository"

2. **Add to .env file**
   ```
   GITHUB_REPO_OWNER=your_github_username
   GITHUB_REPO_NAME=support-tickets
   ```

---

## Complete .env Configuration

After getting all API keys, your `.env` file should look like:

```env
# Google Gemini API Key
GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# GitHub Configuration
GITHUB_TOKEN=ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
GITHUB_REPO_OWNER=your_github_username
GITHUB_REPO_NAME=support-tickets

# Company Information
COMPANY_NAME=Your Company Name
COMPANY_EMAIL=support@yourcompany.com
COMPANY_PHONE=+1-800-123-4567

# ChromaDB Configuration
CHROMA_PERSIST_DIR=./data/vector_db
COLLECTION_NAME=support_documents
```

---

## Security Best Practices

1. **Never commit .env to Git**
   - Already included in `.gitignore`
   - Double-check before pushing code

2. **Use different keys for development and production**
   - Create separate projects/tokens if possible

3. **Rotate keys periodically**
   - GitHub tokens can be regenerated
   - Create new Google API keys as needed

4. **For HuggingFace Spaces**
   - Don't upload `.env` file
   - Use the Secrets feature instead

---

## Testing Your Keys

After adding keys to `.env`, test them:

```bash
# Test the configuration
python -c "from config import Config; print('Google API Key:', 'Set' if Config.GOOGLE_API_KEY else 'Not Set'); print('GitHub Token:', 'Set' if Config.GITHUB_TOKEN else 'Not Set')"
```

---

## Troubleshooting

**Google Gemini API Key Issues:**
- Error "API key not valid": Make sure you copied the entire key
- Error "quota exceeded": You've hit the free tier limit (60 requests/min)
- Solution: Wait a minute or upgrade to paid tier

**GitHub Token Issues:**
- Error "Bad credentials": Token is invalid or expired
- Error "Not Found": Repository name or owner is incorrect
- Solution: Regenerate token with proper scopes

---

## Quick Links

- Google AI Studio: https://aistudio.google.com/app/apikey
- GitHub Tokens: https://github.com/settings/tokens
- Create GitHub Repo: https://github.com/new
- Google AI Pricing: https://ai.google.dev/pricing
- GitHub Token Docs: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
