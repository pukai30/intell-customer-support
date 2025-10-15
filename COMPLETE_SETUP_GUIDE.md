# Complete Setup Guide - Backend + Frontend

End-to-end setup guide for the Intelligent Customer Support System with Python backend and NextJS frontend.

## 📋 Overview

This system consists of:
1. **Python Backend** - FastAPI + Langchain + MongoDB + RAG
2. **NextJS Frontend** - React + TypeScript + Tailwind CSS

## 🎯 Prerequisites

### Required Software
- ✅ **Python 3.12+**
- ✅ **Node.js 18+**
- ✅ **MongoDB** (local or Atlas)
- ✅ **OpenAI API Key**

### Optional (for full features)
- Twilio Account (SMS/WhatsApp)
- Gmail Account (Email support)

## 🚀 Quick Start (5 Minutes)

### Step 1: Backend Setup

```bash
# Install Python dependencies
pip install -e .

# Create .env file
cat > .env << EOF
OPENAI_API_KEY=sk-your-key-here
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=customer_support

# Email (use Gmail App Password)
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-16-char-app-password

APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True
EOF
```

### Step 2: Start MongoDB

```bash
# On Windows
mongod

# On Mac/Linux
sudo mongod
```

### Step 3: Start Backend

```bash
python main.py
```

Backend will run on **http://localhost:8000**

### Step 4: Load IT Support Knowledge

```bash
# In a new terminal
python it_support_knowledge_mnc.py
```

This loads 11 comprehensive IT support documents.

### Step 5: Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on **http://localhost:3000**

### Step 6: Open Browser

```
http://localhost:3000
```

**🎉 You're ready!**

## 📊 What You'll See

### Home Page
- Welcome screen
- Quick links to Knowledge Base and Tickets
- Feature overview

### Knowledge Base Page
- Table of all knowledge documents
- Upload button for PDF/DOCX/TXT files
- Create button for manual entries
- Edit/Delete actions
- Category filter

### Email Tickets Page
- Table of all support tickets
- Auto-refresh every 10 seconds
- Full conversation history
- Filter by status/channel

## 🔧 Detailed Setup

### Backend Configuration

**1. Environment Variables (.env)**

```env
# REQUIRED
OPENAI_API_KEY=sk-proj-your-actual-key
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=customer_support

# EMAIL SUPPORT
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop  # Gmail App Password
IMAP_HOST=imap.gmail.com
IMAP_PORT=993

# APPLICATION
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True

# KNOWLEDGE BASE
KNOWLEDGE_BASE_PATH=./knowledge_base
EMBEDDINGS_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4-turbo-preview
VECTOR_STORE_PATH=./vector_store

# OPTIONAL: TWILIO (for SMS/WhatsApp)
# TWILIO_ACCOUNT_SID=ACxxxxx
# TWILIO_AUTH_TOKEN=xxxxx
# TWILIO_PHONE_NUMBER=+1234567890
```

**2. Gmail App Password Setup**

1. Enable 2-Factor Authentication: https://myaccount.google.com/security
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Select "Mail" and your device
4. Copy the 16-character password
5. Use in `EMAIL_PASSWORD` (remove spaces)

### Frontend Configuration

**1. Environment Variables (.env.local)**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**2. Install Dependencies**

```bash
cd frontend
npm install
```

This installs:
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios
- date-fns

## 🧪 Testing the System

### Test 1: Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "rag_system": "initialized"
}
```

### Test 2: Upload Knowledge (Frontend)

1. Go to http://localhost:3000/knowledge-base
2. Click "📤 Upload File"
3. Select a PDF/DOCX/TXT file
4. Set category and tags
5. Click "Upload"
6. See it appear in the table

### Test 3: Create Knowledge (Frontend)

1. Click "➕ Create Knowledge"
2. Fill in title and content
3. Set category
4. Click "Create Knowledge"
5. See it in the table

### Test 4: Chat API (Backend)

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I reset my password?",
    "customer_identifier": "test@example.com"
  }'
```

