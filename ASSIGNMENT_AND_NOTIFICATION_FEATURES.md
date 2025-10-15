# Assignment and Notification Features

## Overview

This document describes the new **ticket assignment** and **notification system** features that enable manual handling of low-confidence AI responses.

## Features Implemented

### 1. 📋 Enhanced Ticket Model

**Backend Changes (`app/database.py`)**

New fields added to `SupportTicket`:
```python
requires_human: bool = False           # Flag for low-confidence tickets
assigned_to: Optional[str] = None      # Email/ID of assigned agent
assigned_at: Optional[datetime] = None # When ticket was assigned
notification_sent: bool = False        # Track if notification was sent
notification_sent_at: Optional[datetime] = None
```

### 2. 🔔 Automatic Notification System

**How It Works:**

1. **Low Confidence Detection** - When AI confidence < 70%, ticket is flagged
2. **Visual Alerts** - Yellow banner shows unassigned tickets needing attention
3. **Real-time Updates** - Auto-refresh every 10 seconds shows pending tickets
4. **Assignment Tracking** - Once assigned, ticket is removed from notification queue

**Backend (`app/email_integration.py:186-194`)**
```python
if rag_response["can_auto_respond"]:
    # Auto-reply sent
    await db_manager.update_ticket(ticket_id, {
        "auto_resolved": True,
        "status": "pending"
    })
else:
    # Requires human attention
    await db_manager.update_ticket(ticket_id, {
        "status": "pending",
        "priority": "high",
        "requires_human": True  # ✅ Flagged for manual review
    })
```

### 3. 👤 Manual Assignment System

**Features:**

- **Assign tickets to specific agents** by email or name
- **Add assignment notes** for context
- **Track assignment history** in conversation
- **Filter by assignment status** (assigned/unassigned)

**Assignment Flow:**

```
1. Ticket requires human attention (confidence < 70%)
   ↓
2. Yellow notification banner appears
   ↓
3. Agent clicks "View & Assign"
   ↓
4. Ticket details modal shows assignment form
   ↓
5. Agent enters email/name and optional notes
   ↓
6. System creates assignment record
   ↓
7. Adds system message to conversation
   ↓
8. Ticket removed from unassigned queue
```

## API Endpoints

### Assignment Endpoints

#### 1. Assign Ticket to Agent
```http
POST /api/tickets/{ticket_id}/assign
Content-Type: application/json

{
  "ticket_id": "EMAIL-ABC123",
  "assigned_to": "agent@company.com",
  "notes": "Complex issue, needs senior agent"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Ticket assigned to agent@company.com",
  "ticket_id": "EMAIL-ABC123"
}
```

#### 2. Get Assigned Tickets for Agent
```http
GET /api/tickets/assigned/{agent_email}
```

**Response:**
```json
{
  "agent": "agent@company.com",
  "count": 5,
  "tickets": [
    {
      "ticket_id": "EMAIL-ABC123",
      "channel": "email",
      "customer_identifier": "customer@example.com",
      "subject": "Complex issue",
      "status": "pending",
      "priority": "high",
      "created_at": "2024-10-14T10:30:00",
      "assigned_at": "2024-10-14T11:00:00"
    }
  ]
}
```

#### 3. Get Unassigned Tickets
```http
GET /api/tickets/unassigned?requires_human_only=true
```

**Response:**
```json
{
  "count": 3,
  "tickets": [
    {
      "ticket_id": "EMAIL-DEF456",
      "channel": "email",
      "customer_identifier": "customer@example.com",
      "subject": "Help needed",
      "status": "pending",
      "priority": "high",
      "requires_human": true,
      "created_at": "2024-10-14T12:00:00",
      "conversation_count": 2
    }
  ]
}
```

### Notification Endpoints

#### 1. Get Pending Notifications
```http
GET /api/notifications/pending
```

