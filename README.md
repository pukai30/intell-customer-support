# Intelligent Customer Support System

A comprehensive RAG-based (Retrieval Augmented Generation) customer support platform with multi-channel integration including Email, SMS, WhatsApp, and Web Chat.

## 🌟 Features

- **Multi-Channel Support**: 
  - Web Chat Interface (REST API for NextJS frontend)
  - Email (IMAP/SMTP)
  - SMS (via Twilio)
  - WhatsApp (via Twilio Business API)

- **Intelligent AI Responses**:
  - RAG-based system using Langchain and OpenAI
  - Vector embeddings with ChromaDB
  - Automatic response generation with confidence scoring
  - Context-aware conversations

- **Ticket Management**:
  - Full conversation history persistence in MongoDB
  - Automatic ticket creation and tracking
  - Multi-channel unified ticketing
  - Status management (open, pending, resolved, closed)

- **Knowledge Base**:
  - Document ingestion (PDF, DOCX, TXT)
  - Vector embeddings for semantic search
  - Category and tag-based organization
  - Easy content management via API

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Channels                         │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────────────┐   │
│  │Email │  │ SMS  │  │WhatsApp│ │  Web Chat   │   │
│  └──┬───┘  └──┬───┘  └───┬──┘  └──────┬───────┘   │
└─────┼─────────┼──────────┼─────────────┼───────────┘
      │         │          │             │
      └─────────┴──────────┴─────────────┘
                         │
                    ┌────▼─────┐
                    │  FastAPI │
                    │    API   │
                    └────┬─────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼─────┐    ┌────▼─────┐    ┌────▼─────┐
   │   RAG    │    │ MongoDB  │    │ Background│
   │  System  │    │ Database │    │   Tasks   │
   │(Langchain)│    │          │    │           │
   └──────────┘    └──────────┘    └───────────┘
```

## 📋 Prerequisites

- Python 3.12+
- MongoDB (local or Atlas)
- OpenAI API Key
- Twilio Account (for SMS/WhatsApp)
- Email Account (Gmail recommended)

## 🚀 Quick Start

### 1. Clone and Install

```bash
git clone <repository-url>
cd intell-customer-support
pip install -e .
```

### 2. Setup Environment Variables

Create a `.env` file in the root directory. See [ENV_SETUP.md](ENV_SETUP.md) for detailed configuration.

```env
OPENAI_API_KEY=your_openai_key
MONGODB_URL=mongodb://localhost:27017
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
# ... see ENV_SETUP.md for complete list
```

### 3. Start MongoDB

```bash
mongod
```

### 4. Run the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Interactive API Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Knowledge Base Management 🆕
Full CRUD operations with file upload, temporary knowledge (TTL), and IT support content:
- **Upload Files**: PDF, DOCX, TXT support
- **CRUD Operations**: Create, Read, Update, Delete
- **Temporary Knowledge**: Auto-expiry support
- **Categories & Tags**: Organize knowledge
- **Soft Delete**: Recovery option
- See [KNOWLEDGE_BASE_MANAGEMENT.md](KNOWLEDGE_BASE_MANAGEMENT.md) for complete guide

### Key Endpoints

#### Chat Interface
```bash
POST /api/chat
{
  "message": "How do I reset my password?",
  "customer_identifier": "customer@example.com",
  "customer_name": "John Doe"
}
```

#### Add Knowledge
```bash
POST /api/knowledge/add
{
  "title": "Password Reset Guide",
  "content": "Steps to reset password...",
  "category": "account",
  "tags": ["password", "security"],
  "is_temporary": false,
  "expires_in_days": null
}
```

#### Upload Knowledge File 🆕
```bash
POST /api/knowledge/upload
# Upload PDF, DOCX, or TXT file
# Automatically extracts content and adds to knowledge base
```

#### List All Knowledge 🆕
```bash
GET /api/knowledge/list?category=security&limit=50
```

#### Update Knowledge 🆕
```bash
PUT /api/knowledge/{doc_id}
```

#### Delete Knowledge 🆕
```bash
DELETE /api/knowledge/{doc_id}?hard_delete=false
```

#### Get Ticket
```bash
GET /api/tickets/{ticket_id}
```

#### List Tickets
```bash
GET /api/tickets?status=open&limit=50
```

#### Update Ticket Status
```bash
PUT /api/tickets/{ticket_id}/status?status=resolved
```

#### System Statistics
```bash
GET /api/stats
```

### Webhook Endpoints (Twilio)

#### SMS Webhook
```
POST /api/webhooks/sms
```

#### WhatsApp Webhook
```
POST /api/webhooks/whatsapp
```

## 🔧 Configuration

### Knowledge Base Setup

1. **Load IT Support Knowledge Base (MNC):** 🆕
```bash
python it_support_knowledge_mnc.py
# Adds 11 comprehensive IT support documents covering:
# - Hardware, Software, Network, Security
# - Email, Storage, Performance, Mobile
```

2. **Upload files via API:**
```bash
curl -X POST http://localhost:8000/api/knowledge/upload \
  -F "file=@IT_Manual.pdf" \
  -F "category=documentation" \
  -F "tags=manual,reference"
```

3. **Add documents via API:**
```python
import requests

