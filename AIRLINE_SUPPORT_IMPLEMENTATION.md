# Airline Customer Support Implementation Guide

## 🎯 Overview

The system now supports **BOTH IT and Airline customer support** with advanced SLA management, escalation workflows, and domain-specific knowledge bases.

---

## ✅ Completed Features

### 1. SLA (Service Level Agreement) Management ✅

**Database Fields Added:**
- `sla_response_time_minutes`: Expected first response time
- `sla_resolution_time_minutes`: Expected resolution time
- `first_response_at`: When first response sent
- `sla_response_breached`: Response SLA breach flag
- `sla_resolution_breached`: Resolution SLA breach flag
- `sla_response_deadline`: Calculated response deadline
- `sla_resolution_deadline`: Calculated resolution deadline

**SLA Matrix (by Priority):**
```
Priority | Response Time | Resolution Time
---------|---------------|----------------
Urgent   | 15 minutes    | 1 hour
High     | 30 minutes    | 2 hours
Medium   | 60 minutes    | 4 hours
Low      | 120 minutes   | 8 hours
```

**Auto-calculation:**
- SLA deadlines calculated automatically on ticket creation
- Based on ticket priority
- Tracked in background task

### 2. Automatic Escalation System ✅

**Escalation Triggers:**
- Response SLA breach (no response within deadline)
- Resolution SLA breach (not resolved within deadline)
- Runs every 5 minutes via background task

**Escalation Workflow:**
1. Detect SLA breach
2. Extract ticket skills/requirements
3. Find higher-tier agent with matching skills
4. Transfer ticket to higher-tier agent
5. Update escalation history
6. Increment escalation level

**Escalation Levels:**
- L0: Initial assignment
- L1: First escalation
- L2: Second escalation
- L3+: Critical escalation

**Features:**
- Auto-upgrades priority (high → urgent)
- Tracks escalation history
- Decrements load from previous agent
- Increments load for new agent

### 3. Agent Tier System ✅

**Agent Tiers:**
- **Tier 0**: L1/Junior agents (initial assignments)
- **Tier 1**: L2/Senior agents (handles first escalations)
- **Tier 2**: L3/Expert agents (handles complex issues)
- **Tier 3**: L4/Manager level (final escalation)

**Database Fields:**
- `tier`: Agent tier level (0-3)
- `handles_escalations`: Can handle escalated tickets
- `domain`: IT or AIRLINE support domain

**Escalation Logic:**
- Finds agents with `tier > current_tier`
- Matches skills and domain
- Considers current workload
- Prioritizes lowest available tier first

### 4. Support Domain Separation ✅

**Dual Domain Support:**
- **IT Support**: Traditional IT helpdesk
- **Airline Support**: Airline customer service

**Database Models Updated:**
- `SupportTicket.support_domain`: "IT" or "AIRLINE"
- `Agent.domain`: "IT" or "AIRLINE"
- `KnowledgeDocument.domain`: "IT" or "AIRLINE"

**Airline-Specific Fields:**
- `booking_reference`: PNR/booking number
- `flight_number`: Flight identifier
- Links tickets to bookings

### 5. Booking Management System ✅

**Booking Model:**
```python
class Booking:
    booking_reference: str  # PNR (unique)
    customer_email: str
    customer_name: str
    flight_number: str
    origin: str  # Airport code
    destination: str  # Airport code
    departure_date: datetime
    arrival_date: datetime
    booking_class: str  # economy/business/first
    seat_number: str
    ticket_price: float
    booking_status: str  # confirmed/cancelled/pending
    payment_status: str  # paid/pending/refunded
    passengers: List[Dict]
    special_requests: str
```

**Database Operations:**
- `create_booking()`
- `get_booking(booking_reference)`
- `get_bookings_by_customer(email)`
- `update_booking()`

### 6. Flight Route Management ✅

**FlightRoute Model:**
```python
class FlightRoute:
    flight_number: str  # e.g., "AA123"
    airline: str
    origin: str  # Airport code
    destination: str  # Airport code
    departure_time: str
    arrival_time: str
    duration_minutes: int
    aircraft_type: str
    days_of_operation: List[str]
    is_active: bool
```

**Database Operations:**
- `create_flight_route()`
- `get_flight_route(flight_number)`
- `search_flights(origin, destination)`

### 7. Priority-Based Knowledge Retrieval ✅ (Partial)

**Priority Levels:**
- **1**: Normal knowledge (permanent)
- **2**: High priority (temporary important updates)
- **3**: Critical (urgent temporary knowledge)

**How It Works:**
- Higher priority KB documents get precedence
- Temporary high-priority knowledge overrides older permanent knowledge
- Useful for urgent policy changes, alerts, notices