**Response:**
```json
{
  "count": 2,
  "notifications": [
    {
      "ticket_id": "EMAIL-GHI789",
      "channel": "email",
      "customer_identifier": "customer@example.com",
      "subject": "Issue description",
      "priority": "high",
      "created_at": "2024-10-14T13:00:00",
      "last_message": "Customer's question...",
      "confidence": 0.45
    }
  ]
}
```

#### 2. Mark Notification as Sent
```http
POST /api/notifications/{ticket_id}/mark-sent
```

**Response:**
```json
{
  "status": "success",
  "message": "Notification marked as sent",
  "ticket_id": "EMAIL-GHI789"
}
```

## Frontend UI

### 1. Notification Banner

**Location:** Top of Tickets page  
**Visibility:** Shows when `unassignedCount > 0`

**Features:**
- 📊 Shows count of unassigned tickets requiring attention
- 🔘 "View & Assign" button - opens first unassigned ticket
- ❌ Dismiss button - hides banner (reappears on refresh if tickets exist)
- ⏰ Auto-updates every 10 seconds

### 2. Ticket Details Modal - Assignment Section

**Location:** Within ticket modal (when ticket is unassigned)

**UI Elements:**
```
⚠️ Requires Human Assignment
[Assign to Agent] button

↓ (expands on click)

Agent Email/Name: [text input]
Assignment Notes: [textarea - optional]

[Confirm Assignment] [Cancel]
```

**Visual States:**
- **Unassigned + requires_human** → Yellow alert box shown
- **Unassigned + doesn't require human** → Assignment option available
- **Already assigned** → Shows assignment info, no form

### 3. Ticket Table Visual Indicators

**Row Highlighting:**
- 🟨 **Yellow background** → Requires human, unassigned
- ⬜ **White background** → Normal ticket

**Ticket ID Column:**
- ⚠️ **Warning icon** → Requires human attention
- 🤖 **"Auto" badge** → Auto-resolved by AI
- 👤 **Agent badge** → Shows assigned agent name

### 4. Full Conversation Display

**Enhanced Ticket Details:**
- ✅ Complete conversation history with timestamps
- 🎯 Role indicators (Customer, AI Assistant, System)
- 📊 Confidence scores for AI responses
- 🏷️ Auto-generated flags
- 📝 Assignment system messages
- 🔍 Expandable metadata for each message

## Frontend API Integration

**New Functions in `frontend/lib/api.ts`:**

```typescript
// Assign ticket to agent
ticketsAPI.assign(ticketId, assignedTo, notes?)

// Get unassigned tickets
ticketsAPI.getUnassigned(requiresHumanOnly = true)

// Get assigned tickets for agent
ticketsAPI.getAssigned(agentEmail)

// Get pending notifications
notificationsAPI.getPending()

// Mark notification as sent
notificationsAPI.markSent(ticketId)
```

## Usage Examples

### Example 1: Agent Reviews Unassigned Tickets

1. **Agent logs into system**
   - Sees yellow banner: "3 Tickets Require Human Attention"

2. **Click "View & Assign"**
   - First unassigned ticket opens in modal
   - Full conversation visible
   - AI response shows low confidence (45%)

3. **Assign ticket**
   - Click "Assign to Agent"
   - Enter: "john.smith@company.com"
   - Add note: "Escalate to billing department"
   - Click "Confirm Assignment"

4. **Result**
   - Ticket assigned to john.smith@company.com
   - System message added: "Ticket assigned to john.smith@company.com. Notes: Escalate to billing department"
   - Removed from unassigned queue
   - Banner updates: "2 Tickets Require Human Attention"

### Example 2: Automatic Email Processing

1. **Customer sends email**
   ```
   From: confused.customer@example.com
   Subject: How do I...?
   Body: I need help with something but I'm not sure what
   ```

2. **AI processes email**
   - Searches knowledge base
   - Finds 1 partially relevant document
   - Confidence: 35% (below 70% threshold)

