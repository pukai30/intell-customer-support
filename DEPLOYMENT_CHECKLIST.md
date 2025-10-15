# Deployment Checklist

Use this checklist to run your Intelligent Customer Support System locally or deploy to production.

## 🖥️ Local Development Setup

Follow these steps to run the system on your local machine for development and testing.

### Step 1: Prerequisites

- [ ] Python 3.12 or higher installed
  ```bash
  python --version  # Should be 3.12+
  ```

- [ ] MongoDB installed and running
  - **Windows:** Download from https://www.mongodb.com/try/download/community
  - **Mac:** `brew install mongodb-community`
  - **Linux:** `sudo apt-get install mongodb`
  
  ```bash
  # Start MongoDB
  mongod
  
  # Verify it's running (in another terminal)
  mongosh  # or mongo
  ```

- [ ] Git installed (to clone the repository)

### Step 2: Clone and Install

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd intell-customer-support

# Install dependencies
pip install -e .

# This installs all required packages including:
# - FastAPI, Uvicorn
# - Langchain, OpenAI
# - MongoDB drivers
# - Twilio SDK
# - And more...
```

### Step 3: Create Environment File

Create a `.env` file in the root directory:

```bash
# Copy the example (if available) or create new
touch .env
```

**Minimum required configuration for local testing:**

```env
# OpenAI (Required)
OPENAI_API_KEY=sk-your-openai-api-key-here

# MongoDB (Required)
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=customer_support

# Email (Optional - comment out if not testing email)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USER=your-email@gmail.com
# EMAIL_PASSWORD=your-gmail-app-password
# IMAP_HOST=imap.gmail.com
# IMAP_PORT=993

# Twilio (Optional - comment out if not testing SMS/WhatsApp)
# TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
# TWILIO_AUTH_TOKEN=your-auth-token
# TWILIO_PHONE_NUMBER=+1234567890
# TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Application Settings
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True

# Knowledge Base
KNOWLEDGE_BASE_PATH=./knowledge_base
EMBEDDINGS_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4-turbo-preview
VECTOR_STORE_PATH=./vector_store
```

**Getting your OpenAI API key:**
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and paste it in your `.env` file

**For Gmail (if testing email):**
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the 16-character app password (not your regular password)

**For Twilio (if testing SMS/WhatsApp):**
1. Sign up at https://www.twilio.com/try-twilio
2. Get free trial credits
3. Get Account SID and Auth Token from Console
4. Get a trial phone number

### Step 4: Start the Application

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
Creating new vector store...
✓ RAG System initialized
✓ Background tasks started
  - Email monitoring: Every 2 minutes
  - Cleanup: Every 6 hours
✅ System ready!

INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 5: Verify Installation

```bash
# In a new terminal, test the health endpoint
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","database":"connected","rag_system":"initialized","timestamp":"..."}
```

### Step 6: Add Sample Knowledge

```bash
# Run the sample knowledge setup script
python setup_sample_knowledge.py
```

This adds 10 sample documents covering common support topics.

### Step 7: Test the System

**Option A: Run automated tests**
```bash
python test_system.py
```

**Option B: Test manually with curl**
```bash
# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I reset my password?",
    "customer_identifier": "test@example.com",
    "customer_name": "Test User"
  }'
```

**Option C: Use the interactive API docs**
- Open http://localhost:8000/docs in your browser
- Try out the API endpoints interactively

### Step 8: Development Workflow

While developing:

1. **Hot Reload:** The app runs with `DEBUG=True` by default, which enables auto-reload on code changes

2. **View Logs:** Check terminal output for real-time logs

3. **Monitor Database:**
   ```bash
   # Connect to MongoDB
   mongosh
   
   # Use the database
   use customer_support
   
   # View tickets
   db.tickets.find().pretty()
   
   # View knowledge
   db.knowledge.find().pretty()
   ```

4. **Test Webhooks Locally (SMS/WhatsApp):**
   ```bash
   # Install ngrok
   # Download from: https://ngrok.com/download
   
   # Expose local server
   ngrok http 8000
   
   # Use the ngrok URL in Twilio webhook settings
   # Example: https://abc123.ngrok.io/api/webhooks/sms
   ```

### Common Local Development Issues

**Issue: "Connection refused" to MongoDB**
```bash
# Make sure MongoDB is running
mongod

