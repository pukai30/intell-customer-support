# Quick Setup: Intelligent Auto-Assignment System

## 🚀 Complete Setup in 5 Steps

### Step 1: Start Backend
```bash
python main.py
```

Wait for:
```
✅ System ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Create Sample Agents
```bash
# In a new terminal
python setup_sample_agents.py
```

Expected output:
```
✓ Successfully created: 8/8 agents
```

### Step 3: Start Frontend
```bash
cd frontend
npm run dev
```

### Step 4: View Agents Dashboard
Open browser: http://localhost:3000/agents

You'll see:
- 8 agents with different skills
- Team utilization stats
- Individual agent workload

### Step 5: Test Auto-Assignment

**Send a test email:**
```
To: your-support@company.com
Subject: I forgot my password
Body: Can you help me reset my password?
```

**Within 2 minutes:**
1. ✅ Email processed by AI
2. ✅ Low confidence detected (or high, depends on KB)
3. ✅ Skills analyzed: ["password", "email"]
4. ✅ Auto-assigned to Sarah Johnson (password expert)
5. ✅ Visible in tickets page with assignment info

## 📊 What You'll See

### Backend Console
```
🔍 Analyzing ticket EMAIL-ABC123
   Required skills: ['password', 'email']
   Priority: medium
✓ Best agent found: Sarah Johnson (sarah.johnson@company.com)
   Skills: ['password', 'email', 'security']
   Current load: 0/15
✓ Ticket EMAIL-ABC123 assigned to Sarah Johnson
✓ Email from customer@example.com auto-assigned to Sarah Johnson
```

### Frontend Agents Page
```
Team Statistics:
├─ Total Agents: 8
├─ Active Agents: 8  
├─ Team Capacity: 95
├─ Current Load: 1
└─ Team Utilization: 1.1%

Sarah Johnson (AGENT-001)
├─ Status: Active
├─ Skills: password (E), email (E), security (I)
├─ Workload: 1/15 (6.7%)
├─ Total Assigned: 1
├─ Total Resolved: 0
└─ Channels: 📧 💻 💬
```

### Frontend Tickets Page
```
Ticket: EMAIL-ABC123
├─ Customer: customer@example.com
├─ Subject: I forgot my password
├─ Status: Pending
├─ Assigned To: 👤 sarah.johnson
└─ Conversation:
    ├─ 👤 Customer: "Can you help me reset my password?"
    ├─ 🤖 AI: [Low confidence response]
    └─ ⚙️ System: "🎯 Ticket automatically assigned to Sarah Johnson..."
```

## 🧪 Test Different Scenarios

### Test 1: VPN Issue
```
Subject: VPN won't connect
→ Should assign to: Michael Chen or Thomas Anderson (VPN experts)
```

### Test 2: Mobile Device
```
Subject: iPhone email setup
→ Should assign to: Emily Rodriguez or Amanda Wilson (mobile experts)
```

### Test 3: Hardware Problem
```
Subject: Printer not working
→ Should assign to: David Kim or Thomas Anderson (hardware experts)
```

### Test 4: Security Concern
```
Subject: Suspicious email received
→ Should assign to: Jessica Brown (security expert)
```

## 📱 Available Channels

The system automatically assigns based on channel:

- **📧 Email**: All agents support
- **💬 SMS**: Agents 1, 3, 6, 7
- **📱 WhatsApp**: Agents 3, 6, 7
- **💻 Chat**: All agents except Agent 7

## 🎛️ Agent Management

### Toggle Agent Status
```bash
# Deactivate agent
curl -X PUT "http://localhost:8000/api/agents/AGENT-001/status?is_active=false"

# Reactivate agent
curl -X PUT "http://localhost:8000/api/agents/AGENT-001/status?is_active=true"
```

Or use the frontend toggle buttons on the agents page.

### View Agent Stats
```bash
curl http://localhost:8000/api/agents/AGENT-001/stats
```

### View Team Stats
```bash
curl http://localhost:8000/api/agents/team/stats
```

## 🔍 Monitoring

### Real-Time Dashboard
- Auto-refreshes every 30 seconds
- Shows live workload distribution
- Displays top performers
- Color-coded utilization bars

### Agent Cards Show:
- ✅ Current workload (X/Y tickets)
- ✅ Utilization percentage
- ✅ Skills and expertise levels
- ✅ Total tickets assigned/resolved
- ✅ Last assignment timestamp
- ✅ Supported channels

## 🏆 Top Performers

The system tracks and displays:
- Most tickets resolved
- Average resolution time
- Leaderboard with medals (🥇🥈🥉)

## ⚙️ Customization

### Add New Agent
```bash
curl -X POST http://localhost:8000/api/agents/create \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "AGENT-009",
    "name": "Your Name",
    "email": "your.name@company.com",
    "skills": ["password", "network"],
    "skill_levels": {
      "password": "expert",
      "network": "intermediate"
    },
    "max_concurrent_tickets": 10,
    "channels": ["email", "chat"]
  }'
```

### Modify Skills (Backend)
Edit `app/skill_mapper.py`:
- Add new skill categories
- Update keywords
- Adjust priorities

## 🎯 Success Criteria

System is working correctly when:

1. ✅ Agents appear on dashboard
2. ✅ Team stats show capacity
3. ✅ Test email triggers assignment
4. ✅ Console shows assignment logic
5. ✅ Ticket shows assigned agent
6. ✅ Agent's workload increments
7. ✅ Dashboard updates in real-time

## 🐛 Troubleshooting

**No agents showing?**
```bash
# Check if agents were created
curl http://localhost:8000/api/agents/list
# If empty, run: python setup_sample_agents.py
```

**Assignment not working?**
```bash
# Check backend console for errors
# Verify agents are active
# Ensure agent has capacity (load < max)
```

**Frontend not updating?**
- Hard refresh: Ctrl+Shift+R
- Check backend is running
- Verify API URL in frontend/.env.local

## 📚 Documentation

- Full system docs: `INTELLIGENT_AUTO_ASSIGNMENT.md`
- Assignment features: `ASSIGNMENT_AND_NOTIFICATION_FEATURES.md`
- API reference: Check `/docs` endpoint when backend is running

## 🎉 You're All Set!

Your intelligent auto-assignment system is now:
- ✅ Routing tickets based on skills
- ✅ Balancing workload across agents
- ✅ Tracking performance metrics
- ✅ Providing real-time monitoring
- ✅ Supporting all channels (email, SMS, WhatsApp)

**Next**: Send test emails and watch the magic happen! 🚀