### Test 5: View Tickets (Frontend)

1. Go to http://localhost:3000/tickets
2. See any existing tickets
3. Toggle auto-refresh
4. Click "View" to see conversation

## 🎯 Complete Workflow

### 1. Knowledge Base Management

**Upload IT Documentation:**
```bash
# Backend loads knowledge
python it_support_knowledge_mnc.py
```

**Upload via UI:**
1. Frontend: Click "Upload File"
2. Select `company_policy.pdf`
3. Category: "policy"
4. Tags: "hr, compliance"
5. Upload → Auto-extracted and vectorized

**Create Manual Entry:**
1. Frontend: Click "Create Knowledge"
2. Title: "Emergency Contact"
3. Content: "For emergencies, call..."
4. Category: "emergency"
5. Create → Added to RAG system

### 2. Email Support Flow

**Automatic:**
1. Customer sends email to configured address
2. Backend checks email every 2 minutes
3. Creates ticket automatically
4. RAG system analyzes question
5. If confidence > 70%, auto-responds
6. Ticket appears in frontend immediately (10s refresh)

**Manual Monitoring:**
1. Frontend: Go to Tickets page
2. See new ticket appear
3. Click "View" to see conversation
4. Check AI confidence score
5. Update status if needed

### 3. Temporary Knowledge

**Use Case: Maintenance Window**

1. Frontend: Create Knowledge
2. Title: "System Maintenance - Jan 20"
3. Content: "System will be offline..."
4. Check "Temporary knowledge"
5. Expires in: 3 days
6. After 3 days: Auto-deleted by background task

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│          NextJS Frontend                │
│     http://localhost:3000               │
│                                         │
│  ┌──────────────┐  ┌─────────────────┐ │
│  │  Knowledge   │  │  Email Tickets  │ │
│  │     Base     │  │   Monitoring    │ │
│  └──────────────┘  └─────────────────┘ │
└─────────────────┬───────────────────────┘
                  │ REST API
                  ▼
┌─────────────────────────────────────────┐
│       Python Backend (FastAPI)          │
│     http://localhost:8000               │
│                                         │
│  ┌─────────┐  ┌──────────┐  ┌────────┐ │
│  │   RAG   │  │ MongoDB  │  │ Channels│ │
│  │ System  │  │ Database │  │ Email   │ │
│  │Langchain│  │          │  │ SMS/WA  │ │
│  └─────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────┘
                  │
                  ▼
           ┌──────────────┐
           │   MongoDB    │
           │ Port: 27017  │
           └──────────────┘
```

## 🔄 Data Flow

### Knowledge Upload Flow
```
Frontend Upload → Backend API → Extract Content → 
Chunk Text → Generate Embeddings → Store in ChromaDB → 
Save Metadata in MongoDB → Return Success
```

### Ticket Creation Flow
```
Email Received → Backend Monitors → Create Ticket → 
RAG Analyzes → Generate Response → Store Conversation → 
Frontend Auto-Refreshes → Display Ticket
```

## 🛠️ Troubleshooting

### Backend Issues

**"Cannot connect to MongoDB"**
```bash
# Check if MongoDB is running
mongosh  # or mongo

# If not, start it
mongod
```

**"Invalid OpenAI API key"**
- Verify key at https://platform.openai.com/api-keys
- Check billing at https://platform.openai.com/usage
- Ensure key starts with `sk-`

**"Email authentication failed"**
- Use Gmail App Password (NOT regular password)
- Generate at https://myaccount.google.com/apppasswords
- Enable 2FA first

### Frontend Issues

**"Cannot connect to backend"**
```bash
# Ensure backend is running
curl http://localhost:8000/health

