# Example Emails for Auto-Assignment Testing

This document contains example emails that will trigger auto-assignment based on different scenarios.

---

## ✅ Emails That Will Be AUTO-RESPONDED (High Confidence)

These emails match the knowledge base and will get automatic AI responses:

### 1. Password Reset Request
```
Subject: Forgot my password
Body: Hi, I forgot my password and can't log into my account. Can you help me reset it?
```
**Result**: AI will respond with password reset instructions from knowledge base

### 2. VPN Connection Issue
```
Subject: VPN not connecting
Body: My VPN client is not connecting. I keep getting a connection timeout error.
```
**Result**: AI will respond with VPN troubleshooting steps from knowledge base

### 3. Printer Problem
```
Subject: Printer not working
Body: The office printer is showing an error and not printing my documents.
```
**Result**: AI will respond with printer troubleshooting from knowledge base

---

## 🎯 Emails That Will Trigger AUTO-ASSIGNMENT (Low Confidence)

These emails require human intervention and will be auto-assigned to agents:

### 1. Complex Hardware Request (Assigned to Hardware Specialist)
```
Subject: Need new workstation for AutoCAD
Body: I need a new high-performance workstation for running AutoCAD and 3D rendering software. 
My current computer is too slow for the new projects. Can someone help me get approval and 
configure the right specs? I also need it integrated with our domain and all software licenses transferred.
```
**Why assigned**: Complex procurement + custom configuration not in KB
**Assigned to**: Agent with "hardware" skill (e.g., David Lee or Priya Sharma)

---

### 2. Security Incident (Assigned to Security Specialist)
```
Subject: Suspicious email with attachment
Body: I received a suspicious email claiming to be from IT asking me to download an attachment 
and enter my credentials. I didn't click it, but I'm worried it might be a phishing attempt. 
Several colleagues also received similar emails. Should I report this somewhere?
```
**Why assigned**: Security incident requiring investigation, not standard KB
**Assigned to**: Agent with "security" skill (e.g., Michael Brown)

---

### 3. Custom Software Development Request (Assigned to Software Specialist)
```
Subject: Need custom Excel macro for reporting
Body: Our team needs a custom Excel macro to automate our monthly sales reports. The macro 
should pull data from multiple sheets, calculate totals, and generate charts. Can someone 
from IT help develop this?
```
**Why assigned**: Custom development work, not standard support
**Assigned to**: Agent with "software" skill (e.g., Sarah Johnson or Michael Brown)

---

### 4. Network Infrastructure Issue (Assigned to Network Specialist)
```
Subject: Entire floor has no internet
Body: The entire 3rd floor has lost internet connectivity since this morning. Around 50 
employees are affected. The network switches seem to be working but there's no internet access. 
This is urgent as it's impacting business operations.
```
**Why assigned**: Infrastructure issue requiring on-site investigation
**Assigned to**: Agent with "network" skill (e.g., Emily Chen or David Lee)

---

### 5. Account Access Request (Assigned to Account Specialist)
```
Subject: Need access to SAP and SharePoint
Body: I'm a new employee in the Finance department. I need access to SAP for financial reporting 
and SharePoint for the Finance shared drive. My manager is John Smith. When can this be set up?
```
**Why assigned**: Requires approval and manual account provisioning
**Assigned to**: Agent with "account" skill (e.g., Sarah Johnson or Priya Sharma)

---

### 6. Email Server Configuration (Assigned to Email Specialist)
```
Subject: Setting up email forwarding for team mailbox
Body: I need to set up automatic email forwarding from our team mailbox (support@company.com) 
to three different team members. Also, I need to configure an auto-reply for when we're out of office. 
Can someone help with the Exchange server settings?
```
**Why assigned**: Requires server-side configuration, not user-level support
**Assigned to**: Agent with "email" skill (e.g., Michael Brown or David Lee)

---

### 7. Data Recovery Request (Assigned to Hardware/Software Specialist)
```
Subject: Accidentally deleted important files
Body: I accidentally deleted an entire folder of important project files from my computer yesterday. 
They're not in the Recycle Bin. Is there any way to recover them? These files are critical for 
tomorrow's client presentation.
```
**Why assigned**: Requires specialized data recovery tools/process
**Assigned to**: Agent with "hardware" or "software" skill

