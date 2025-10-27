# Intelligent Customer Support System - Code Documentation

## Overview

This documentation covers all Python modules in the `app/` folder, including configuration points for monitoring intervals and channel enable/disable settings.

---

## Core Modules

### 1. `api.py` - REST API Endpoints
**Purpose**: FastAPI application with all HTTP endpoints for the customer support system.

**Key Endpoints**:
- `GET /api/agents/list` - List all agents
- `GET /api/agents/{agent_id}` - Get agent details
- `POST /api/agents` - Create new agent
- `GET /api/tickets/list` - List all tickets
- `GET /api/tickets/{ticket_id}` - Get ticket details
- `POST /api/tickets/{ticket_id}/update-status` - Update ticket status
- `POST /api/tickets/{ticket_id}/reassign` - Reassign ticket to agent
- `POST /api/knowledge/add` - Add knowledge document
- `GET /api/knowledge/list` - List knowledge documents
- `GET /api/config` - Get system configuration
- `PUT /api/config` - Update system configuration
- `POST /api/whatsapp/check-messages` - Check WhatsApp messages on-demand

**Configuration Points**:
- No background monitoring times in this file
- All channel enable/disable controlled via `/api/config` endpoint

---

### 2. `background_tasks.py` - ⏰ Background Monitoring Tasks
**Purpose**: Manages periodic background tasks for monitoring channels and system maintenance.

**🔧 CONFIGURATION - Background Task Monitoring Times**:

```python
# Lines 124-140: Email Monitoring
self.scheduler.add_job(
    self.check_emails_task,
    trigger=IntervalTrigger(minutes=2),  # ← CHANGE HERE for email frequency
    ...
)

# Lines 134-140: WhatsApp Monitoring  
self.scheduler.add_job(
    self.check_whatsapp_task,
    trigger=IntervalTrigger(minutes=2),  # ← CHANGE HERE for WhatsApp frequency
    ...
)

# Lines 161-167: SLA Monitoring & Escalation
self.scheduler.add_job(
    self.sla_monitoring_task,
    trigger=IntervalTrigger(minutes=5),  # ← CHANGE HERE for SLA check frequency
    ...
)

# Lines 152-158: Expired Knowledge Cleanup
self.scheduler.add_job(
    self.cleanup_expired_knowledge_task,
    trigger=IntervalTrigger(hours=1),  # ← CHANGE HERE for cleanup frequency
    ...
)

# Lines 143-149: General Cleanup
self.scheduler.add_job(
    self.cleanup_old_tickets_task,
    trigger=IntervalTrigger(hours=6),  # ← CHANGE HERE for cleanup frequency
    ...
)
```

**Current Monitoring Schedule**:
- Email checking: **Every 2 minutes**
- WhatsApp checking: **Every 2 minutes**
- SLA monitoring & escalation: **Every 5 minutes**
- Expired knowledge cleanup: **Every hour**
- General cleanup: **Every 6 hours**

---

### 3. `config.py` - System Configuration
**Purpose**: Centralized configuration management using Pydantic Settings.

**Key Settings**:
- `mongodb_url`: MongoDB connection string
- `openai_api_key`: OpenAI API key for LLM
- `email_host`, `email_port`: Email server settings
- `twilio_account_sid`, `twilio_auth_token`: Twilio credentials
- `support_email`: Default support email

---

### 4. `database.py` - Database Models and Manager
**Purpose**: MongoDB database operations and data models.

**Key Models**:
- `SupportTicket`: Ticket data model
- `KnowledgeDocument`: Knowledge base document model
- `Agent`: Support agent model
- `SystemConfiguration`: System configuration model

**Key Methods**:
- `create_ticket()` - Create new ticket
- `get_ticket()` - Get ticket by ID
- `update_ticket()` - Update ticket
- `get_all_knowledge_documents()` - Get all KB documents
- `get_system_config()` - Get system configuration
- `update_system_config()` - Update system configuration

---

### 5. `rag_system.py` - RAG (Retrieval Augmented Generation) System
**Purpose**: Knowledge base querying and AI-powered responses.