response = requests.post('http://localhost:8000/api/knowledge/add', json={
    "title": "Product Setup Guide",
    "content": "Full setup instructions...",
    "category": "setup",
    "tags": ["installation", "configuration"],
    "is_temporary": False  # or True with expires_in_days
})
```

4. **Temporary Knowledge (TTL):** 🆕
```python
# Auto-expires after specified days
response = requests.post('http://localhost:8000/api/knowledge/add', json={
    "title": "Maintenance Window Notice",
    "content": "System down on Jan 20...",
    "category": "announcement",
    "is_temporary": True,
    "expires_in_days": 7  # Auto-deleted after 7 days
})
```

### Twilio Webhook Setup

For production, configure webhooks in Twilio Console:
- SMS: `https://your-domain.com/api/webhooks/sms`
- WhatsApp: `https://your-domain.com/api/webhooks/whatsapp`

For local development, use [ngrok](https://ngrok.com/):
```bash
ngrok http 8000
# Use the ngrok URL for webhooks
```

## 🧪 Testing

### Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are your business hours?",
    "customer_identifier": "test@example.com"
  }'
```

### Test Knowledge Base
```bash
# Add knowledge
curl -X POST http://localhost:8000/api/knowledge/add \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Business Hours",
    "content": "We are open Monday-Friday, 9 AM to 5 PM EST",
    "category": "general"
  }'

# Query it
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "When are you open?",
    "customer_identifier": "test@example.com"
  }'
```

## 📊 Monitoring

The system includes background tasks that:
- Check for new emails every 2 minutes
- Process incoming messages automatically
- **Clean up expired knowledge every hour** 🆕
- Clean up old tickets every 6 hours

View statistics:
```bash
curl http://localhost:8000/api/stats
```

## 🔒 Security Considerations

1. **Environment Variables**: Never commit `.env` file
2. **API Keys**: Use environment variables for all sensitive data
3. **CORS**: Update CORS settings in `app/api.py` for production
4. **Authentication**: Add API authentication for production use
5. **Rate Limiting**: Implement rate limiting for public endpoints

## 🏗️ Project Structure

```
intell-customer-support/
├── app/
│   ├── __init__.py
│   ├── api.py                    # FastAPI application and routes
│   ├── config.py                 # Configuration management
│   ├── database.py               # MongoDB models and operations
│   ├── rag_system.py             # RAG/Langchain implementation
│   ├── email_integration.py      # Email channel handler
│   ├── sms_integration.py        # SMS/Twilio handler
│   ├── whatsapp_integration.py   # WhatsApp handler
│   └── background_tasks.py       # Background monitoring tasks
├── knowledge_base/               # Knowledge documents
│   └── uploads/                  # Uploaded files (PDF, DOCX, TXT)
├── vector_store/                 # ChromaDB vector store
├── main.py                       # Application entry point
├── setup_sample_knowledge.py     # Sample knowledge loader
├── it_support_knowledge_mnc.py   # IT support knowledge (MNC) 🆕
├── test_system.py                # Test suite
├── pyproject.toml                # Python dependencies
├── README.md                     # This file
├── QUICK_START.md                # Quick start guide
├── ENV_SETUP.md                  # Environment setup guide
├── DEPLOYMENT_CHECKLIST.md       # Deployment guide
└── KNOWLEDGE_BASE_MANAGEMENT.md  # Knowledge base guide 🆕
```

## 🔮 Future Enhancements

- [ ] Voice call support
- [ ] Slack/Teams integration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Agent handoff workflows
- [ ] Custom model fine-tuning
- [ ] File attachment handling
- [ ] Conversation sentiment analysis

## 🤝 NextJS Frontend Application

A complete NextJS frontend is included in the `frontend/` directory!

### 🎯 Features
- **📚 Knowledge Base Management** - Upload, create, edit, delete knowledge documents
- **📧 Email Ticket Monitoring** - Real-time ticket tracking with auto-refresh
- **🔄 Auto-Refresh** - Tickets update every 10 seconds
- **📊 Interactive Tables** - Clean, responsive data display
- **🎨 Modern UI** - Tailwind CSS with simple, professional design

### 🚀 Quick Start

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Visit **http://localhost:3000**

### 📖 Pages

**1. Knowledge Base (`/knowledge-base`)**
- View all knowledge in table format
- Upload files (PDF, DOCX, TXT)
- Create knowledge manually
- Edit/Delete operations
- Filter by category

**2. Email Tickets (`/tickets`)**
- Real-time ticket monitoring
- Full conversation history
- Auto-refresh every 10 seconds
- Filter by status and channel
- View complete email trace

See [FRONTEND_SETUP_GUIDE.md](FRONTEND_SETUP_GUIDE.md) for complete documentation.

## 📝 License

MIT License - see LICENSE file for details

## 🐛 Troubleshooting

See [ENV_SETUP.md](ENV_SETUP.md) for detailed troubleshooting guide.

Common issues:
- **MongoDB Connection**: Ensure MongoDB is running on port 27017
- **Email Issues**: Use Gmail App Password, not regular password
- **Twilio Webhooks**: Use ngrok for local testing
- **OpenAI Errors**: Verify API key and billing status

## 📧 Support

For issues and questions:
1. Check [ENV_SETUP.md](ENV_SETUP.md)
2. Review API documentation at `/docs`
3. Open an issue on GitHub

---

Built with ❤️ using FastAPI, Langchain, and OpenAI