---

### 8. Unclear/Vague Issue (Assigned Based on Keywords)
```
Subject: Computer acting weird
Body: My computer is doing strange things. Sometimes it's slow, sometimes programs crash, 
and today it showed a blue screen once. Not sure what's wrong.
```
**Why assigned**: Vague issue requiring diagnosis, multiple possible causes
**Assigned to**: Agent with "hardware" or "software" skill based on keywords

---

### 9. Policy Question (Low KB Match)
```
Subject: Can I use personal cloud storage for work files?
Body: I want to use my personal Dropbox account to sync work files between my office computer 
and home laptop. Is this allowed according to company IT policy? If not, what are the approved alternatives?
```
**Why assigned**: Policy question that may not be in technical KB
**Assigned to**: Agent with general IT skills or security background

---

### 10. Multi-System Integration Issue (Complex)
```
Subject: CRM not syncing with Outlook calendar
Body: Our CRM system is not syncing appointments to Outlook calendars. I've tried reconnecting 
the integration but it still doesn't work. This is affecting the whole sales team's scheduling. 
Can someone look into the API connection?
```
**Why assigned**: Complex integration issue requiring technical investigation
**Assigned to**: Agent with "software" and "email" skills

---

## 🧪 How to Test Auto-Assignment

### Step 1: Send a Test Email
Send one of the "auto-assignment" emails above to your configured support email address.

### Step 2: Check Backend Logs
Look for these messages in the backend console:
```
✓ Email from user@example.com auto-assigned to [Agent Name]
  - Agent: [agent_name]
  - Skills matched: [skill1, skill2]
  - Confidence: [0.0-0.7]
```

### Step 3: Check UI
1. Go to **Tickets Page** (http://localhost:3000/tickets)
2. Look for the `Requires Human` badge
3. Check the `Assigned To` column
4. Click "View" to see full conversation and assignment details

### Step 4: Check Agent Dashboard
1. Go to **Agents Page** (http://localhost:3000/agents)
2. See the agent's workload increase
3. Check team statistics

---

## 🎨 Assignment Logic Summary

The system assigns tickets based on:

1. **Skill Matching**: Extracts skills from ticket content and matches with agent skills
2. **Skill Level**: Prefers agents with higher skill levels (expert > advanced > intermediate)
3. **Workload**: Balances assignments across agents (prefers lower current load)
4. **Availability**: Only assigns to active agents
5. **Channel Support**: Ensures agent supports the communication channel
6. **Working Hours**: Considers agent shift timings (if configured)

---

## 📊 Sample Agents and Their Skills

Based on `setup_sample_agents.py`:

| Agent | Skills | Best For |
|-------|--------|----------|
| Sarah Johnson | software, email, account (expert) | Software issues, email, accounts |
| Michael Brown | network, security, software (expert) | Security incidents, network |
| Emily Chen | hardware, network (expert) | Hardware, network infrastructure |
| David Lee | hardware, email, network (advanced) | Hardware, email server |
| Priya Sharma | software, hardware, account (advanced) | General IT, accounts |
| John Wilson | software, network (intermediate) | Basic software/network |
| Lisa Anderson | email, account (intermediate) | Email, user accounts |
| Robert Martinez | hardware, software (intermediate) | Basic hardware/software |

---

## 💡 Tips for Testing

1. **Test different skills**: Send emails requiring different expertise to see routing
2. **Test workload balancing**: Send multiple tickets to see distribution
3. **Check confidence scores**: Look at backend logs to see RAG confidence levels
4. **Test edge cases**: Send vague or ambiguous requests
5. **Monitor notifications**: Check for unassigned ticket notifications if no agent matches

---

## 🚨 When NO Assignment Happens

If no suitable agent is found, the system will:
- Mark ticket as `requires_human: true`
- Send a notification (visible in UI banner)
- Set priority to "high"
- Wait for manual assignment

This happens when:
- No agents are active
- No agent has the required skills
- All agents are at maximum load
- No agent supports the channel

