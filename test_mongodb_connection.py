"""
Test MongoDB Connection and Ticket Storage
Simple diagnostic script to check if tickets are being saved
"""
import asyncio
from app.database import db_manager, SupportTicket, ConversationMessage
from datetime import datetime

async def test_connection():
    """Test MongoDB connection and ticket creation"""
    print("=" * 80)
    print("  TESTING MONGODB CONNECTION")
    print("=" * 80)
    
    try:
        # Connect to MongoDB
        print("\n1. Connecting to MongoDB...")
        await db_manager.connect()
        print("   ✓ Connected successfully!")
        
        # Check if database exists
        print("\n2. Checking database...")
        db_names = await db_manager.client.list_database_names()
        print(f"   Available databases: {db_names}")
        if "customer_support" in db_names:
            print("   ✓ customer_support database exists")
        else:
            print("   ⚠️ customer_support database NOT found (will be created)")
        
        # Check collections
        print("\n3. Checking collections...")
        collections = await db_manager.db.list_collection_names()
        print(f"   Available collections: {collections}")
        
        # Count existing tickets
        print("\n4. Counting existing tickets...")
        ticket_count = await db_manager.db.tickets.count_documents({})
        print(f"   Found {ticket_count} existing tickets")
        
        # Try to create a test ticket
        print("\n5. Creating test ticket...")
        test_ticket = SupportTicket(
            ticket_id="TEST-12345",
            channel="test",
            customer_identifier="test@example.com",
            subject="Test Ticket",
            status="open"
        )
        
        # Delete if exists
        await db_manager.db.tickets.delete_one({"ticket_id": "TEST-12345"})
        
        # Create new
        result = await db_manager.create_ticket(test_ticket)
        print(f"   ✓ Test ticket created with ID: {result}")
        
        # Verify it was saved
        print("\n6. Verifying ticket was saved...")
        saved_ticket = await db_manager.get_ticket("TEST-12345")
        if saved_ticket:
            print(f"   ✓ Ticket retrieved successfully!")
            print(f"     - Ticket ID: {saved_ticket.ticket_id}")
            print(f"     - Customer: {saved_ticket.customer_identifier}")
            print(f"     - Subject: {saved_ticket.subject}")
        else:
            print("   ✗ ERROR: Ticket not found after creation!")
        
        # Add a message
        print("\n7. Adding message to ticket...")
        test_message = ConversationMessage(
            role="user",
            content="Test message",
            timestamp=datetime.utcnow()
        )
        await db_manager.add_message_to_ticket("TEST-12345", test_message)
        
        # Verify message was added
        updated_ticket = await db_manager.get_ticket("TEST-12345")
        if updated_ticket and len(updated_ticket.conversation) > 0:
            print(f"   ✓ Message added! Conversation has {len(updated_ticket.conversation)} message(s)")
        else:
            print("   ✗ ERROR: Message not added!")
        
        # Check all tickets
        print("\n8. Listing all tickets...")
        all_tickets = await db_manager.get_all_tickets()
        print(f"   Found {len(all_tickets)} total tickets")
        for ticket in all_tickets[:5]:  # Show first 5
            print(f"     - {ticket.ticket_id}: {ticket.subject} ({ticket.customer_identifier})")
        
        # Cleanup test ticket
        print("\n9. Cleaning up test ticket...")
        await db_manager.db.tickets.delete_one({"ticket_id": "TEST-12345"})
        print("   ✓ Test ticket deleted")
        
        print("\n" + "=" * 80)
        print("  ✓ ALL TESTS PASSED!")
        print("  MongoDB is working correctly!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        print("\nPossible issues:")
        print("  1. MongoDB is not running (start with: mongod)")
        print("  2. Connection string is incorrect")
        print("  3. Database permissions issue")
        import traceback
        traceback.print_exc()
    
    finally:
        await db_manager.disconnect()

if __name__ == "__main__":
    asyncio.run(test_connection())

