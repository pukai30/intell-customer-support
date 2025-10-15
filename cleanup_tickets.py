"""
Clean up all tickets from the database
Use this to start fresh with new email configuration
"""
import asyncio
from app.database import db_manager

async def cleanup_tickets():
    """Delete all tickets from MongoDB"""
    print("=" * 80)
    print("  CLEANING UP TICKETS")
    print("=" * 80)
    
    # Connect to MongoDB
    await db_manager.connect()
    
    # Count existing tickets
    count = await db_manager.db.tickets.count_documents({})
    print(f"\nFound {count} existing tickets")
    
    if count == 0:
        print("✓ No tickets to clean up")
        await db_manager.disconnect()
        return
    
    # Ask for confirmation
    print(f"\n⚠️  WARNING: This will delete ALL {count} tickets!")
    print("This action cannot be undone.")
    response = input("\nDo you want to continue? (yes/no): ")
    
    if response.lower() != 'yes':
        print("\n✗ Cleanup cancelled")
        await db_manager.disconnect()
        return
    
    # Delete all tickets
    result = await db_manager.db.tickets.delete_many({})
    print(f"\n✓ Deleted {result.deleted_count} tickets")
    
    # Also reset agent loads to 0
    agents_updated = await db_manager.db.agents.update_many(
        {},
        {
            "$set": {
                "current_load": 0,
                "total_assigned": 0,
                "total_resolved": 0
            }
        }
    )
    print(f"✓ Reset {agents_updated.modified_count} agents' workload to 0")
    
    print("\n" + "=" * 80)
    print("✓ Cleanup complete! Database is ready for new tickets.")
    print("=" * 80)
    
    await db_manager.disconnect()

if __name__ == "__main__":
    asyncio.run(cleanup_tickets())

