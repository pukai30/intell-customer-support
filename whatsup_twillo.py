from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Your Account SID and Auth Token from .env file
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

# Verify credentials are loaded
if not account_sid or not auth_token:
    print("❌ ERROR: Twilio credentials not found in .env file")
    print("Please add to .env file:")
    print("TWILIO_ACCOUNT_SID=your_account_sid")
    print("TWILIO_AUTH_TOKEN=your_auth_token")
    exit(1)

print(f"✓ Loaded Twilio Account SID: {account_sid[:10]}...")
print(f"✓ Loaded Twilio Auth Token: {auth_token[:10]}...")

client = Client(account_sid, auth_token)

# The WhatsApp Sandbox number (or your approved Twilio number)
# prefixed with "whatsapp:"
from_whatsapp_number = 'whatsapp:+14155238886'  # Your Twilio WhatsApp number


def read_whatsapp_messages(limit=10):
    """Read recent WhatsApp messages received by your Twilio WhatsApp number"""
    try:
        print("\n" + "=" * 80)
        print("  READING WHATSAPP MESSAGES FROM TWILIO")
        print("=" * 80)
        
        # Get messages sent TO your WhatsApp number (incoming messages)
        messages = client.messages.list(
            to=from_whatsapp_number,
            limit=limit
        )
        
        if not messages:
            print("   ℹ️  No messages found for your WhatsApp number")
            print(f"   Listening on: {from_whatsapp_number}")
        else:
            print(f"\n   ✓ Found {len(messages)} message(s) for {from_whatsapp_number}\n")
            
            for i, msg in enumerate(messages, 1):
                print(f"   Message #{i}:")
                print(f"      From: {msg.from_}")
                print(f"      To: {msg.to}")
                print(f"      Date: {msg.date_sent}")
                print(f"      Status: {msg.status}")
                print(f"      SID: {msg.sid}")
                print()
                print(f"      📝 Message Body:")
                print(f"      {'-' * 70}")
                print(f"      {msg.body}")
                print(f"      {'-' * 70}")
                print()
        
        return messages
        
    except Exception as e:
        print(f"\n   ✗ Error reading messages: {e}")
        return []


def send_whatsapp_message(to_number, message_body):
    """Send a WhatsApp message"""
    try:
        print("\n" + "=" * 80)
        print("  SENDING WHATSAPP MESSAGE")
        print("=" * 80)
        
        # Ensure to_number is in correct format
        if not to_number.startswith('whatsapp:'):
            to_number = f'whatsapp:{to_number}'
        
        print(f"\n   From: {from_whatsapp_number}")
        print(f"   To: {to_number}")
        print(f"   Message: {message_body}\n")
        
        message = client.messages.create(
            from_=from_whatsapp_number,
            body=message_body,
            to=to_number
        )
        
        print(f"   ✓ Message sent successfully!")
        print(f"   Message SID: {message.sid}")
        print(f"   Message status: {message.status}\n")
        
        return message
        
    except Exception as e:
        print(f"\n   ✗ Error sending message: {e}")
        return None


def delete_all_whatsapp_messages(limit=100):
    """Delete all WhatsApp messages from Twilio"""
    try:
        print("\n" + "=" * 80)
        print("  DELETING ALL WHATSAPP MESSAGES")
        print("=" * 80)
        
        # Get all messages (limit can be adjusted)
        messages = client.messages.list(
            to=from_whatsapp_number,
            limit=limit
        )
        
        if not messages:
            print("   ℹ️  No messages found to delete")
            print(f"   Listening on: {from_whatsapp_number}")
            return 0
        
        print(f"\n   Found {len(messages)} message(s) to delete...\n")
        
        deleted_count = 0
        failed_count = 0
        
        for i, msg in enumerate(messages, 1):
            try:
                # Delete the message
                client.messages(msg.sid).delete()
                deleted_count += 1
                print(f"   [{i}/{len(messages)}] ✓ Deleted message SID: {msg.sid[:20]}...")
                
            except Exception as del_error:
                failed_count += 1
                print(f"   [{i}/{len(messages)}] ✗ Failed to delete {msg.sid[:20]}...: {del_error}")
        
        print(f"\n   {'-' * 80}")
        print(f"   Summary:")
        print(f"   ✓ Successfully deleted: {deleted_count}")
        print(f"   ✗ Failed to delete: {failed_count}")
        print(f"   Total processed: {len(messages)}\n")
        
        return deleted_count
        
    except Exception as e:
        print(f"\n   ✗ Error deleting messages: {e}")
        import traceback
        traceback.print_exc()
        return 0


# Example usage
if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "read":
        # Read messages mode
        read_whatsapp_messages()
    
    elif len(sys.argv) > 1 and sys.argv[1] == "send":
        # Send message mode
        to_number = 'whatsapp:+919830312959'  # Recipient number
        message_body = "Hello from Twilio WhatsApp! This is a test message."
        send_whatsapp_message(to_number, message_body)
    
    elif len(sys.argv) > 1 and sys.argv[1] == "delete":
        # Delete all messages mode
        delete_all_whatsapp_messages()
    
    else:
        # Interactive mode
        print("\n" + "=" * 80)
        print("  TWILIO WHATSAPP TEST")
        print("=" * 80)
        
        print("\nChoose an option:")
        print("1. Read incoming WhatsApp messages")
        print("2. Send a WhatsApp message")
        print("3. Both (read, then send)")
        print("4. Delete all WhatsApp messages")
        
        choice = input("\nEnter choice (1/2/3/4): ").strip()
        
        if choice == "1":
            read_whatsapp_messages()
        
        elif choice == "2":
            to_number = input("\nEnter recipient number (e.g., +919830312959): ").strip()
            message_body = input("Enter message to send: ").strip()
            
            if to_number and message_body:
                send_whatsapp_message(to_number, message_body)
            else:
                print("Both recipient and message are required")
        
        elif choice == "3":
            read_whatsapp_messages()
            
            print("\n" + "-" * 80)
            to_number = input("\nEnter recipient number to send test message (or press Enter to skip): ").strip()
            
            if to_number:
                message_body = "Hello! This is a test message from the Intelligent Customer Support System."
                send_whatsapp_message(to_number, message_body)
        
        elif choice == "4":
            # Confirmation for delete operation
            print("\n⚠️  WARNING: This will delete ALL WhatsApp messages!")
            confirm = input("Are you sure? (type 'yes' to confirm): ").strip().lower()
            
            if confirm == 'yes':
                delete_all_whatsapp_messages()
            else:
                print("Delete operation cancelled")
        
        else:
            print("Invalid choice")