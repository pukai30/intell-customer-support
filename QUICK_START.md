# Quick Start Guide

Get your Intelligent Customer Support System up and running in minutes!

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.12 or higher installed
- ✅ MongoDB installed and running
- ✅ OpenAI API key
- ✅ (Optional) Twilio account for SMS/WhatsApp
- ✅ (Optional) Email account for email support

## Step-by-Step Setup

### Step 1: Install Dependencies

```bash
pip install -e .
```

This will install all required packages including:
- FastAPI, Uvicorn (API server)
- Langchain, OpenAI (AI/RAG system)
- MongoDB drivers
- Twilio SDK
- Email libraries
- And more...

### Step 2: Start MongoDB

**Option A: Local MongoDB**
```bash
# On Windows
mongod

# On Mac/Linux
sudo mongod
```

**Option B: MongoDB Atlas (Cloud)**
- Sign up at https://www.mongodb.com/cloud/atlas
- Create a free cluster
- Get connection string
- Use it in your `.env` file

### Step 3: Create Environment File

Create a `.env` file in the root directory:

```env
# Minimum required configuration
OPENAI_API_KEY=sk-your-api-key-here
MONGODB_URL=mongodb://localhost:27017

# Email (optional - for email support)
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Twilio (optional - for SMS/WhatsApp)
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+1234567890
```

**Getting OpenAI API Key:**
1. Visit https://platform.openai.com/api-keys
2. Create new secret key
3. Copy and paste into `.env`

### Step 4: Run the Application

```bash
python main.py
```

You should see:
```
╔═══════════════════════════════════════════════════════════╗
║   Intelligent Customer Support System                    ║
║   RAG-based Multi-Channel Support Platform               ║
╚═══════════════════════════════════════════════════════════╝

✓ Connected to MongoDB: customer_support
Loading existing vector store...
✓ RAG System initialized
✓ Background tasks started
  - Email monitoring: Every 2 minutes
  - Cleanup: Every 6 hours
✅ System ready!

INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Add Sample Knowledge

Open a new terminal and run:

```bash
python setup_sample_knowledge.py
```

This will populate your knowledge base with 10 sample documents covering:
- Account creation
- Password reset
- Business hours
- Payment methods
- Subscriptions
- And more...

### Step 6: Test the System

Run the test suite:

```bash
python test_system.py
```

Or test manually using curl:

```bash
# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I reset my password?",
    "customer_identifier": "test@example.com"
  }'
```

### Step 7: Explore the API

Visit the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## What's Next?

### 1. Customize Knowledge Base

Add your own knowledge:

```python
import requests

requests.post('http://localhost:8000/api/knowledge/add', json={
    "title": "Your Custom FAQ",
    "content": "Your detailed answer here...",
    "category": "custom",
    "tags": ["tag1", "tag2"]
})
```

### 2. Set Up Email Support

1. Enable App Password in Gmail
2. Update `.env` with credentials
3. The system will automatically check for new emails every 2 minutes

### 3. Set Up SMS/WhatsApp

1. Create Twilio account
2. Get phone number with SMS/WhatsApp
3. Update `.env` with Twilio credentials
4. Configure webhooks (use ngrok for local development)

### 4. Build Your NextJS Frontend

Use the provided API endpoints to build your chat interface:

```javascript
// Example React/NextJS code
const sendMessage = async (message) => {
  const response = await fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: message,
      customer_identifier: userEmail,
      conversation_id: conversationId
    })
  });
  
  const data = await response.json();
  return data.response;
};
```

## Common Issues

### "Connection refused" error
- Make sure MongoDB is running: `mongod`
- Check if port 27017 is available

### "OpenAI API error"
- Verify your API key is correct
- Check you have credits/billing set up in OpenAI account

### Email not working
- Use Gmail App Password (not regular password)
- Enable 2FA and generate app password
- Check firewall allows ports 587 and 993

### Twilio webhooks not working locally
- Use ngrok to expose local server: `ngrok http 8000`
- Use the ngrok URL in Twilio webhook configuration

## Architecture Overview

```
┌─────────────┐
│   Channels  │  Email, SMS, WhatsApp, Web Chat
└──────┬──────┘
       │
┌──────▼──────┐
│  FastAPI    │  REST API Server
└──────┬──────┘
       │
┌──────▼──────────────────────┐
│  RAG System (Langchain)     │  AI-powered responses
│  - OpenAI Embeddings        │
│  - ChromaDB Vector Store    │
│  - GPT-4 Generation         │
└──────┬──────────────────────┘
       │
┌──────▼──────┐
│  MongoDB    │  Ticket & Knowledge Storage
└─────────────┘
```

## Key Features

✅ **Multi-Channel Support**
- Web chat (REST API)
- Email (IMAP/SMTP)
- SMS (Twilio)
- WhatsApp (Twilio)

✅ **Intelligent Responses**
- RAG-based AI using GPT-4
- Semantic search with embeddings
- Confidence scoring
- Context-aware conversations

✅ **Ticket Management**
- Automatic ticket creation
- Full conversation history
- Status tracking
- Cross-channel support

✅ **Knowledge Base**
- Vector embeddings for semantic search
- Support for PDF, DOCX, TXT files
- Category and tag organization
- Easy content management

## Next Steps

1. ✅ System is running
2. ✅ Knowledge base populated
3. ✅ Tested basic functionality
4. 📝 Customize knowledge for your use case
5. 📝 Set up additional channels (email, SMS, WhatsApp)
6. 📝 Build your NextJS frontend
7. 📝 Deploy to production

## Need Help?

- 📚 Full documentation: [README.md](README.md)
- 🔧 Environment setup: [ENV_SETUP.md](ENV_SETUP.md)
- 🌐 API docs: http://localhost:8000/docs
- 🧪 Run tests: `python test_system.py`

---

**Congratulations! Your Intelligent Customer Support System is ready! 🎉**