# Check .env.local
cat frontend/.env.local
# Should have: NEXT_PUBLIC_API_URL=http://localhost:8000
```

**"Auto-refresh not working"**
- Check browser console for errors
- Toggle auto-refresh off/on
- Use manual refresh button

**"File upload fails"**
- Check file type (PDF, DOCX, TXT only)
- Check backend logs for errors
- Ensure backend is running

### Common Issues

**Port already in use**
```bash
# Backend (8000)
# Windows: netstat -ano | findstr :8000
# Mac/Linux: lsof -i :8000

# Frontend (3000)
# Windows: netstat -ano | findstr :3000
# Mac/Linux: lsof -i :3000
```

## 📁 Project Structure

```
intell-customer-support/
├── app/                    # Python backend
│   ├── api.py
│   ├── rag_system.py
│   ├── database.py
│   └── ...
├── frontend/               # NextJS frontend
│   ├── app/
│   │   ├── knowledge-base/
│   │   └── tickets/
│   ├── components/
│   └── lib/
├── knowledge_base/         # Uploaded files
├── vector_store/          # ChromaDB storage
├── main.py                # Backend entry
├── it_support_knowledge_mnc.py
└── .env                   # Backend config
```

## 🎓 Next Steps

### After Setup

1. **Customize Knowledge Base**
   - Upload your company documentation
   - Create custom categories
   - Add specific FAQs

2. **Configure Email**
   - Set up email forwarding to support address
   - Test email-to-ticket flow
   - Verify auto-responses

3. **Monitor Performance**
   - Check RAG confidence scores
   - Review auto-resolved vs manual tickets
   - Adjust confidence thresholds if needed

4. **Optional: Add Twilio**
   - Get Twilio account
   - Add credentials to `.env`
   - Set up webhooks (use ngrok for local testing)

### Production Deployment

**Backend:**
- Deploy to AWS/DigitalOcean/Heroku
- Use production MongoDB (Atlas)
- Set up HTTPS
- Configure firewall
- See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

**Frontend:**
- Deploy to Vercel (recommended)
- Update `NEXT_PUBLIC_API_URL` to production backend
- Configure custom domain
- Enable analytics

## 📝 Available Scripts

### Backend
```bash
python main.py                      # Start backend
python it_support_knowledge_mnc.py  # Load IT knowledge
python setup_sample_knowledge.py    # Load sample knowledge
python test_system.py              # Run tests
```

### Frontend
```bash
npm run dev    # Development server
npm run build  # Production build
npm start      # Production server
npm run lint   # Run linter
```

## 📚 Documentation Files

- `README.md` - Main documentation
- `QUICK_START.md` - Quick start guide
- `ENV_SETUP.md` - Environment setup
- `DEPLOYMENT_CHECKLIST.md` - Production deployment
- `KNOWLEDGE_BASE_MANAGEMENT.md` - KB API guide
- `FRONTEND_SETUP_GUIDE.md` - Frontend guide
- `COMPLETE_SETUP_GUIDE.md` - This file

## 🎯 Success Checklist

- [ ] Backend running on http://localhost:8000
- [ ] MongoDB connected and running
- [ ] IT knowledge loaded (11 documents)
- [ ] Frontend running on http://localhost:3000
- [ ] Can upload files via UI
- [ ] Can create knowledge via UI
- [ ] Can view tickets in real-time
- [ ] Auto-refresh working
- [ ] Can test chat API

## 🔐 Security Notes

**Development:**
- Never commit `.env` file
- Use `.env.example` for templates
- Keep API keys secure

**Production:**
- Use environment variables
- Enable authentication
- Set up CORS properly
- Use HTTPS everywhere
- Regular security audits

## 📞 Support

For issues:
1. Check this guide
2. Review error messages
3. Check browser/terminal console
4. Verify all services running
5. Review API documentation at `/docs`

---

**Congratulations! Your intelligent customer support system is fully operational! 🎉**

**Backend:** http://localhost:8000
**Frontend:** http://localhost:3000
**API Docs:** http://localhost:8000/docs

