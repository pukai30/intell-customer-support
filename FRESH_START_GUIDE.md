# Fresh Start Guide - Reset System to Zero

## Overview

This guide explains how to completely reset the Intelligent Customer Support System to start fresh with zero tickets and zero agent assignments.

---

## 🎯 What Gets Reset

### ✅ What Will Be Deleted/Cleared:
- ✓ **All Tickets** (including open, pending, resolved, closed)
- ✓ **All Agent Load Counts** (current_load, total_assigned, total_resolved)
- ✓ **All Ticket Statistics**

### ❌ What Will NOT Be Affected:
- ✗ **Agents** (agents remain with their skills, tiers, schedules)
- ✗ **Knowledge Base Documents** (all knowledge preserved)
- ✗ **SLA Policies** (SLA rules remain intact)
- ✗ **Official Holidays** (holiday calendar preserved)
- ✗ **Personal Agent Holidays** (agent-specific holidays preserved)
- ✗ **System Configuration** (email, WhatsApp, SMS settings preserved in `configurations` collection)

**Note**: System configuration is stored in MongoDB in the `configurations` collection (not in `.env`), but is NOT deleted during fresh start.

---

## 🚀 Method 1: Using the Fresh Start Script (Recommended)

### Step 1: Make sure backend is NOT running

If backend is running, stop it first:
```bash
# Press Ctrl+C in the terminal where backend is running
# Or kill the process:
# Windows: taskkill /F /IM python.exe
# Linux/Mac: pkill -f python
```

### Step 2: Run the fresh start script

```bash
python fresh_start.py
```

### Step 3: Confirm the reset

The script will:
1. Show you current ticket count
2. Show you agent count
3. Preview some tickets that will be deleted
4. Ask for confirmation (type `yes`)

**Example Output:**
```
=========================================
  🚀 FRESH START - SYSTEM RESET
=========================================

This will:
  ✓ Delete ALL tickets
  ✓ Reset agent current_load to 0
  ✓ Reset agent total_assigned to 0
  ✓ Reset agent total_resolved to 0

📊 Current Status:
  Tickets in database: 45
  Agents in database: 8

📋 Sample tickets to be deleted:
  1. EMAIL-ABC12345: Password reset request
  2. WHATSAPP-XYZ78901: Laptop not charging
  ...

⚠️  WARNING: This will delete ALL 45 tickets!
Type 'yes' to confirm reset: yes
```

### Step 4: Verify the reset

After confirming, you'll see:
```
✓ Deleted 45 tickets
✓ Reset 8 agents
  - current_load: 0
  - total_assigned: 0
  - total_resolved: 0

✅ Step 3: Verifying cleanup...
  ✓ All tickets deleted

Agent Status:
  ✓ John Doe: load=0, assigned=0
  ✓ Jane Smith: load=0, assigned=0
  ...

=========================================
✓ FRESH START COMPLETE!
=========================================
```

### Step 5: Restart backend (if needed)

```bash
python main.py
```

---

## 🛠️ Method 2: Using MongoDB Shell (Manual)

If you prefer to use MongoDB directly:

### Step 1: Open MongoDB shell

```bash
mongosh
```

### Step 2: Select database

```javascript
use customer_support
```

### Step 3: Delete all tickets

```javascript
db.tickets.deleteMany({})
```

Expected output:
```
{ acknowledged: true, deletedCount: 45 }
```

### Step 4: Reset agent workloads

```javascript
db.agents.updateMany(
  {},
  {
    $set: {
      current_load: 0,
      total_assigned: 0,
      total_resolved: 0
    }
  }
)
```

Expected output:
```
{ acknowledged: true, matchedCount: 8, modifiedCount: 8 }
```

### Step 5: Verify

```javascript
// Check ticket count (should be 0)
db.tickets.countDocuments({})

// Check agent loads (should all be 0)
db.agents.find({}, {name: 1, current_load: 1, total_assigned: 1})

// Note: System configuration is in 'configurations' collection and is NOT deleted
```

### Step 6: View all collections (optional)

```javascript
// See all collections in the database
show collections

// Output will show:
//   agents
//   tickets (now empty)
//   knowledge
//   holidays
//   configurations (system config is here, not deleted)
//   agent_holidays
//   sla_rules
```

### Step 7: Exit

```javascript
exit
```

---

## 🔍 Method 3: Using the Existing Cleanup Script

There's already a `cleanup_tickets.py` script:

```bash
python cleanup_tickets.py
```

**Note**: This script also resets agent counts, but the `fresh_start.py` has better verification and reporting.

---

## 📊 Before and After Comparison

### Before Reset:
```
Tickets: 45
  - Open: 12
  - In Progress: 8
  - Pending: 15
  - Resolved: 10

Agents: 8
  - John Doe: current_load=5, total_assigned=120
  - Jane Smith: current_load=3, total_assigned=95
  - Bob Wilson: current_load=4, total_assigned=110
  ...
```

