# Knowledge Base Management Guide

Complete guide for managing the intelligent knowledge base system with full CRUD operations, file uploads, temporary knowledge, and IT support content.

## 📚 Overview

The knowledge base system supports:
- ✅ **File Upload** - PDF, DOCX, TXT files
- ✅ **CRUD Operations** - Create, Read, Update, Delete documents
- ✅ **Temporary Knowledge** - TTL (Time-To-Live) support for temporary documents
- ✅ **Categories & Tags** - Organize knowledge
- ✅ **Version Control** - Track updates
- ✅ **Soft Delete** - Recovery option
- ✅ **Automatic Expiry** - Auto-deactivate expired documents
- ✅ **Vector Store** - Semantic search with embeddings
- ✅ **Multi-format Support** - PDF, DOCX, TXT

## 🚀 Quick Start

### 1. Add Knowledge via API

```bash
curl -X POST http://localhost:8000/api/knowledge/add \
  -H "Content-Type: application/json" \
  -d '{
    "title": "How to Reset Password",
    "content": "Step 1: Go to selfservice portal...",
    "category": "security",
    "tags": ["password", "reset", "account"],
    "is_temporary": false
  }'
```

### 2. Upload File

```bash
curl -X POST http://localhost:8000/api/knowledge/upload \
  -F "file=@IT_Manual.pdf" \
  -F "category=documentation" \
  -F "tags=manual,reference" \
  -F "is_temporary=false"
```

### 3. Load IT Support Knowledge

```bash
# Run the comprehensive IT support knowledge base loader
python it_support_knowledge_mnc.py
```

## 📋 API Endpoints

### Create Knowledge

**POST** `/api/knowledge/add`

```json
{
  "title": "VPN Setup Guide",
  "content": "Complete VPN setup instructions...",
  "category": "network",
  "tags": ["vpn", "remote", "access"],
  "source": "IT Department",
  "is_temporary": false,
  "expires_in_days": null,
  "created_by": "admin@company.com"
}
```

**Response:**
```json
{
  "status": "success",
  "document_ids": ["507f1f77bcf86cd799439011"],
  "message": "Document added to knowledge base",
  "is_temporary": false,
  "expires_in_days": null
}
```

### Upload File

**POST** `/api/knowledge/upload`

**Form Data:**
- `file`: File to upload (PDF, DOCX, TXT)
- `category`: Category name (default: "general")
- `tags`: Comma-separated tags
- `is_temporary`: Boolean (default: false)
- `expires_in_days`: Number (optional, for temporary knowledge)
- `created_by`: Email/username (optional)

**Example:**
```bash
curl -X POST http://localhost:8000/api/knowledge/upload \
  -F "file=@policy_document.pdf" \
  -F "category=policy" \
  -F "tags=hr,policy,confidential" \
  -F "is_temporary=true" \
  -F "expires_in_days=30" \
  -F "created_by=hr@company.com"
```

### List All Knowledge Documents

**GET** `/api/knowledge/list?category={category}&include_inactive={bool}&limit={number}`

**Query Parameters:**
- `category` (optional): Filter by category
- `include_inactive` (optional, default: false): Include soft-deleted documents
- `limit` (optional, default: 100): Maximum results

**Example:**
```bash
# List all active documents
curl http://localhost:8000/api/knowledge/list

# List documents in 'security' category
curl http://localhost:8000/api/knowledge/list?category=security

# List including inactive documents
curl http://localhost:8000/api/knowledge/list?include_inactive=true&limit=50
```

**Response:**
```json
{
  "status": "success",
  "count": 25,
  "documents": [
    {
      "id": "507f1f77bcf86cd799439011",
      "title": "Password Reset Guide",
      "category": "security",
      "tags": ["password", "reset"],
      "file_name": "password_reset.pdf",
      "file_type": "pdf",
      "is_active": true,
      "is_temporary": false,
      "expires_at": null,
      "created_by": "admin@company.com",
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00",
      "content_preview": "Step 1: Navigate to selfservice portal..."
    }
  ]
}
```

### Get Specific Document

**GET** `/api/knowledge/{doc_id}`

**Example:**
```bash
curl http://localhost:8000/api/knowledge/507f1f77bcf86cd799439011
```

