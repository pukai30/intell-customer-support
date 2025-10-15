# 🎯 SLA Management System - Complete Guide

## Overview

Industry-standard SLA (Service Level Agreement) Management system with policy configuration, business hours, escalation rules, templates, and full UI management.

---

## ✨ Features Implemented

### 1. **SLA Policy Management**
- ✅ Create custom SLA policies
- ✅ Category-based SLAs (hardware, software, network, security, etc.)
- ✅ Priority-based SLAs (urgent, high, medium, low)
- ✅ Customer tier-based SLAs (VIP, premium, standard)
- ✅ Response and resolution time tracking
- ✅ Policy activation/deactivation
- ✅ Default policy configuration

### 2. **Business Hours Configuration**
- ✅ Working days selection (Mon-Fri, custom days)
- ✅ Business hours (9-5, custom times)
- ✅ Timezone support
- ✅ 24/7 vs Business Hours option
- ✅ Holiday calendar management

### 3. **Escalation Matrix**
- ✅ Multi-level escalation rules
- ✅ Time-based escalation triggers
- ✅ Tier-based agent routing
- ✅ Email notifications on escalation
- ✅ Automatic vs manual escalation

### 4. **SLA Templates**
- ✅ Predefined policy templates
- ✅ Quick-start configurations
- ✅ Template application to domain
- ✅ Industry-standard presets

### 5. **Frontend Management UI**
- ✅ Policy creation interface
- ✅ Policy listing and filtering
- ✅ Policy details view
- ✅ Template browser
- ✅ Visual time formatting
- ✅ Real-time updates

---

## 📊 Default SLA Policies

### 1. **Critical Issues - 24/7** (`IT_CRITICAL_247`)
- **Response Time:** 15 minutes
- **Resolution Time:** 1 hour
- **Coverage:** 24/7
- **Categories:** outage, security, data-loss
- **Priorities:** urgent, critical
- **Escalation:** 3 levels (L1→L2→L3)

### 2. **High Priority - Business Hours** (`IT_HIGH_BUSINESS_HOURS`)
- **Response Time:** 30 minutes
- **Resolution Time:** 4 hours
- **Coverage:** Business Hours
- **Categories:** hardware, software, network, email
- **Priorities:** high
- **Escalation:** 2 levels

### 3. **Medium Priority - Standard** (`IT_MEDIUM_STANDARD`) ⭐ DEFAULT
- **Response Time:** 2 hours
- **Resolution Time:** 8 hours (1 business day)
- **Coverage:** Business Hours
- **Categories:** password, account, access, general
- **Priorities:** medium
- **Escalation:** 1 level

### 4. **Low Priority - Requests** (`IT_LOW_REQUESTS`)
- **Response Time:** 8 hours
- **Resolution Time:** 40 hours (5 business days)
- **Coverage:** Business Hours
- **Categories:** feature-request, enhancement, question
- **Priorities:** low
- **Escalation:** None

### 5. **VIP Customer - Expedited** (`IT_VIP_EXPEDITED`)
- **Response Time:** 15 minutes
- **Resolution Time:** 2 hours
- **Coverage:** 24/7
- **Customer Tier:** VIP
- **Priorities:** medium, high, urgent
- **Escalation:** 2 levels

### 6. **Network Issues - Urgent** (`IT_NETWORK_URGENT`)
- **Response Time:** 20 minutes
- **Resolution Time:** 2 hours
- **Coverage:** 24/7
- **Categories:** network, connectivity, vpn, wifi
- **Priorities:** high, urgent
- **Escalation:** 2 levels

### 7. **Security - Immediate** (`IT_SECURITY_IMMEDIATE`) 🔥 HIGHEST
- **Response Time:** 10 minutes
- **Resolution Time:** 1 hour
- **Coverage:** 24/7
- **Categories:** security, breach, malware, phishing
- **Priorities:** urgent, critical
- **Escalation:** 2 levels (rapid escalation at 5 & 30 min)
- **Notifications:** Security team + CISO

---

## 🚀 Quick Start

### Step 1: Load Default SLA Policies
```bash
python setup_sla_policies.py
```

**Output:**
```
✅ SLA Setup Complete!
   - Policies Created: 7
   - Templates Created: 3
```

### Step 2: Access SLA Management UI
1. Start backend: `python main.py`
2. Start frontend: `cd frontend && npm run dev`
3. Go to: http://localhost:3000/sla-management

### Step 3: View SLA Dashboard
- Go to: http://localhost:3000/sla-dashboard
- Monitor compliance rates
- Check SLA breaches
- View escalation levels

---

## 🔧 API Endpoints

### Policy Management