# Or check if it's running as a service
# Windows: services.msc → MongoDB Server
# Mac: brew services list
# Linux: sudo systemctl status mongod
```

**Issue: "Invalid API key" from OpenAI**
- Verify your API key in `.env` file
- Check you have credits: https://platform.openai.com/usage
- Make sure there are no extra spaces in the key

**Issue: Email integration errors**
- Comment out email variables in `.env` if not testing email
- Or use valid Gmail App Password (not regular password)

**Issue: Port 8000 already in use**
```bash
# Change port in .env
APP_PORT=8001

# Or kill the process using port 8000
# Windows: netstat -ano | findstr :8000
# Mac/Linux: lsof -i :8000
```

### Step 9: Making Changes

When developing new features:

1. **Edit code** in `app/` directory
2. **App auto-reloads** (if DEBUG=True)
3. **Test changes** using curl or /docs
4. **Check logs** in terminal
5. **Commit changes** to git

### Local Testing Checklist

- [ ] Application starts without errors
- [ ] MongoDB connection successful
- [ ] Health endpoint responds
- [ ] Can add knowledge via API
- [ ] Chat endpoint works and returns responses
- [ ] Confidence scores are calculated
- [ ] Tickets are created in database
- [ ] Conversation history is saved
- [ ] Background tasks are running (check logs)
- [ ] API documentation accessible at /docs

---

## ✅ Pre-Deployment (Production)

### 1. Environment Configuration
- [ ] Create production `.env` file with all required credentials
- [ ] Set `DEBUG=False` in production
- [ ] Update `APP_HOST` and `APP_PORT` as needed
- [ ] Configure production MongoDB connection string
- [ ] Verify OpenAI API key has sufficient credits
- [ ] Set up Twilio production phone numbers

### 2. Security
- [ ] Add authentication middleware to API endpoints
- [ ] Update CORS settings in `app/api.py` to allow only your frontend domain
- [ ] Enable HTTPS/SSL certificates
- [ ] Set up API rate limiting
- [ ] Implement request validation and sanitization
- [ ] Set up environment variable encryption/secrets management
- [ ] Configure firewall rules

### 3. Database
- [ ] Set up MongoDB Atlas cluster or production MongoDB server
- [ ] Configure database backups
- [ ] Set up database monitoring
- [ ] Create database indexes (done automatically on startup)
- [ ] Plan data retention policy

### 4. Knowledge Base
- [ ] Populate knowledge base with production content
- [ ] Test RAG responses for accuracy
- [ ] Set appropriate confidence thresholds
- [ ] Organize content by categories and tags

## 🚀 Deployment Steps

### Option A: Traditional Server (VPS/EC2)

1. **Prepare Server**
   ```bash
   # Install Python 3.12
   sudo apt update
   sudo apt install python3.12 python3-pip
   
   # Install MongoDB
   # See: https://www.mongodb.com/docs/manual/installation/
   
   # Clone repository
   git clone <your-repo>
   cd intell-customer-support
   ```

2. **Install Dependencies**
   ```bash
   pip install -e .
   ```

3. **Configure Environment**
   ```bash
   # Copy and edit .env file
   nano .env
   ```

4. **Run with Process Manager**
   ```bash
   # Install PM2 or Supervisor
   pip install supervisor
   
   # Or use systemd
   sudo nano /etc/systemd/system/customer-support.service
   ```

   Sample systemd service:
   ```ini
   [Unit]
   Description=Customer Support API
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/path/to/intell-customer-support
   ExecStart=/usr/bin/python3 main.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Set Up Reverse Proxy (Nginx)**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Option B: Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.12-slim

   WORKDIR /app
   COPY . .

   RUN pip install -e .

   EXPOSE 8000
   CMD ["python", "main.py"]
   ```

2. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   services:
     api:
       build: .
       ports:
         - "8000:8000"
       env_file:
         - .env
       depends_on:
         - mongodb

     mongodb:
       image: mongo:latest
       ports:
         - "27017:27017"
       volumes:
         - mongo-data:/data/db

   volumes:
     mongo-data:
   ```

3. **Deploy**
   ```bash
   docker-compose up -d
   ```

### Option C: Cloud Platform (Heroku, Railway, Render)

1. **Add Procfile**
   ```
   web: python main.py
   ```

2. **Configure buildpacks** (if needed)
   ```bash
   heroku buildpacks:set heroku/python
   ```

3. **Set environment variables** in platform dashboard

4. **Deploy**
   ```bash
   git push heroku main
   ```

## 🔧 Post-Deployment

### 1. Twilio Webhook Configuration
- [ ] Update SMS webhook URL in Twilio Console
  - `https://yourdomain.com/api/webhooks/sms`
