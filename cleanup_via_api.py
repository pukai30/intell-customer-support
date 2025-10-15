"""
Clean up all tickets via API
Simple script that doesn't require database dependencies
"""
import requests

API_URL = "http://localhost:8000"

def cleanup_tickets():
    """Delete all tickets via API"""
    print("=" * 80)
    print("  CLEANING UP TICKETS VIA API")
    print("=" * 80)
    
    try:
        # Get all tickets
        response = requests.get(f"{API_URL}/api/tickets")
        if response.status_code != 200:
            print(f"✗ Error getting tickets: {response.status_code}")
            return
        
        tickets = response.json().get("tickets", [])
        count = len(tickets)
        
        print(f"\nFound {count} existing tickets")
        
        if count == 0:
            print("✓ No tickets to clean up")
            return
        
        # Show ticket summaries
        print("\nTickets to be deleted:")
        for ticket in tickets[:10]:  # Show first 10
            print(f"  - {ticket['ticket_id']}: {ticket.get('subject', 'No subject')}")
        if count > 10:
            print(f"  ... and {count - 10} more tickets")
        
        # Ask for confirmation
        print(f"\n⚠️  WARNING: This will delete ALL {count} tickets!")
        print("This action cannot be undone.")
        response_input = input("\nDo you want to continue? (yes/no): ")
        
        if response_input.lower() != 'yes':
            print("\n✗ Cleanup cancelled")
            return
        
        # Note: We don't have a bulk delete API, so we'll use MongoDB directly
        print("\n⚠️  Please use MongoDB directly to delete tickets:")
        print("\n  mongosh")
        print("  use customer_support")
        print("  db.tickets.deleteMany({})")
        print("  db.agents.updateMany({}, {$set: {current_load: 0, total_assigned: 0, total_resolved: 0}})")
        print("  exit")
        
        print("\nOr restart backend and it will handle cleanup on next restart")
        
    except requests.exceptions.ConnectionError:
        print("✗ Error: Cannot connect to backend API")
        print("  Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    cleanup_tickets()

