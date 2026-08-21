# Streamlit Cloud Deployment Guide

## Prerequisites

1. **GitHub Account** - Your code must be pushed to a public GitHub repository
2. **Streamlit Account** - Sign up at [streamlit.io](https://streamlit.io)
3. **Groq API Key** - Get from [console.groq.com](https://console.groq.com)

---

## Step-by-Step Deployment Instructions

### Step 1: Prepare Your GitHub Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Grok Chatbot with LangGraph"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/KLE_Ganagavthi_GenAIGrok.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Make sure `.env` and `.streamlit/secrets.toml` are in `.gitignore`** ✅ (already configured)

---

### Step 2: Create Streamlit Cloud Account

1. Go to [streamlit.io](https://streamlit.io)
2. Click **"Sign Up"** or **"Log In"** (use GitHub for easier OAuth)
3. Complete the sign-up process

---

### Step 3: Deploy Your App

1. After signing in to Streamlit Cloud, click **"Create App"**
2. Fill in deployment details:
   - **Repository**: Select your GitHub repo `KLE_Ganagavthi_GenAIGrok`
   - **Branch**: `main`
   - **Main file path**: `main.py`

3. Click **"Deploy"** and wait for the build to complete (2-5 minutes)

---

### Step 4: Configure Secrets

**CRITICAL: Never commit `.env` or `secrets.toml` to GitHub!**

1. In Streamlit Cloud dashboard, open your deployed app settings
2. Click the **⋮ (three dots)** → **Edit secrets**
3. Add your secrets in TOML format:

```toml
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxx"
GROQ_MODEL = "qwen/qwen3.6-27b"
```

4. Click **"Save"**
5. Your app will restart automatically with the secrets loaded

---

### Step 5: Verify Deployment

1. Your app should now be live at: `https://grok-chatbot-YOUR_USERNAME.streamlit.app`
2. Test the chatbot:
   - Verify the UI loads correctly
   - Try the calculator tool with sample numbers
   - Test the greeting tool with a name
   - Check that model selection works

---

## Troubleshooting

### Issue: "GROQ_API_KEY is not set"
**Solution**: 
- Make sure you added the secret in Streamlit Cloud's secrets editor
- Wait for the app to restart after adding secrets
- Refresh your browser

### Issue: "Request timeout" or "Module not found"
**Solution**:
- Check `requirements.txt` has all dependencies
- Verify `main.py` is in the root directory
- Check logs in Streamlit Cloud dashboard

### Issue: "Agent is processing..." hangs indefinitely
**Solution**:
- Check Groq API status at [status.groq.com](https://status.groq.com)
- Reduce conversation history: Add cleanup logic for chat history
- Increase timeout in settings if available

### Issue: Chat history too large → Memory error
**Solution**:
- Streamlit Cloud free tier has 1GB RAM limit
- Implement chat history truncation in the app
- Clear chat history frequently via the "Clear Chat History" button

---

## Performance Tips for Free Tier

1. **Optimize dependencies**: Only install what you need
2. **Limit context window**: Truncate old messages periodically
3. **Use efficient models**: `mixtral-8x7b-32768` is faster than `llama-3.3-70b`
4. **Monitor memory**: Watch the Streamlit Cloud metrics dashboard
5. **Cache results**: Use `@st.cache_data` for expensive operations

---

## Upgrading from Free Tier

If you need more resources:
- **Compute**: Upgrade to Streamlit+ ($9/month per app)
- **Advanced features**: Custom domain, priority support
- **Alternative hosting**: AWS, Azure, Heroku, Railway.app

---

## Quick Reference

| File | Purpose |
|------|---------|
| `main.py` | Main Streamlit app |
| `requirements.txt` | Python dependencies |
| `.streamlit/config.toml` | Streamlit configuration |
| `.gitignore` | Files to exclude from git |
| `.env.example` | Template for local development |

---

## Local Development

To test locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example and add your API key)
cp .env.example .env

# Run locally
streamlit run main.py
```

Your app will open at `http://localhost:8501`

---

## Support & Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-cloud
- **LangChain Docs**: https://python.langchain.com
- **Groq API Docs**: https://console.groq.com/docs