**Key Methods**:
- `query(question, conversation_history, domain)` - Query knowledge base
- `add_documents_to_knowledge_base()` - Add documents
- `initialize()` - Initialize vector store

**Configuration Points**:
```python
# Line 97: Number of documents to retrieve
search_kwargs={"k": 10}  # ← INCREASE for more context, DECREASE for faster queries

# Line 430: Confidence threshold for auto-response
"can_auto_respond": confidence > 0.4  # ← LOWER (0.3) for more responses, HIGHER (0.7) for stricter

# Lines 469-470: Base confidence calculation
base_confidence = 0.5 + (len(source_documents) - 1) * 0.1  # ← ADJUST for confidence scaling
```

---

### 6. `email_integration.py` - Email Channel Integration
**Purpose**: Email receiving, processing, and sending.

**Key Methods**:
- `check_new_emails(since_minutes)` - Check for new emails
- `process_email(email_data)` - Process incoming email
- `send_email(to_email, subject, body)` - Send email response

**Enable/Disable Email**:
```python
# To disable email processing, modify check_emails_task() in background_tasks.py:
# Lines 19-33 in background_tasks.py
# Comment out this block:
# self.scheduler.add_job(
#     self.check_emails_task,
#     trigger=IntervalTrigger(minutes=2),
#     ...
# )
```

---

### 7. `whatsapp_integration.py` - WhatsApp Channel Integration
**Purpose**: WhatsApp message receiving and sending via Twilio.

**Key Methods**:
- `check_new_whatsapp_messages()` - Check for new messages
- `process_incoming_whatsapp()` - Process incoming message
- `send_whatsapp_message()` - Send WhatsApp message
- `get_processed_message_sids()` - Get processed message IDs

**🔧 Enable/Disable WhatsApp**:

**Method 1: Via System Configuration** (Recommended)
```python
# Update system config through API: PUT /api/config
# Set whatsapp_enabled = False
```

**Method 2: Via Code**
```python
# File: app/whatsapp_integration.py
# Lines 20-36: _init_from_settings() method

def _init_from_settings(self):
    if settings.twilio_account_sid and settings.twilio_auth_token:
        self.enabled = True  # ← CHANGE TO False TO DISABLE
    else:
        self.enabled = False
```

**Method 3: Via Background Tasks**
```python
# File: app/background_tasks.py
# Lines 134-140: Comment out WhatsApp monitoring
# self.scheduler.add_job(
#     self.check_whatsapp_task,
#     ...
# )
```

---

### 8. `sms_integration.py` - SMS Channel Integration
**Purpose**: SMS message handling via Twilio.

**Enable/Disable SMS**:
```python
# Similar to WhatsApp - controlled via configuration
# Set sms_enabled = False in system configuration
```

---

### 9. `auto_assignment.py` - Automatic Ticket Assignment
**Purpose**: Automatic ticket assignment to agents based on skills and availability.

**Key Methods**:
- `auto_assign_ticket()` - Assign ticket to best agent
- `get_team_stats()` - Get team statistics
- `find_best_agent()` - Find best matching agent

**Configuration Points**:
```python
# Line 109: Agent availability check
if not agent.is_active or agent.current_load >= agent.max_concurrent_tickets:
    # Line 125: Skill matching score
    skill_score = len(matched_skills) / len(required_skills)
    
    # Line 140: Load balancing weight
    load_weight = 0.3  # ← ADJUST to prioritize skills (lower) or availability (higher)
```

---

### 10. `skill_mapper.py` - Skill Extraction and Mapping
**Purpose**: Extract skills from customer messages using NLP.

**Key Methods**:
- `extract_skills(text, domain)` - Extract skills from text
- `map_ticket_to_agent_skills()` - Map ticket to agent skills

---

### 11. `escalation_system.py` - SLA Monitoring and Escalation
**Purpose**: Monitor ticket SLAs and escalate when needed.