3. **System response**
   - ❌ No auto-reply sent
   - ✅ Ticket created with `requires_human: true`
   - ✅ Notification appears on dashboard
   - ✅ Ticket highlighted in yellow

4. **Agent intervenes**
   - Sees notification
   - Views full conversation
   - Manually responds to customer
   - Assigns ticket to self

## Testing the Features

### Test Case 1: Low Confidence Email

```bash
# Send email with vague content
To: your-support@company.com
Subject: Help
Body: I need assistance
```

**Expected:**
1. Email received and processed
2. Low confidence detected (no matching KB)
3. Ticket created with `requires_human: true`
4. No auto-reply sent
5. Notification banner appears: "1 Ticket Requires Human Attention"
6. Ticket row highlighted in yellow with ⚠️ icon

### Test Case 2: Manual Assignment

```bash
# API test
curl -X POST http://localhost:8000/api/tickets/EMAIL-ABC123/assign \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "EMAIL-ABC123",
    "assigned_to": "support@company.com",
    "notes": "Customer needs account verification"
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Ticket assigned to support@company.com",
  "ticket_id": "EMAIL-ABC123"
}
```

**UI Changes:**
- Ticket row shows 👤 support badge
- Yellow background removed
- Assignment info visible in ticket details
- Conversation includes system message about assignment

### Test Case 3: Get Unassigned Tickets

```bash
curl http://localhost:8000/api/tickets/unassigned?requires_human_only=true
```

**Expected:**
- List of all tickets with `requires_human: true` and `assigned_to: null`
- Count matches notification banner number
- Each ticket includes conversation count

## Benefits

### For Support Agents

✅ **Clear visibility** of tickets needing attention  
✅ **Prioritized workflow** - high-priority tickets highlighted  
✅ **Context preservation** - full conversation history  
✅ **Flexible assignment** - assign to self or team members  
✅ **Audit trail** - track who handled what

### For Managers

✅ **Performance tracking** - see assignment patterns  
✅ **Workload distribution** - monitor agent assignments  
✅ **Quality assurance** - review low-confidence cases  
✅ **System improvement** - identify knowledge gaps

### For System Efficiency

✅ **Hybrid approach** - AI handles high confidence, humans handle edge cases  
✅ **Continuous improvement** - low-confidence cases help identify KB gaps  
✅ **Scalability** - system handles volume, humans add quality  
✅ **Customer satisfaction** - complex issues get human attention

## Configuration

### Confidence Threshold

Adjust in `app/rag_system.py:364`:

```python
# Current: 70% threshold
"can_auto_respond": confidence > 0.7

# More conservative (90%)
"can_auto_respond": confidence > 0.9

# More aggressive (50%)
"can_auto_respond": confidence > 0.5
```

### Notification Refresh Interval

Adjust in `frontend/app/tickets/page.tsx:52`:

```typescript
// Current: 10 seconds
const interval = setInterval(() => {
  loadTickets()
}, 10000)

// Faster: 5 seconds
}, 5000)

// Slower: 30 seconds
}, 30000)
```

## Next Steps

Future enhancements could include:

1. **Email notifications** - Send alerts to agents when assigned
2. **Slack integration** - Post to Slack channel for urgent tickets  
3. **SLA tracking** - Monitor response times for assigned tickets
4. **Agent availability** - Check agent status before assignment
5. **Smart routing** - Auto-assign based on agent expertise
6. **Escalation rules** - Auto-escalate if unassigned for X hours
7. **Analytics dashboard** - Visualize assignment patterns

## Summary

The system now provides a complete workflow for:

1. ✅ **Automatic detection** of low-confidence AI responses
2. ✅ **Real-time notifications** of tickets needing attention
3. ✅ **Manual assignment** to specific support agents
4. ✅ **Full conversation tracking** for context
5. ✅ **Visual indicators** for ticket status and priority
6. ✅ **API support** for all assignment operations

This creates a **hybrid AI-human support system** where AI handles routine queries and humans step in for complex cases, ensuring high-quality customer support at scale.

