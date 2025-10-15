# 🗓️ Holiday Calendar Management System

## Overview

The Holiday Calendar Management System provides comprehensive holiday and leave management for your customer support team. It includes Indian national holidays, regional holidays, and individual agent holiday management with holiday-aware ticket assignment.

## 🎯 Features

### 1. **Indian National Holidays**
- ✅ **2024-2025 Calendar**: Complete Indian holiday calendar
- ✅ **National Holidays**: Republic Day, Independence Day, Gandhi Jayanti, etc.
- ✅ **Religious Holidays**: Holi, Diwali, Eid, Christmas, etc.
- ✅ **Regional Holidays**: Maharashtra, Karnataka, Tamil Nadu
- ✅ **Company Holidays**: New Year's Eve/Day

### 2. **Individual Agent Holidays**
- ✅ **Personal Leave**: Individual agent leave management
- ✅ **Leave Types**: Personal, Sick, Vacation, Emergency
- ✅ **Partial Day Leave**: Start/end time support
- ✅ **Approval Workflow**: Manager approval tracking
- ✅ **Reason Tracking**: Leave reason documentation

### 3. **Holiday-Aware Assignment**
- ✅ **Smart Assignment**: Skips agents on holidays
- ✅ **Time-Based Checking**: Partial day leave support
- ✅ **Workload + Holiday**: Combines both factors
- ✅ **Fallback Logic**: Assigns to available agents only

### 4. **Management UI**
- ✅ **Agent Details Page**: Individual holiday calendar
- ✅ **Holiday Management**: Add/edit/delete holidays
- ✅ **Visual Calendar**: Easy holiday viewing
- ✅ **Leave Types**: Color-coded leave types

## 🚀 Quick Setup

### 1. Load Indian Holidays
```bash
python setup_indian_holidays.py
```

### 2. Access Agent Details
- Go to `/agents` page
- Click on any agent name
- View their holiday calendar
- Add/edit holidays

### 3. Test Holiday Assignment
- Create agent holidays
- Send test emails
- Verify assignment skips agents on holidays

## 📋 API Endpoints

### Holiday Management
```bash
# Get all holidays
GET /api/holidays/list?year=2024&holiday_type=national

# Check if date is holiday
GET /api/holidays/check/2024-01-26?region=Maharashtra

# Create holiday
POST /api/holidays/create
```

### Agent Holiday Management
```bash
# Get agent holidays
GET /api/agents/{agent_id}/holidays?start_date=2024-01-01&end_date=2024-12-31

# Create agent holiday
POST /api/agents/{agent_id}/holidays/create

# Check agent holiday status
GET /api/agents/{agent_id}/holidays/check/2024-01-26?time=14:30

# Update agent holiday
PUT /api/agents/{agent_id}/holidays/{holiday_id}

# Delete agent holiday
DELETE /api/agents/{agent_id}/holidays/{holiday_id}
```

### Available Agents
```bash
# Get available agents (holiday-aware)
GET /api/agents/available?date=2024-01-26&time=14:30&skills=network,security&domain=IT
```

## 🎨 Frontend Pages

### 1. **Agent Details Page** (`/agents/[agentId]`)
- **Agent Information**: Complete agent details
- **Holiday Calendar**: Visual holiday management
- **Add Holiday**: Modal for creating holidays
- **Leave Management**: Edit/delete holidays

### 2. **Agents List Page** (`/agents`)
- **Clickable Names**: Links to agent details
- **Holiday Status**: Visual indicators
- **Quick Access**: Direct navigation

## 🔧 Configuration

### Holiday Types
- **national**: Indian national holidays
- **regional**: State-specific holidays
- **company**: Company-specific holidays
- **personal**: Individual agent holidays

### Leave Types
- **personal**: Personal leave
- **sick**: Sick leave
- **vacation**: Vacation leave
- **emergency**: Emergency leave

### Regional Support
- **Maharashtra**: Shivaji Jayanti, Maharashtra Day
- **Karnataka**: Karnataka Rajyotsava
- **Tamil Nadu**: Pongal

## 📊 Assignment Logic