#### Create SLA Policy
```bash
POST /api/sla/policies/create
```

**Request Body:**
```json
{
  "policy_id": "IT_CUSTOM_HIGH",
  "name": "Custom High Priority",
  "description": "Custom SLA for high priority tickets",
  "domain": "IT",
  "categories": ["hardware", "software"],
  "priorities": ["high"],
  "customer_tiers": ["standard"],
  "response_time_minutes": 30,
  "resolution_time_minutes": 240,
  "use_business_hours": true,
  "auto_escalate": true,
  "is_default": false,
  "priority_order": 75
}
```

#### List SLA Policies
```bash
GET /api/sla/policies/list?domain=IT&is_active=true
```

#### Get Policy Details
```bash
GET /api/sla/policies/{policy_id}
```

#### Update Policy
```bash
PUT /api/sla/policies/{policy_id}
```

**Request Body:**
```json
{
  "response_time_minutes": 20,
  "resolution_time_minutes": 180
}
```

#### Delete (Deactivate) Policy
```bash
DELETE /api/sla/policies/{policy_id}
```

### Template Management

#### List Templates
```bash
GET /api/sla/templates/list?category=IT
```

#### Get Template Details
```bash
GET /api/sla/templates/{template_id}
```

#### Apply Template
```bash
POST /api/sla/templates/{template_id}/apply?domain=IT
```

---

## 📖 Policy Matching Logic

When a ticket is created, the system finds the best matching SLA policy:

### Matching Priority (Highest to Lowest):
1. **Category Match** (score +10)
2. **Priority Match** (score +5)
3. **Customer Tier Match** (score +3)
4. **Policy Priority Order** (configurable)
5. **Default Policy** (fallback)

### Example Scenarios:

**Scenario 1: VIP Customer with Network Issue**
- Ticket: `category=network, priority=high, customer_tier=vip`
- **Matches:** `IT_VIP_EXPEDITED` (best match due to VIP tier)
- **SLA:** 15min response, 2hr resolution, 24/7

**Scenario 2: Standard Customer with Security Breach**
- Ticket: `category=security, priority=urgent, customer_tier=standard`
- **Matches:** `IT_SECURITY_IMMEDIATE` (highest priority)
- **SLA:** 10min response, 1hr resolution, 24/7

**Scenario 3: Password Reset Request**
- Ticket: `category=password, priority=medium, customer_tier=standard`
- **Matches:** `IT_MEDIUM_STANDARD` (default policy)
- **SLA:** 2hr response, 8hr resolution, business hours

---

## 🎨 Frontend UI Features

### SLA Management Page (`/sla-management`)

**Features:**
- ✅ Create new SLA policies with form
- ✅ View all active policies in table
- ✅ Filter by domain and status
- ✅ Policy details modal
- ✅ Delete (deactivate) policies
- ✅ SLA template quick-start
- ✅ Visual time formatting (15m, 2h, 1day)
- ✅ Status indicators (Active/Inactive)
- ✅ Default policy badges

**Navigation:**
```
🤖 IT Support
├─ 📚 Knowledge Base
├─ 🎫 Tickets
├─ 👥 Agents
├─ 📊 SLA (Dashboard)
└─ ⚙️ SLA Config (Management) ← NEW
```

---

## 💼 Use Cases

### Use Case 1: Standard IT Support Team
**Setup:** Apply "Standard IT Support SLA" template
- Critical issues: 15min/1hr
- High priority: 30min/4hr
- Medium (default): 2hr/8hr
- Low priority: 8hr/5days

### Use Case 2: Enterprise with VIP Customers
**Setup:** Apply "Enterprise IT SLA" template
- All standard policies + VIP expedited support
- VIP gets 15min response time on all priorities
- 24/7 coverage for VIP customers

### Use Case 3: Security-Focused Organization
**Setup:** Create custom security policy
- Security incidents: 10min response, immediate escalation
- CISO notification on all security tickets
- No SLA breaches allowed for security

### Use Case 4: Small Team with Limited Hours
**Setup:** Apply "Basic IT Support" template
- Single SLA for all tickets
- 4hr response, 2-day resolution
- Business hours only (9-5)

---

## 📈 Business Hours Calculation

### Example: Business Hours Mode

**Configuration:**
- Working Days: Monday-Friday
- Hours: 9:00 AM - 5:00 PM (8 hours/day)
- Timezone: UTC

**Ticket Created:** Friday 4:00 PM
**SLA:** 2-hour response time

**Calculation:**
- 1 hour remaining on Friday (4PM-5PM)
- Pause over weekend
- Resume Monday 9:00 AM
- 1 hour remaining Monday morning
- **Deadline:** Monday 10:00 AM

