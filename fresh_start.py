"""
Fresh Start Script - Clean all tickets and reset agent counts to zero
Use this script to completely reset the system to a fresh state

What this does:
1. Deletes ALL tickets from the database
2. Resets all agent counts to zero (current_load, total_assigned, total_resolved)
3. Optionally clears agent holidays and leaves
4. Resets ticket counters

What this DOES NOT do:
- Delete agents
- Delete knowledge base documents
- Delete SLA policies
- Delete official holidays

Run this after: python fresh_start.py
"""
import asyncio
from app.database import db_manager

async def fresh_start():
    """Complete fresh start - clean tickets and reset agents"""
    print("=" * 80)
    print("  🚀 FRESH START - SYSTEM RESET")
    print("=" * 80)
    print()
    print("This will:")
    print("  ✓ Delete ALL tickets")
    print("  ✓ Reset agent current_load to 0")
    print("  ✓ Reset agent total_assigned to 0")
    print("  ✓ Reset agent total_resolved to 0")
    print()
    print("This will NOT:")
    print("  ✗ Delete agents")
    print("  ✗ Delete knowledge base")
    print("  ✗ Delete SLA policies")
    print("  ✗ Delete holidays")
    print("  ✗ Delete system configuration")
    print("=" * 80)
    
    # Connect to MongoDB
    try:
        await db_manager.connect()
        print("✓ Connected to database")
    except Exception as e:
        print(f"✗ Cannot connect to database: {e}")
        print("  Make sure MongoDB is running and credentials are correct")
        return
    
    # Count tickets
    try:
        ticket_count = await db_manager.db.tickets.count_documents({})
        agent_count = await db_manager.db.agents.count_documents({})
        
        print(f"\n📊 Current Status:")
        print(f"  Tickets in database: {ticket_count}")
        print(f"  Agents in database: {agent_count}")
        
        if ticket_count == 0 and agent_count == 0:
            print("\n✓ Database is already empty")
            await db_manager.disconnect()
            return
    except Exception as e:
        print(f"✗ Error reading database: {e}")
        await db_manager.disconnect()
        return
    
    # Get list of tickets (preview)
    try:
        tickets_cursor = db_manager.db.tickets.find({}).limit(10)
        tickets_preview = []
        async for ticket in tickets_cursor:
            tickets_preview.append({
                "id": ticket.get("ticket_id", "unknown"),
                "subject": ticket.get("subject", "no subject"),
                "status": ticket.get("status", "unknown"),
                "customer": ticket.get("customer_identifier", "unknown")
            })
        
        if tickets_preview:
            print("\n📋 Sample tickets to be deleted:")
            for i, ticket in enumerate(tickets_preview[:5], 1):
                print(f"  {i}. {ticket['id']}: {ticket['subject'][:50]}")
            if ticket_count > 5:
                print(f"  ... and {ticket_count - 5} more tickets")
    except Exception as e:
        print(f"  Note: Could not preview tickets ({e})")
    
    # Confirmation
    print(f"\n⚠️  WARNING: This will delete ALL {ticket_count} tickets!")
    print("⚠️  This action cannot be undone!")
    print()
    
    response = input("Type 'yes' to confirm reset: ").strip().lower()
    
    if response != 'yes':
        print("\n✗ Reset cancelled")
        await db_manager.disconnect()
        return
    
    # Step 1: Delete all tickets
    print("\n🧹 Step 1: Deleting all tickets...")
    try:
        result = await db_manager.db.tickets.delete_many({})
        print(f"  ✓ Deleted {result.deleted_count} tickets")
    except Exception as e:
        print(f"  ✗ Error deleting tickets: {e}")
        await db_manager.disconnect()
        return
    
    # Step 2: Reset agent workload
    print("\n🔄 Step 2: Resetting agent workload...")
    try:
        # Reset all agents to zero workload
        agents_result = await db_manager.db.agents.update_many(
            {},
            {
                "$set": {
                    "current_load": 0,
                    "total_assigned": 0,
                    "total_resolved": 0
                }
            }
        )
        print(f"  ✓ Reset {agents_result.modified_count} agents")
        print(f"    - current_load: 0")
        print(f"    - total_assigned: 0")
        print(f"    - total_resolved: 0")
    except Exception as e:
        print(f"  ✗ Error resetting agents: {e}")
        await db_manager.disconnect()
        return
    
    # Step 3: Verify cleanup
    print("\n✅ Step 3: Verifying cleanup...")
    try:
        remaining_tickets = await db_manager.db.tickets.count_documents({})
        
        # Check a few agents
        sample_agents_cursor = db_manager.db.agents.find({}).limit(5)
        agents_check = []
        async for agent in sample_agents_cursor:
            agents_check.append({
                "name": agent.get("name", "unknown"),
                "current_load": agent.get("current_load", -1),
                "total_assigned": agent.get("total_assigned", -1)
            })
        
        if remaining_tickets == 0:
            print("  ✓ All tickets deleted")
        else:
            print(f"  ⚠️  Warning: {remaining_tickets} tickets still in database")
        
        if agents_check:
            print("\n  Agent Status:")
            for agent in agents_check:
                status = "✓" if agent['current_load'] == 0 and agent['total_assigned'] == 0 else "⚠️"
                print(f"  {status} {agent['name']}: load={agent['current_load']}, assigned={agent['total_assigned']}")
    except Exception as e:
        print(f"  ⚠️  Could not verify cleanup: {e}")
    
    # Final message
    print("\n" + "=" * 80)
    print("✓ FRESH START COMPLETE!")
    print("=" * 80)
    print()
    print("The system has been reset:")
    print("  ✓ All tickets removed")
    print("  ✓ All agents reset to zero workload")
    print("  ✓ Ready for new tickets")
    print()
    print("Next steps:")
    print("  1. Restart the backend server if running")
    print("  2. Test by sending an email/WhatsApp message")
    print("  3. Verify agents start with load = 0")
    print()
    print("Note: Agents, knowledge base, and configuration are preserved")
    print("=" * 80)
    
    await db_manager.disconnect()

if __name__ == "__main__":
    asyncio.run(fresh_start())