**Response:**
```json
{
  "status": "success",
  "document": {
    "id": "507f1f77bcf86cd799439011",
    "title": "Password Reset Guide",
    "content": "Full content here...",
    "category": "security",
    "tags": ["password", "reset"],
    "file_name": "password_reset.pdf",
    "file_type": "pdf",
    "source": "/knowledge_base/uploads/abc123_password_reset.pdf",
    "is_active": true,
    "is_temporary": false,
    "expires_at": null,
    "created_by": "admin@company.com",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

### Update Document

**PUT** `/api/knowledge/{doc_id}`

```json
{
  "title": "Updated Password Reset Guide",
  "content": "Updated content...",
  "category": "security",
  "tags": ["password", "reset", "updated"]
}
```

**All fields are optional** - only include fields you want to update.

**Example:**
```bash
curl -X PUT http://localhost:8000/api/knowledge/507f1f77bcf86cd799439011 \
  -H "Content-Type: application/json" \
  -d '{"title": "New Title", "tags": ["updated", "new"]}'
```

**Note:** If you update content, the vector embeddings are automatically regenerated.

### Delete Document

**DELETE** `/api/knowledge/{doc_id}?hard_delete={bool}`

**Query Parameters:**
- `hard_delete` (optional, default: false): 
  - `false`: Soft delete (mark as inactive, can be recovered)
  - `true`: Permanent deletion

**Example:**
```bash
# Soft delete (recommended)
curl -X DELETE http://localhost:8000/api/knowledge/507f1f77bcf86cd799439011

# Hard delete (permanent)
curl -X DELETE "http://localhost:8000/api/knowledge/507f1f77bcf86cd799439011?hard_delete=true"
```

### List Categories

**GET** `/api/knowledge/categories/list`

**Response:**
```json
{
  "status": "success",
  "categories": [
    {"name": "hardware", "count": 15},
    {"name": "software", "count": 23},
    {"name": "security", "count": 18},
    {"name": "network", "count": 12}
  ]
}
```

## ⏰ Temporary Knowledge (TTL)

### Use Cases
- Emergency procedures (valid for incident duration)
- Temporary policy changes
- Event-specific information
- Time-limited offers or announcements
- Project-specific documentation

### Create Temporary Knowledge

```bash
curl -X POST http://localhost:8000/api/knowledge/add \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Emergency Maintenance Window",
    "content": "System will be down for maintenance on Jan 20...",
    "category": "announcement",
    "tags": ["emergency", "maintenance", "temporary"],
    "is_temporary": true,
    "expires_in_days": 7,
    "created_by": "ops@company.com"
  }'
```

### Automatic Expiry
- Background task runs **every hour**
- Checks for expired documents (`expires_at` < current time)
- Automatically soft-deletes expired documents
- Expired documents removed from vector store (no longer returned in searches)
- Can be recovered by IT if needed

### Manual Expiry Check
```python
# Run cleanup task manually
from app.background_tasks import background_tasks
import asyncio