### Example: 24/7 Mode

**Configuration:**
- 24/7 coverage
- No business hours restriction

**Ticket Created:** Friday 4:00 PM
**SLA:** 2-hour response time

**Calculation:**
- Continuous time counting
- **Deadline:** Friday 6:00 PM (same day)

---

## 🔄 Escalation Workflow

### Automatic Escalation Example:

**Ticket:** High priority issue (30min response, 4hr resolution)

**Timeline:**
1. **10:00 AM** - Ticket created, assigned to Tier 0 agent
2. **10:30 AM** - Response SLA deadline
3. **10:32 AM** - No response → Auto-escalate to Tier 1
4. **10:35 AM** - Tier 1 agent responds (SLA met)
5. **2:00 PM** - Resolution SLA deadline
6. **1:45 PM** - Ticket resolved by Tier 1 (SLA met)

**Result:** ✅ No SLA breach, escalation worked as intended

---

## 🛠️ Customization Guide

### Creating a Custom SLA Policy

**Via UI:**
1. Go to `/sla-management`
2. Click "Create New Policy"
3. Fill in the form:
   - Policy ID: `IT_CUSTOM_URGENT`
   - Name: `Custom Urgent Issues`
   - Categories: `database, application`
   - Response: `20 minutes`
   - Resolution: `2 hours`
   - Coverage: `24/7`
4. Click "Create Policy"

**Via API:**
```python
import requests

policy_data = {
    "policy_id": "IT_CUSTOM_URGENT",
    "name": "Custom Urgent Issues",
    "description": "Database and application critical issues",
    "domain": "IT",
    "categories": ["database", "application"],
    "priorities": ["urgent"],
    "response_time_minutes": 20,
    "resolution_time_minutes": 120,
    "use_business_hours": False,
    "auto_escalate": True,
    "priority_order": 85
}

response = requests.post(
    "http://localhost:8000/api/sla/policies/create",
    json=policy_data
)
print(response.json())
```

---

## 📊 Monitoring & Reporting

### SLA Dashboard Metrics

**Available Metrics:**
- ✅ Total tickets processed
- ✅ Response SLA compliance rate
- ✅ Resolution SLA compliance rate
- ✅ Average response time
- ✅ SLA breach count
- ✅ Tickets by escalation level (L0-L3)
- ✅ Breached tickets list

**Access:** http://localhost:3000/sla-dashboard

---

## 🎯 Best Practices

### 1. **Policy Design**
- ✅ Create specific policies for critical categories
- ✅ Use priority-based SLAs for general coverage
- ✅ Set one default policy as fallback
- ✅ Order policies by specificity (priority_order)

### 2. **Business Hours**
- ✅ Use 24/7 for critical/security issues
- ✅ Use business hours for standard requests
- ✅ Configure holidays for accurate calculations
- ✅ Set appropriate timezone

### 3. **Escalation Rules**
- ✅ Define multiple escalation levels
- ✅ Set reasonable trigger times
- ✅ Map to appropriate agent tiers
- ✅ Add notification emails for critical escalations

### 4. **Customer Tiers**
- ✅ Create VIP policies with expedited SLAs
- ✅ Separate premium from standard support
- ✅ Ensure VIP policies have high priority_order

---

## 🚨 Troubleshooting

### Issue: No SLA policy matched
**Solution:** Ensure you have a default policy (`is_default=true`)

### Issue: Wrong policy applied
**Solution:** Check `priority_order` values and policy specificity

### Issue: Business hours not calculating correctly
**Solution:** Verify timezone and working days configuration

### Issue: Escalations not triggering
**Solution:** Check `auto_escalate=true` and escalation rules are defined

---

## 📚 Related Documentation

- `CURRENT_STATUS.md` - Application status
- `README.md` - Project overview
- `DEPLOYMENT_CHECKLIST.md` - Production deployment
- `INTELLIGENT_AUTO_ASSIGNMENT.md` - Agent assignment logic

---

## 🎉 Summary

You now have a **complete industry-standard SLA Management system** with:

✅ 7 predefined policies covering all scenarios
✅ 3 quick-start templates
✅ Full CRUD API for policies
✅ Business hours & holiday support
✅ Multi-level escalation matrix
✅ Customer tier-based SLAs
✅ Beautiful management UI
✅ Real-time SLA monitoring dashboard

**The system is production-ready and follows industry best practices!** 🚀

---

**Setup Time:** < 5 minutes  
**Policies:** 7 ready-to-use  
**Templates:** 3 configurations  
**API Endpoints:** 8 endpoints  
**Frontend Pages:** 2 pages (Dashboard + Management)

**Start managing SLAs like a pro!** ⚡