**Use Cases:**
- Flight cancellations due to weather
- Emergency policy updates
- Special promotions/exceptions
- Critical alerts

### 8. Comprehensive Airline Knowledge Base ✅

**10 Knowledge Documents Created:**

1. **Flight Cancellation Policy**
   - 24-hour free cancellation
   - Cancellation fees by class and timing
   - Refund processing

2. **Ticket Refund Process**
   - Online/phone refund requests
   - Refund timelines
   - Non-refundable ticket options
   - Travel credits

3. **Flight Change and Modification**
   - Change fees by class
   - Date/time/route changes
   - Name corrections
   - Elite member benefits

4. **Baggage Policy and Fees**
   - Carry-on allowances
   - Checked baggage fees
   - Special items
   - Lost/damaged baggage

5. **Check-in and Boarding Process**
   - Online/airport check-in
   - Check-in deadlines
   - Boarding zones
   - Travel documents

6. **Seat Selection and Upgrades**
   - Seat types and fees
   - Upgrade options
   - Bidding system
   - Elite member perks

7. **Flight Delays and Compensation**
   - Delay compensation tiers
   - Passenger rights
   - Denied boarding compensation
   - Claims process

8. **Loyalty Program - SkyMiles**
   - Membership tiers
   - Earning/redeeming miles
   - Elite benefits
   - Family pooling

9. **Special Assistance and Accessibility**
   - Wheelchair services
   - Medical equipment
   - Service animals
   - Unaccompanied minors

10. **International Travel Requirements**
    - Passport/visa requirements
    - Health requirements
    - Customs/immigration
    - Travel insurance

**Loading Script:**
```bash
python airline_knowledge_base.py
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Customer Support System                  │
├──────────────────────┬──────────────────────────────────┤
│    IT Support        │      Airline Support             │
├──────────────────────┼──────────────────────────────────┤
│ - Hardware/Software  │ - Bookings/Cancellations         │
│ - Network/Security   │ - Flight Changes                 │
│ - Accounts/Email     │ - Baggage Issues                 │
│ - Password Resets    │ - Delays/Compensation            │
└──────────────────────┴──────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              RAG System (Domain-Aware)                   │
│  - IT Knowledge Base (11 docs)                          │
│  - Airline Knowledge Base (10 docs)                     │
│  - Priority-based retrieval                             │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│            SLA Management & Escalation                   │
│  - Monitor response/resolution times                     │
│  - Auto-escalate on SLA breach                          │
│  - Tier-based agent routing                             │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Agent Assignment System                     │
│  - Skill-based routing                                  │
│  - Load balancing                                       │
│  - Domain filtering (IT vs Airline)                     │
│  - Tier-based escalation                                │
└─────────────────────────────────────────────────────────┘
```

---

## 🚧 Remaining Tasks

### Backend (In Progress):

1. **Priority-Based RAG Retrieval** 🔄
   - Update `rag_system.py` to consider priority field
   - Filter by domain in queries
   - Boost high-priority documents in results

2. **API Endpoints** 🔄
   - Booking CRUD APIs
   - Flight search APIs
   - SLA dashboard API
   - Escalation history API
   - Domain-specific ticket APIs

3. **Sample Data Scripts** ⏳
   - Create sample bookings
   - Create sample flights
   - Create airline agents with tiers

### Frontend (Pending):

1. **Domain Switcher** ⏳
   - UI toggle between IT and Airline mode
   - Different navigation for each domain
   - Domain-specific branding

2. **Airline Pages** ⏳
   - Bookings management page
   - Flight search page
   - My Trips page
   - Refund requests page

3. **SLA Dashboard** ⏳
   - Response time metrics
   - Resolution time metrics
   - SLA compliance rates
   - Escalation statistics

4. **Enhanced Ticket View** ⏳
   - Show SLA deadlines
   - Display escalation history
   - Show booking/flight info
   - Priority indicators

---

## 🚀 Quick Start

### 1. Load Airline Knowledge Base

```bash
# Load airline policies and procedures
python airline_knowledge_base.py
```

### 2. Create Airline Agents

```bash
# Create agents with airline skills and tiers
python setup_airline_agents.py  # (to be created)
```

### 3. Create Sample Bookings

```bash
# Create sample flight bookings
python create_sample_bookings.py  # (to be created)
```

### 4. Test Airline Support

Send test email with:
```
Subject: Need to cancel my flight
Body: I need to cancel my booking AA123456. Can I get a refund?
```

Expected behavior:
- RAG searches AIRLINE knowledge base
- Finds cancellation policy
- Auto-responds with refund options
- If complex, assigns to airline agent