- [ ] Update WhatsApp webhook URL in Twilio Console
  - `https://yourdomain.com/api/webhooks/whatsapp`
- [ ] Test webhooks with Twilio debugger

### 2. Email Configuration
- [ ] Verify email sending works in production
- [ ] Test email receiving/monitoring
- [ ] Configure email forwarding if needed
- [ ] Set up email alerts for system errors

### 3. Monitoring & Logging
- [ ] Set up application monitoring (e.g., Sentry, DataDog)
- [ ] Configure log aggregation (e.g., ELK, Papertrail)
- [ ] Set up uptime monitoring (e.g., Pingdom, UptimeRobot)
- [ ] Create alerting rules for errors and downtime
- [ ] Monitor API response times

### 4. Performance Optimization
- [ ] Enable caching for frequently accessed data
- [ ] Optimize database queries
- [ ] Set up CDN if serving static files
- [ ] Configure connection pooling
- [ ] Monitor vector store performance

### 5. Backup & Recovery
- [ ] Set up automated MongoDB backups
- [ ] Export and backup vector store regularly
- [ ] Document recovery procedures
- [ ] Test backup restoration

## 📊 Monitoring Endpoints

Monitor these endpoints for system health:

```bash
# Health check
curl https://yourdomain.com/health

# System statistics
curl https://yourdomain.com/api/stats

# Open tickets count
curl https://yourdomain.com/api/tickets?status=open
```

## 🔒 Security Hardening

### API Security
- [ ] Implement API key authentication
- [ ] Add rate limiting (e.g., using slowapi)
- [ ] Enable CORS only for trusted domains
- [ ] Validate all input data
- [ ] Sanitize user messages
- [ ] Implement request signing for webhooks

### Infrastructure Security
- [ ] Keep all dependencies updated
- [ ] Regular security audits
- [ ] Enable firewall
- [ ] Use HTTPS everywhere
- [ ] Secure MongoDB (authentication, encryption at rest)
- [ ] Rotate API keys and secrets regularly

## 📈 Scaling Considerations

### Horizontal Scaling
- [ ] Use load balancer (Nginx, AWS ALB)
- [ ] Make application stateless
- [ ] Use external session storage
- [ ] Share vector store across instances

### Vertical Scaling
- [ ] Increase server resources as needed
- [ ] Optimize ChromaDB configuration
- [ ] Use connection pooling
- [ ] Implement caching layer (Redis)

### Database Scaling
- [ ] MongoDB replica sets for high availability
- [ ] Sharding for large datasets
- [ ] Read replicas for scaling reads

## 🧪 Production Testing

Before going live, test:
- [ ] All API endpoints work correctly
- [ ] Email sending and receiving
- [ ] SMS webhook functionality
- [ ] WhatsApp webhook functionality
- [ ] Chat conversation flow
- [ ] Knowledge base retrieval
- [ ] Ticket creation and management
- [ ] Background tasks execution
- [ ] Error handling and recovery
- [ ] Load testing (use tools like Locust, k6)

## 📱 Frontend Integration

For NextJS frontend:
- [ ] Update API endpoint URLs to production
- [ ] Implement error handling
- [ ] Add loading states
- [ ] Configure CORS
- [ ] Test end-to-end flow
- [ ] Deploy frontend to Vercel/Netlify

## 🚨 Incident Response

Create procedures for:
- [ ] API downtime
- [ ] Database failures
- [ ] High error rates
- [ ] Webhook failures
- [ ] OpenAI API issues
- [ ] Twilio service disruptions

## 📝 Documentation

Maintain:
- [ ] API documentation (Swagger at /docs)
- [ ] Deployment runbook
- [ ] Troubleshooting guide
- [ ] Architecture diagrams
- [ ] Team onboarding docs

## ✅ Launch Checklist

Final checks before going live:
- [ ] All environment variables configured
- [ ] SSL certificate installed and working
- [ ] Database backups configured
- [ ] Monitoring and alerting active
- [ ] Error tracking configured
- [ ] Knowledge base populated
- [ ] All tests passing
- [ ] Performance benchmarks met
- [ ] Security review completed
- [ ] Team trained on system
- [ ] Support procedures documented
- [ ] Rollback plan prepared

---

## Need Help?

- 📚 [README.md](README.md) - Full documentation
- 🚀 [QUICK_START.md](QUICK_START.md) - Quick start guide
- 🔧 [ENV_SETUP.md](ENV_SETUP.md) - Environment setup
- 🌐 API Docs: https://yourdomain.com/docs

**Good luck with your deployment! 🚀**