### Holiday-Aware Assignment Process
1. **Extract Skills**: Analyze ticket for required skills
2. **Get Current Date/Time**: Check for holidays
3. **Filter Agents**: Only available agents (not on holiday)
4. **Calculate Scores**: Skills + Load + Tier + Channel
5. **Assign Best**: Highest scoring available agent

### Assignment Factors
- **Skills Match**: 40% weight
- **Load Factor**: 30% weight
- **Tier Level**: 20% weight
- **Channel Preference**: 10% weight
- **Holiday Status**: Must be available

## 🎯 Use Cases

### 1. **National Holiday Management**
```python
# All agents get national holidays
# No tickets assigned on Republic Day, Independence Day, etc.
# Automatic holiday detection
```

### 2. **Individual Leave Management**
```python
# Agent takes personal leave
# System skips them for assignments
# Other agents handle their workload
```

### 3. **Partial Day Leave**
```python
# Agent available 9 AM - 1 PM
# System assigns only during available hours
# After 1 PM, skips this agent
```

### 4. **Regional Holiday Support**
```python
# Maharashtra agents get state holidays
# Karnataka agents get different holidays
# System respects regional preferences
```

## 🔍 Monitoring & Analytics

### Holiday Impact
- **Assignment Success Rate**: With/without holidays
- **Agent Availability**: Holiday vs working days
- **Load Distribution**: During holiday periods

### Leave Analytics
- **Leave Patterns**: Most common leave types
- **Approval Times**: Manager response times
- **Coverage**: Holiday coverage analysis

## 🚨 Troubleshooting

### Common Issues

#### 1. **Agents Not Getting Assigned**
```bash
# Check if agent is on holiday
GET /api/agents/{agent_id}/holidays/check/{date}?time={time}

# Verify agent availability
GET /api/agents/available?date={date}&time={time}
```

#### 2. **Holidays Not Loading**
```bash
# Check holiday data
GET /api/holidays/list

# Verify Indian holidays loaded
python setup_indian_holidays.py
```

#### 3. **Assignment Issues**
```bash
# Check available agents
GET /api/agents/available?date=2024-01-26&time=14:30

# Verify agent skills and load
GET /api/agents/{agent_id}
```

## 📈 Best Practices

### 1. **Holiday Planning**
- Load holidays in advance
- Plan for peak periods
- Consider regional differences

### 2. **Leave Management**
- Approve leaves promptly
- Plan coverage for key agents
- Use partial day leaves effectively

### 3. **Assignment Optimization**
- Monitor assignment success rates
- Adjust agent skills as needed
- Balance workload during holidays

## 🎉 Success Metrics

### Holiday System Success
- ✅ **100% Holiday Coverage**: All Indian holidays loaded
- ✅ **Smart Assignment**: Skips agents on holidays
- ✅ **Regional Support**: State-specific holidays
- ✅ **Individual Management**: Personal leave tracking

### Assignment Improvements
- ✅ **Holiday-Aware**: No assignments to unavailable agents
- ✅ **Time-Based**: Respects partial day leaves
- ✅ **Fallback Logic**: Assigns to available agents only
- ✅ **Load Balancing**: Distributes work among available agents

## 🔮 Future Enhancements

### Planned Features
- **Recurring Holidays**: Automatic yearly holidays
- **Holiday Templates**: Predefined holiday sets
- **Bulk Operations**: Mass holiday management
- **Calendar Integration**: External calendar sync
- **Holiday Analytics**: Detailed reporting
- **Mobile Support**: Mobile holiday management

---

## 🎯 **Ready to Use!**

Your Holiday Calendar Management System is now fully operational with:

- ✅ **Indian National Holidays** (2024-2025)
- ✅ **Individual Agent Holidays**
- ✅ **Holiday-Aware Assignment**
- ✅ **Management UI**
- ✅ **API Support**

**Next Steps:**
1. Run `python setup_indian_holidays.py`
2. Restart backend: `python main.py`
3. Access `/agents` page
4. Click agent names to manage holidays
5. Test holiday-aware assignment

**Your support team now has comprehensive holiday management! 🎉**