**Key Methods**:
- `check_and_escalate_tickets()` - Check SLAs and escalate
- `get_ticket_age_minutes()` - Calculate ticket age
- `escalate_ticket()` - Escalate ticket to next tier

**Configuration Points**:
```python
# Check SLA monitoring frequency in background_tasks.py:
# Lines 161-167: Currently every 5 minutes
trigger=IntervalTrigger(minutes=5)  # ← CHANGE HERE
```

---

### 12. `notification_handler.py` - Customer Notifications
**Purpose**: Send notifications to customers across all channels.

**Key Methods**:
- `send_channel_notification()` - Send notification to customer
- `notify_human_agent_required()` - Notify when human agent required
- `_send_email_notification()` - Send email notification
- `_send_sms_notification()` - Send SMS notification
- `_send_whatsapp_notification()` - Send WhatsApp notification

---

## 📋 Quick Reference: Enable/Disable Channels

### Enable/Disable WhatsApp
1. **Via API** (Recommended): `PUT /api/config` with `whatsapp_enabled: false`
2. **Via Code**: Modify `app/whatsapp_integration.py` line 29: `self.enabled = False`
3. **Via Background Tasks**: Comment out lines 134-140 in `background_tasks.py`

### Enable/Disable Email
- Comment out lines 125-131 in `background_tasks.py`
- Or remove Twilio credentials from `.env`

### Enable/Disable SMS
- Set `sms_enabled = False` in system configuration
- Or remove SMS credentials from `.env`

---

## 🔧 Configuration Changes Summary

### To Change Monitoring Frequency:
1. Open `app/background_tasks.py`
2. Find the relevant task scheduling block
3. Modify `IntervalTrigger()` parameters:
   - `minutes=X` for every X minutes
   - `hours=Y` for every Y hours
   - `seconds=Z` for every Z seconds

### To Enable/Disable Channels:
1. **WhatsApp**: Set `whatsapp_enabled` in system config via API
2. **Email**: Comment out email job in `background_tasks.py`
3. **SMS**: Set `sms_enabled` in system config via API

### To Adjust Auto-Response Confidence:
1. Open `app/rag_system.py`
2. Line 430: Change `confidence > 0.4` threshold
3. Lines 469-470: Adjust confidence calculation formula

---

## 📊 Current System Configuration

**Monitoring Intervals** (in `background_tasks.py`):
- Email checking: Every 2 minutes (Line 127)
- WhatsApp checking: Every 2 minutes (Line 136)
- SLA monitoring: Every 5 minutes (Line 163)
- Expired knowledge cleanup: Every 1 hour (Line 154)
- General cleanup: Every 6 hours (Line 145)

**Retrieval Settings** (in `rag_system.py`):
- Documents retrieved (k): 10 (Line 97)
- Confidence threshold: > 0.4 (40%) (Line 430)
- Base confidence: 0.5 + 0.1 per additional document (Lines 469-470)

**Channel Enable/Disable**:
- Email: Enabled by default (if credentials configured)
- WhatsApp: Controlled via `whatsapp_enabled` config flag
- SMS: Controlled via `sms_enabled` config flag

---

## 🛠️ Common Modifications

### Make WhatsApp Check Every 5 Minutes Instead of 2:
```python
# File: app/background_tasks.py, Line 136
trigger=IntervalTrigger(minutes=5)  # Changed from minutes=2
```

### Disable WhatsApp Permanently:
```python
# File: app/whatsapp_integration.py, Line 29
self.enabled = False  # Add this line
```

### Make System More Strict (Higher Confidence Required):
```python
# File: app/rag_system.py, Line 430
"can_auto_respond": confidence > 0.7  # Changed from 0.4
```

### Increase Retrieved Documents for Better Context:
```python
# File: app/rag_system.py, Line 97
search_kwargs={"k": 15}  # Changed from 10
```

---

## 📝 Notes

- All configuration changes require restarting the application
- Background tasks start automatically when the FastAPI app starts
- Channel credentials are loaded from `.env` file
- System configuration can be updated via API without code changes (preferred method)