---

## 📝 Usage Examples

### Scenario 1: Automatic Response (High Confidence)

**Customer Email:**
```
Subject: How do I check in online?
Body: I have a flight tomorrow. How can I check in online?
```

**System Response:**
1. Searches airline knowledge base
2. Finds "Check-in and Boarding Process"
3. Confidence: 0.92 (high)
4. Auto-responds with online check-in instructions
5. No agent assignment needed

### Scenario 2: Agent Assignment (Low Confidence)

**Customer Email:**
```
Subject: Need special meal for my flight
Body: I have a peanut allergy and need a special meal for flight AA456 on Dec 25.
```

**System Response:**
1. Searches knowledge base
2. Partial match on special meals
3. Confidence: 0.45 (low)
4. Assigns to Tier 0 airline agent
5. SLA: Response in 60 min, Resolution in 4 hours

### Scenario 3: SLA Escalation

**Ticket Timeline:**
- 10:00 AM: Customer asks about refund
- 10:05 AM: Auto-assigned to Agent (Tier 0)
- 11:05 AM: No response (SLA breach)
- 11:05 AM: Auto-escalated to Tier 1 agent
- 11:15 AM: Tier 1 agent responds
- Resolution: Within SLA

---

## 🎨 UI Mockup (To Be Implemented)

```
┌────────────────────────────────────────────────────────────┐
│  SkyHigh Support    [IT Support ▼ | Airline Support]       │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  [Home] [My Bookings] [Flights] [Tickets] [Knowledge Base] │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ My Bookings                                         │   │
│  │                                                     │   │
│  │ ┌──────────┬──────────┬──────────┬─────────────┐  │   │
│  │ │ PNR      │ Flight   │ Date     │ Status      │  │   │
│  │ ├──────────┼──────────┼──────────┼─────────────┤  │   │
│  │ │ AA123456 │ AA123    │ Dec 25   │ Confirmed   │  │   │
│  │ │ AA789012 │ AA456    │ Jan 10   │ Pending     │  │   │
│  │ └──────────┴──────────┴──────────┴─────────────┘  │   │
│  │                                                     │   │
│  │ [Request Refund] [Change Flight] [View Details]    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Support Tickets                                     │   │
│  │                                                     │   │
│  │ Ticket #12345 - Flight Cancellation                 │   │
│  │ Status: Escalated (L1) | SLA: ⚠️ Response Breached  │   │
│  │ Assigned to: Jane Doe (Tier 1)                      │   │
│  │ [View Details]                                      │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

---

## 📈 Next Steps

1. **Complete priority-based RAG** (10 min)
2. **Create API endpoints** (30 min)
3. **Create sample data scripts** (20 min)
4. **Build frontend domain switcher** (40 min)
5. **Build airline pages** (60 min)
6. **Testing and refinement** (30 min)

**Total estimated time**: ~3 hours

---

## 🔧 Configuration

### Environment Variables

```env
# Existing
OPENAI_API_KEY=your_key
MONGODB_URL=mongodb://localhost:27017
EMAIL_USER=your_email
EMAIL_PASSWORD=your_password

# New (optional)
DEFAULT_SUPPORT_DOMAIN=AIRLINE  # or IT
SLA_CHECK_INTERVAL_MINUTES=5
```

### SLA Customization

Edit `app/database.py`:

```python
sla_matrix = {
    "urgent": {"response": 15, "resolution": 60},
    "high": {"response": 30, "resolution": 120},
    "medium": {"response": 60, "resolution": 240},
    "low": {"response": 120, "resolution": 480}
}
```

---

## 📚 Documentation Files

- `AIRLINE_SUPPORT_IMPLEMENTATION.md` - This file
- `AUTO_ASSIGNMENT_FIX.md` - Auto-assignment fixes
- `INTELLIGENT_AUTO_ASSIGNMENT.md` - Auto-assignment system
- `ANTI_HALLUCINATION_FIX.md` - RAG improvements
- `EXAMPLE_AUTO_ASSIGNMENT_EMAILS.md` - Test scenarios

---

## 💡 Tips

1. **Testing Airline Support:**
   - Load airline knowledge first
   - Create airline agents
   - Send emails with airline keywords (booking, flight, refund)

2. **Monitoring SLA:**
   - Check logs every 5 minutes for SLA monitoring
   - Watch for escalation messages
   - Use SLA dashboard API for metrics

3. **Priority Knowledge:**
   - Use priority=3 for urgent temporary updates
   - Set expiration date for temporary knowledge
   - Higher priority always wins in RAG search

---

Ready to continue with API implementation and frontend! 🚀

