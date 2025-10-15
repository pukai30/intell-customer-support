# Environment Setup Guide

This guide will help you set up the environment variables for the Intelligent Customer Support System.

## Required Environment Variables

Create a `.env` file in the root directory with the following variables:

### OpenAI Configuration
```env
OPENAI_API_KEY=your_openai_api_key_here
```
- Get your API key from: https://platform.openai.com/api-keys

### MongoDB Configuration
```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=customer_support
```
- Install MongoDB locally or use MongoDB Atlas: https://www.mongodb.com/cloud/atlas

### Email Configuration (Gmail Example)
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
```

**For Gmail:**
1. Enable 2-Factor Authentication on your Google Account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the App Password (not your regular password)

### Twilio Configuration (SMS & WhatsApp)
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

**Setup Twilio:**
1. Create account: https://www.twilio.com/try-twilio
2. Get your Account SID and Auth Token from the Console
3. Purchase a phone number with SMS/WhatsApp capabilities
4. For WhatsApp, use Twilio Sandbox or apply for WhatsApp Business API

### Application Configuration
```env
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True
```

### Knowledge Base Configuration
```env
KNOWLEDGE_BASE_PATH=./knowledge_base
EMBEDDINGS_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4-turbo-preview
VECTOR_STORE_PATH=./vector_store
```

## Complete .env Example

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx

# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=customer_support

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=support@yourcompany.com
EMAIL_PASSWORD=your_16_char_app_password
IMAP_HOST=imap.gmail.com
IMAP_PORT=993

# Twilio Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True

# Knowledge Base Configuration
KNOWLEDGE_BASE_PATH=./knowledge_base
EMBEDDINGS_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4-turbo-preview
VECTOR_STORE_PATH=./vector_store
```

## Installation Steps

1. **Install Python dependencies:**
   ```bash
   pip install -e .
   ```

2. **Install MongoDB:**
   - **Windows:** Download from https://www.mongodb.com/try/download/community
   - **Mac:** `brew install mongodb-community`
   - **Linux:** Follow official docs

3. **Start MongoDB:**
   ```bash
   mongod
   ```

4. **Create .env file with your credentials**

5. **Run the application:**
   ```bash
   python main.py
   ```

## Webhook Configuration (for Twilio)

### SMS Webhook
Set in Twilio Console → Phone Numbers → Your Number:
```
https://your-domain.com/api/webhooks/sms
```

### WhatsApp Webhook
Set in Twilio Console → WhatsApp → Sandbox or Your Number:
```
https://your-domain.com/api/webhooks/whatsapp
```

**For local development, use ngrok:**
```bash
ngrok http 8000
```
Then use the ngrok URL for webhooks.

## Testing the Setup

1. **Test the API:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Add knowledge to the system:**
   ```bash
   curl -X POST http://localhost:8000/api/knowledge/add \
     -H "Content-Type: application/json" \
     -d '{
       "title": "How to reset password",
       "content": "To reset your password: 1. Click 'Forgot Password' 2. Enter your email 3. Check your email for reset link",
       "category": "account",
       "tags": ["password", "security"]
     }'
   ```

3. **Test chat:**
   ```bash
   curl -X POST http://localhost:8000/api/chat \
     -H "Content-Type: application/json" \
     -d '{
       "message": "How do I reset my password?",
       "customer_identifier": "test@example.com"
     }'
   ```

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running: `mongosh` or `mongo`
- Check if port 27017 is available
- Verify MONGODB_URL in .env

### Email Not Working
- Verify Gmail App Password (not regular password)
- Check firewall for ports 587 (SMTP) and 993 (IMAP)
- Enable "Less secure app access" if using regular password (not recommended)

### Twilio Not Receiving Messages
- Verify webhook URLs are publicly accessible
- Use ngrok for local development
- Check Twilio debugger in console for errors

### OpenAI API Errors
- Verify API key is valid
- Check billing/credits in OpenAI account
- Ensure model names are correct (gpt-4-turbo-preview, text-embedding-3-small)