asyncio.run(background_tasks.cleanup_expired_knowledge_task())
```

## 🏢 IT Support Knowledge Base for MNC

### Pre-built Categories

The system includes comprehensive IT support knowledge for traditional MNC companies:

1. **Hardware Support** (3 documents)
   - Desktop troubleshooting
   - Laptop battery issues
   - Printer problems

2. **Software Support** (1 document)
   - Microsoft Office 365 complete guide

3. **Network** (1 document)
   - VPN setup and troubleshooting

4. **Security** (2 documents)
   - Password reset procedures
   - Phishing identification and reporting

5. **Email** (1 document)
   - Outlook troubleshooting

6. **Storage** (1 document)
   - Network drive access

7. **Performance** (1 document)
   - Computer optimization

8. **Mobile** (1 document)
   - BYOD and mobile device management

### Load IT Support Knowledge

```bash
python it_support_knowledge_mnc.py
```

This adds **11 comprehensive documents** covering all major IT support scenarios in a traditional MNC environment.

### Sample Questions It Can Answer

- "My computer won't start, what should I do?"
- "How do I reset my password?"
- "I think I received a phishing email"
- "How do I connect to VPN?"
- "Outlook is running very slow"
- "Cannot access network drives"
- "How to set up email on iPhone?"
- "Laptop battery drains quickly"
- "Printer is offline, how to fix?"
- "How to report security incident?"

## 📊 Knowledge Base Structure

### Database Schema

```javascript
{
  "_id": ObjectId,
  "title": String,
  "content": String (full text),
  "category": String,
  "tags": [String],
  "source": String (file path or URL),
  "file_name": String (original filename),
  "file_type": String (pdf, docx, txt),
  "chunk_ids": [String] (references to vector store),
  "is_active": Boolean,
  "is_temporary": Boolean,
  "expires_at": DateTime (null if not temporary),
  "created_by": String,
  "created_at": DateTime,
  "updated_at": DateTime,
  "metadata": Object
}
```

### Vector Store

- **Engine**: ChromaDB
- **Embeddings**: OpenAI text-embedding-3-small
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters
- **Persistence**: Local storage in `./vector_store/`

### How It Works

1. **Document Upload/Creation**:
   - Content extracted from file or provided directly
   - Split into chunks (1000 chars with 200 overlap)
   - Each chunk embedded using OpenAI embeddings
   - Chunks stored in ChromaDB with metadata
   - Document metadata stored in MongoDB

2. **Search/Retrieval**:
   - User question embedded
   - Top 5 similar chunks retrieved from ChromaDB
   - Chunks sent to GPT-4 with context
   - Answer generated with confidence score

3. **Update**:
   - Old chunks deleted from vector store
   - New content chunked and embedded
   - MongoDB document updated
   - Vector store persisted

4. **Delete**:
   - Soft delete: Mark as inactive (default)
   - Hard delete: Remove from MongoDB and vector store
   - Chunks removed from ChromaDB

## 🔧 Configuration

### Environment Variables

```env
# Knowledge Base Settings
KNOWLEDGE_BASE_PATH=./knowledge_base
VECTOR_STORE_PATH=./vector_store
EMBEDDINGS_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4-turbo-preview
```

### Upload Limits

- **File Size**: Depends on your server configuration
- **File Types**: `.pdf`, `.docx`, `.txt`
- **Path Length**: Maximum 400 characters
- **Content Size**: No hard limit (vector store auto-chunks)

### Storage Locations

```
project_root/
├── knowledge_base/
│   ├── uploads/          # Uploaded files stored here
│   └── documents/        # Manual documents (optional)
└── vector_store/         # ChromaDB persistence
    ├── chroma.sqlite3
    └── [embedding data]
```

## 🎯 Best Practices

### 1. Organizing Knowledge

```
Category Structure (Recommended):
├── hardware (physical issues)
├── software (applications)
├── network (connectivity)
├── security (passwords, threats)
├── email (Outlook, communication)
├── storage (files, drives)
├── performance (optimization)
├── mobile (BYOD, devices)
├── policy (company policies)
└── documentation (manuals, guides)
```

### 2. Tagging Strategy

- Use 3-7 tags per document
- Include specific and general tags
- Examples:
  - Specific: "vpn-cisco", "outlook-2021"
  - General: "network", "email"
  - Action: "troubleshooting", "setup"

### 3. Content Quality

✅ **Good Knowledge Content**:
- Step-by-step instructions
- Screenshots or diagrams (describe in text)
- Common errors and solutions
- Prerequisites listed
- Contact information for escalation
- Last updated date in content

❌ **Avoid**:
- Vague instructions
- Outdated information
- Missing context
- No error handling
- Dead links

### 4. Temporary Knowledge

Use for:
- ✅ Emergency announcements (1-7 days)
- ✅ Scheduled maintenance info (1-3 days)
- ✅ Temporary policy changes (30-90 days)
- ✅ Event-specific guides (7-30 days)

Don't use for:
- ❌ Permanent policies
- ❌ Standard procedures
- ❌ Long-term reference material

### 5. Updating vs. Creating New

**Update existing** when:
- Fixing errors or typos
- Adding new steps to existing process
- Updating version numbers
- Clarifying instructions

**Create new** when:
- Completely different topic
- New product/service
- Alternative procedure
- Different audience/use case

## 🔍 Search and Retrieval

### How RAG Works

1. **User asks question**: "How do I reset my password?"
2. **Question is embedded**: Vector representation created
3. **Similarity search**: Top 5 relevant chunks retrieved
4. **Context building**: Chunks combined with question
5. **LLM generation**: GPT-4 generates answer using context
6. **Confidence scoring**: Based on relevance of chunks
7. **Auto-response decision**: If confidence > 70%, auto-respond

### Confidence Scores

- **0.8-1.0**: High confidence - auto-respond
- **0.5-0.79**: Medium confidence - auto-respond with disclaimer
- **< 0.5**: Low confidence - escalate to human

## 📈 Monitoring

### Check Knowledge Base Status

```bash
# List all documents
curl http://localhost:8000/api/knowledge/list

# Get statistics
curl http://localhost:8000/api/stats