### After Reset:
```
Tickets: 0

Agents: 8
  - John Doe: current_load=0, total_assigned=0
  - Jane Smith: current_load=0, total_assigned=0
  - Bob Wilson: current_load=0, total_assigned=0
  ...
```

---

## ✅ Post-Reset Checklist

After running the fresh start:

1. ✓ Tickets cleared
2. ✓ Agent workloads reset to 0
3. ✓ Restart backend server
4. ✓ Test with a new email/WhatsApp message
5. ✓ Verify ticket is created successfully
6. ✓ Verify agent gets assigned properly
7. ✓ Check agent load increments correctly

---

## 🧪 Testing After Fresh Start

### Test Email Processing:

1. Send an email to support email
2. Wait 2 minutes (background task interval)
3. Check backend logs:
   ```
   [14:30:15] Checking for new emails...
   ✓ Found 1 new email(s)
   ✓ Email from user@example.com auto-assigned to John Doe
   ```
4. Check frontend Tickets page - should show 1 new ticket
5. Check frontend Agents page - John Doe should show load=1

### Test WhatsApp Processing:

1. Send WhatsApp message to support number
2. Click "Check WhatsApp" button in Tickets page (or wait 2 minutes)
3. Check backend logs:
   ```
   [14:30:15] Checking WhatsApp messages from Twilio...
   ✓ Found 1 new WhatsApp message(s)
   ✓ WhatsApp ticket WHATSAPP-ABC123 assigned to Jane Smith
   ```
4. Check frontend - should show ticket assigned to agent

---

## 🔧 Troubleshooting

### Issue: "Cannot connect to database"

**Solution**:
```bash
# Check if MongoDB is running
# Windows:
Get-Service MongoDB

# Linux/Mac:
systemctl status mongod

# Start MongoDB if not running
# Windows: Start-Service MongoDB
# Linux/Mac: sudo systemctl start mongod
```

### Issue: "Agents still show old load"

**Solution**:
```bash
# Manually reset in MongoDB shell:
db.agents.updateMany(
  {},
  { $set: { current_load: 0, total_assigned: 0, total_resolved: 0 } }
)
```

### Issue: "Some tickets still exist after reset"

**Solution**:
```bash
# Manually delete in MongoDB shell:
db.tickets.deleteMany({})
```

---

## 📝 Important Notes

1. **Backup First**: Before running fresh start, consider backing up your data:
   ```bash
   # Create backup
   mongodump --db customer_support --out backup/
   ```

2. **Check Agent Status**: After reset, verify all agents show load=0 in the frontend

3. **Knowledge Base**: Your knowledge base documents are NOT deleted - good!

4. **Configuration**: Email, WhatsApp, SMS configuration is preserved - no need to reconfigure

5. **SLA Policies**: Your SLA policies remain - no need to recreate them

## 📊 MongoDB Collections

Your database contains these collections:
- `agents` - Support agents
- `tickets` - All support tickets (deleted during fresh start)
- `knowledge` - Knowledge base documents
- `holidays` - Official holidays
- `agent_holidays` - Personal agent holidays
- `configurations` - System configuration (email, WhatsApp, SMS settings)
- `sla_rules` - SLA policies

**Note**: System configuration is stored in the `configurations` collection in MongoDB, NOT in the `.env` file. This is different from environment variables.

---

## 🎯 Use Cases for Fresh Start

1. **Development/Testing**: Start with clean slate for testing
2. **Production Reset**: Reset production after major issues
3. **Data Migration**: Clear old data before importing new data
4. **Load Testing**: Reset system state between load tests
5. **Bug Reproduction**: Start fresh to reproduce specific bugs

---

## 🔐 Safety Measures

The fresh start script includes safety measures:

1. ✓ Shows count of items to be deleted
2. ✓ Shows preview of tickets to be deleted
3. ✓ Requires explicit confirmation ("yes")
4. ✓ Reports what was deleted
5. ✓ Verifies cleanup was successful
6. ✓ Doesn't delete agents, knowledge base, or configuration

---

## 📞 Need Help?

If you encounter issues:

1. Check MongoDB is running
2. Check database credentials in `.env` file
3. Check backend logs for errors
4. Verify database connection in `test_mongodb_connection.py`
5. Review `APP_CODE_DOCUMENTATION.md` for detailed information

---

## Summary

**Quick Command:**
```bash
python fresh_start.py
```

**What It Does:**
- Deletes all tickets
- Resets agent loads to 0
- Preserves agents, knowledge base, configuration

**Time Required:**
- Fresh Start Script: 10-30 seconds
- Manual MongoDB: 2-5 minutes

**Result:**
- Clean system ready for new tickets
- Agents ready to receive new assignments
- All statistics reset to zero

