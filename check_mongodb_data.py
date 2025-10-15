"""
Diagnostic script to check MongoDB data
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.database import db_manager


async def check_data():
    """Check what data exists in MongoDB"""
    print("=" * 80)
    print("  MONGODB DATA CHECK")
    print("=" * 80)
    print()
    
    try:
        await db_manager.connect()
        
        # Check Knowledge Base
        print("📚 KNOWLEDGE BASE:")
        print("-" * 80)
        kb_count = await db_manager.db.knowledge.count_documents({})
        print(f"Total documents: {kb_count}")
        
        if kb_count > 0:
            # Get first few documents
            cursor = db_manager.db.knowledge.find({}).limit(5)
            async for doc in cursor:
                print(f"  - {doc.get('title', 'Untitled')} (Category: {doc.get('category', 'None')})")
        else:
            print("  ⚠️  No knowledge documents found!")
            print("  → Run: python it_support_knowledge_mnc.py")
        
        print()
        
        # Check Agents
        print("👥 AGENTS:")
        print("-" * 80)
        agents_count = await db_manager.db.agents.count_documents({})
        print(f"Total agents: {agents_count}")
        
        if agents_count > 0:
            cursor = db_manager.db.agents.find({}).limit(10)
            async for agent in cursor:
                print(f"  - {agent.get('name', 'Unknown')} ({agent.get('email', 'no-email')}) - Tier {agent.get('tier', 0)}")
        else:
            print("  ⚠️  No agents found!")
            print("  → Run: python setup_sample_agents.py")
        
        print()
        
        # Check Tickets
        print("🎫 TICKETS:")
        print("-" * 80)
        tickets_count = await db_manager.db.tickets.count_documents({})
        print(f"Total tickets: {tickets_count}")
        
        if tickets_count > 0:
            open_count = await db_manager.db.tickets.count_documents({"status": "open"})
            closed_count = await db_manager.db.tickets.count_documents({"status": "closed"})
            print(f"  - Open: {open_count}")
            print(f"  - Closed: {closed_count}")
        
        print()
        
        # Check SLA Policies
        print("⚙️ SLA POLICIES:")
        print("-" * 80)
        sla_count = await db_manager.db.sla_policies.count_documents({})
        print(f"Total SLA policies: {sla_count}")
        
        if sla_count > 0:
            cursor = db_manager.db.sla_policies.find({}).limit(10)
            async for policy in cursor:
                print(f"  - {policy.get('name', 'Unknown')} (ID: {policy.get('policy_id', 'None')})")
        else:
            print("  ⚠️  No SLA policies found!")
            print("  → Run: python setup_sla_policies.py")
        
        print()
        print("=" * 80)
        print("✅ Database check complete!")
        print("=" * 80)
        
        await db_manager.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(check_data())