# List categories
curl http://localhost:8000/api/knowledge/categories/list
```

### Background Tasks

Monitor background task logs:
```
[10:30:00] Checking for expired knowledge...
  No expired documents found

[10:31:00] Checking for new emails...
  No new emails
```

### Database Queries

```javascript
// MongoDB shell
use customer_support

// Count documents by category
db.knowledge.aggregate([
  { $group: { _id: "$category", count: { $sum: 1 } } }
])

// Find temporary documents
db.knowledge.find({ is_temporary: true })

// Find expired documents
db.knowledge.find({
  is_temporary: true,
  expires_at: { $lte: new Date() }
})
```

## 🛠️ Maintenance

### Regular Tasks

**Daily**:
- Monitor system logs
- Check for failed uploads
- Review low-confidence queries

**Weekly**:
- Review and update outdated content
- Add new FAQs based on support tickets
- Clean up test documents

**Monthly**:
- Audit knowledge base completeness
- Update categories and tags
- Review auto-response accuracy
- Backup vector store and database

### Backup

```bash
# Backup MongoDB
mongodump --db customer_support --out ./backups/

# Backup vector store
cp -r ./vector_store ./backups/vector_store_$(date +%Y%m%d)

# Backup uploaded files
cp -r ./knowledge_base/uploads ./backups/uploads_$(date +%Y%m%d)
```

### Restore

```bash
# Restore MongoDB
mongorestore --db customer_support ./backups/customer_support/

# Restore vector store
cp -r ./backups/vector_store_20240115 ./vector_store/

# Restart application to reload
```

## 🔐 Security Considerations

### Access Control

- All API endpoints should be protected with authentication (add in production)
- Implement role-based access:
  - **Admin**: Full CRUD operations
  - **Editor**: Create, Read, Update
  - **Viewer**: Read only
  - **User**: Search only (through chat interface)

### Sensitive Information

- Don't store passwords or credentials in knowledge base
- Mark sensitive documents with appropriate tags
- Implement access logging
- Regular security audits

### File Upload Security

- File type validation (PDF, DOCX, TXT only)
- File size limits
- Virus scanning (add antivirus integration)
- Sanitize file names
- Isolated storage location

## 🚀 Advanced Usage

### Bulk Upload

```python
import requests
import glob

API_URL = "http://localhost:8000"

# Upload all PDFs in a directory
for pdf_file in glob.glob("./docs/*.pdf"):
    with open(pdf_file, 'rb') as f:
        response = requests.post(
            f"{API_URL}/api/knowledge/upload",
            files={"file": f},
            data={
                "category": "documentation",
                "tags": "manual,reference",
                "created_by": "admin@company.com"
            }
        )
        print(f"Uploaded {pdf_file}: {response.json()}")
```

### Custom Categories

```python
# Add knowledge with custom category
categories = {
    "onboarding": "New employee guides",
    "compliance": "Regulatory compliance docs",
    "training": "Training materials",
    "procedures": "Standard operating procedures"
}

for category, description in categories.items():
    # Create category document
    requests.post(f"{API_URL}/api/knowledge/add", json={
        "title": f"{category.title()} - Overview",
        "content": description,
        "category": category,
        "tags": [category, "overview"]
    })
```

### Integration with Ticket System

```python
# Automatically suggest knowledge based on ticket
async def suggest_knowledge_for_ticket(ticket_id):
    ticket = await db_manager.get_ticket(ticket_id)
    
    # Get last user message
    user_messages = [msg for msg in ticket.conversation if msg.role == "user"]
    if user_messages:
        last_message = user_messages[-1].content
        
        # Search knowledge
        similar_docs = await rag_system.get_similar_documents(last_message, k=3)
        
        # Return suggestions
        return [
            {
                "title": doc["metadata"]["title"],
                "relevance": doc["similarity_score"]
            }
            for doc in similar_docs
        ]
```

## 📞 Support

For issues or questions:
- **API Issues**: Check `/docs` for interactive API documentation
- **Upload Failures**: Check file format and size
- **Search Not Working**: Rebuild vector store index
- **IT Support Content**: See `it_support_knowledge_mnc.py`

## 📝 Change Log

### Version 1.0
- Initial knowledge base system
- CRUD operations
- File upload support
- Temporary knowledge with TTL
- IT support knowledge base
- Automatic expiry cleanup
- Soft delete functionality
- Vector store integration

---

**Ready to manage your intelligent knowledge base! 🎓**

