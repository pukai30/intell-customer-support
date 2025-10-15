"""
Create sample airline support agents with tier system
Run this script to populate the database with airline agents
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.database import db_manager, Agent
from datetime import datetime

# Airline Support Agents (with tiers for escalation)
AIRLINE_AGENTS = [
    {
        "agent_id": "airline_agent_001",
        "name": "Lisa Martinez",
        "email": "lisa.martinez@skyhigh.com",
        "skills": ["booking", "cancellation", "refund", "check-in"],
        "skill_levels": {
            "booking": "expert",
            "cancellation": "advanced",
            "refund": "expert",
            "check-in": "expert"
        },
        "is_active": True,
        "tier": 0,  # L1 - Junior agent
        "handles_escalations": False,
        "domain": "AIRLINE",
        "max_concurrent_tickets": 15,
        "channels": ["email", "chat"]
    },
    {
        "agent_id": "airline_agent_002",
        "name": "Carlos Rivera",
        "email": "carlos.rivera@skyhigh.com",
        "skills": ["baggage", "delays", "compensation", "special-assistance"],
        "skill_levels": {
            "baggage": "advanced",
            "delays": "advanced",
            "compensation": "intermediate",
            "special-assistance": "expert"
        },
        "is_active": True,
        "tier": 0,  # L1 - Junior agent
        "handles_escalations": False,
        "domain": "AIRLINE",
        "max_concurrent_tickets": 12,
        "channels": ["email", "sms", "whatsapp"]
    },
    {
        "agent_id": "airline_agent_003",
        "name": "Amy Chen",
        "email": "amy.chen@skyhigh.com",
        "skills": ["seat-selection", "upgrades", "loyalty", "miles"],
        "skill_levels": {
            "seat-selection": "expert",
            "upgrades": "expert",
            "loyalty": "expert",
            "miles": "expert"
        },
        "is_active": True,
        "tier": 0,  # L1 - Junior agent
        "handles_escalations": False,
        "domain": "AIRLINE",
        "max_concurrent_tickets": 14,
        "channels": ["email", "chat"]
    },
    {
        "agent_id": "airline_agent_004",
        "name": "Marcus Johnson",
        "email": "marcus.johnson@skyhigh.com",
        "skills": ["international", "visa", "customs", "documentation"],
        "skill_levels": {
            "international": "advanced",
            "visa": "intermediate",
            "customs": "advanced",
            "documentation": "advanced"
        },
        "is_active": True,
        "tier": 0,  # L1 - Junior agent
        "handles_escalations": False,
        "domain": "AIRLINE",
        "max_concurrent_tickets": 10,
        "channels": ["email"]
    },
    # TIER 1 - Senior Agents (Handle escalations)
    {
        "agent_id": "airline_supervisor_001",
        "name": "Jennifer Wong",
        "email": "jennifer.wong@skyhigh.com",
        "skills": ["booking", "cancellation", "refund", "delays", "compensation", "complex-issues"],
        "skill_levels": {
            "booking": "expert",
            "cancellation": "expert",
            "refund": "expert",
            "delays": "expert",
            "compensation": "expert",
            "complex-issues": "expert"
        },
        "is_active": True,
        "tier": 1,  # L2 - Senior agent
        "handles_escalations": True,
        "domain": "AIRLINE",
        "max_concurrent_tickets": 10,
        "channels": ["email", "chat", "phone"]
    },
    {
        "agent_id": "airline_supervisor_002",
        "name": "David Thompson",
        "email": "david.thompson@skyhigh.com",
        "skills": ["baggage", "special-assistance", "international", "vip-service"],
        "skill_levels": {
            "baggage": "expert",
            "special-assistance": "expert",
            "international": "expert",
            "vip-service": "expert"
        },
        "is_active": True,
        "tier": 1,  # L2 - Senior agent
        "handles_escalations": True,
        "domain": "AIRLINE",
        "max_concurrent_tickets": 8,
        "channels": ["email", "chat", "phone"]
    },
    # TIER 2 - Expert Agents
    {
        "agent_id": "airline_expert_001",
        "name": "Rachel Kim",
        "email": "rachel.kim@skyhigh.com",
        "skills": ["all-airline-issues", "legal", "disputes", "vip-service", "crisis-management"],
        "skill_levels": {
            "all-airline-issues": "expert",
            "legal": "expert",
            "disputes": "expert",
            "vip-service": "expert",
            "crisis-management": "expert"
        },
        "is_active": True,
        "tier": 2,  # L3 - Expert agent
        "handles_escalations": True,
        "domain": "AIRLINE",
        "max_concurrent_tickets": 5,
        "channels": ["email", "chat", "phone"]
    },
    # TIER 3 - Manager
    {
        "agent_id": "airline_manager_001",
        "name": "Robert Anderson",
        "email": "robert.anderson@skyhigh.com",
        "skills": ["all-airline-issues", "legal", "executive-resolution", "crisis-management"],
        "skill_levels": {
            "all-airline-issues": "expert",
            "legal": "expert",
            "executive-resolution": "expert",
            "crisis-management": "expert"
        },
        "is_active": True,
        "tier": 3,  # L4 - Manager
        "handles_escalations": True,
        "domain": "AIRLINE",
        "max_concurrent_tickets": 3,
        "channels": ["email", "phone"]
    }
]


async def setup_agents():
    """Create airline support agents in the database"""
    print("=" * 80)
    print("  SETTING UP AIRLINE SUPPORT AGENTS")
    print("=" * 80)
    print()
    
    try:
        await db_manager.connect()
        
        success_count = 0
        update_count = 0
        
        for agent_data in AIRLINE_AGENTS:
            try:
                # Check if agent already exists
                existing_agent = await db_manager.get_agent(agent_data["agent_id"])
                
                if existing_agent:
                    print(f"⚠️  Agent {agent_data['name']} already exists - updating")
                    await db_manager.update_agent(agent_data["agent_id"], agent_data)
                    update_count += 1
                else:
                    agent = Agent(**agent_data)
                    await db_manager.create_agent(agent)
                    print(f"✅ Created: {agent_data['name']} (Tier {agent_data['tier']})")
                    success_count += 1
                    
            except Exception as e:
                print(f"❌ Error creating agent {agent_data['name']}: {e}")
        
        print()
        print("=" * 80)
        print(f"✅ Setup Complete!")
        print(f"   - Created: {success_count} agents")
        print(f"   - Updated: {update_count} agents")
        print("=" * 80)
        print()
        print("📊 Agent Summary:")
        print(f"   - Tier 0 (L1): 4 junior agents")
        print(f"   - Tier 1 (L2): 2 senior agents")
        print(f"   - Tier 2 (L3): 1 expert agent")
        print(f"   - Tier 3 (L4): 1 manager")
        print()
        print("🎯 Skills Coverage:")
        print("   - Booking & Cancellation: Lisa, Jennifer")
        print("   - Baggage & Delays: Carlos, David")
        print("   - Seats & Upgrades: Amy")
        print("   - International Travel: Marcus, David")
        print("   - Complex/VIP Issues: Rachel, Robert")
        print()
        
        await db_manager.disconnect()
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(setup_agents())

