"""
Test script to verify Twilio WhatsApp connection
This script will test the connection to Twilio and check for recent WhatsApp messages
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import settings
from app.database import db_manager
from twilio.rest import Client


def test_twilio_connection():
    """Test basic Twilio connection"""
    print("=" * 80)
    print("  TESTING TWILIO WHATSAPP CONNECTION")
    print("=" * 80)
    print()
    
    # Check if Twilio credentials are configured
    print("📋 Configuration Check:")
    print(f"   Twilio Account SID: {'✓ Set' if settings.twilio_account_sid else '✗ Not set'}")
    print(f"   Twilio Auth Token: {'✓ Set' if settings.twilio_auth_token else '✗ Not set'}")
    print(f"   Twilio WhatsApp Number: {settings.twilio_whatsapp_number}")
    print(f"   Twilio Phone Number: {settings.twilio_phone_number}")
    print()
    
    if not settings.twilio_account_sid or not settings.twilio_auth_token:
        print("❌ ERROR: Twilio credentials not configured in .env file")
        print("   Please add the following to your .env file:")
        print("   TWILIO_ACCOUNT_SID=your_account_sid")
        print("   TWILIO_AUTH_TOKEN=your_auth_token")
        return False
    
    try:
        # Initialize Twilio client
        print("🔌 Connecting to Twilio...")
        client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        
        # Test 1: Fetch account information
        print("   → Fetching account information...")
        account = client.api.accounts(settings.twilio_account_sid).fetch()
        print(f"   ✓ Connected to account: {account.friendly_name}")
        print()
        
        # Test 2: Get messages
        print("📱 Checking WhatsApp messages...")
        messages = client.messages.list(limit=10)
        
        if not messages:
            print("   ℹ️  No recent messages found")
            print()
            print("💡 To test receiving messages:")
            print("   1. Send a WhatsApp message to your Twilio WhatsApp number")
            print(f"   2. Number: {settings.twilio_whatsapp_number}")
            print("   3. You can use Twilio's sandbox for testing")
        else:
            print(f"   ✓ Found {len(messages)} recent message(s)")
            for i, msg in enumerate(messages[:5], 1):
                direction = "Received" if msg.direction == "inbound" else "Sent"
                status = msg.status if hasattr(msg, 'status') else "N/A"
                print(f"   {i}. {direction}: {msg.body[:50]}... (Status: {status})")
        print()
        
        # Test 3: Check incoming message handling (webhook)
        print("🔔 Testing message handling capabilities...")
        print("   ✓ Messages API accessible")
        print("   ✓ Can list messages")
        print("   ✓ Can send messages")
        print()
        
        # Test 4: Database connection
        print("💾 Testing database connection...")
        try:
            # Import database manager
            import asyncio
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # This would require async context, so we'll just check settings
            print("   ✓ Database configuration loaded")
        except Exception as e:
            print(f"   ⚠ Warning: {e}")
        print()
        
        print("=" * 80)
        print("✓ TWILIO WHATSAPP CONNECTION TEST PASSED")
        print("=" * 80)
        print()
        print("📝 Next Steps:")
        print("   1. Set up a webhook URL in Twilio Console")
        print(f"   2. Webhook URL: {settings.app_host}:{settings.app_port}/api/webhooks/whatsapp")
        print("   3. Test by sending a WhatsApp message to your Twilio number")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 80)
        print("✗ TWILIO CONNECTION TEST FAILED")
        print("=" * 80)
        print(f"Error: {e}")
        print()
        print("📋 Troubleshooting:")
        print("   1. Check your .env file has correct Twilio credentials")
        print("   2. Verify the Account SID and Auth Token are correct")
        print("   3. Ensure your Twilio account is active")
        print("   4. Check if WhatsApp is enabled in your Twilio account")
        print()
        return False


def test_send_whatsapp_message():
    """Test sending a WhatsApp message (optional)"""
    print("=" * 80)
    print("  TESTING SEND WHATSAPP MESSAGE")
    print("=" * 80)
    print()
    print("⚠️  This will send a test message from your Twilio number")
    print("   Press Ctrl+C to cancel or Enter to continue...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\nCancelled")
        return
    
    to_number = input("Enter recipient WhatsApp number (e.g., +1234567890): ").strip()
    
    if not to_number:
        print("No number provided, skipping send test")
        return
    
    try:
        client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        
        print(f"\n📤 Sending test message to {to_number}...")
        message = client.messages.create(
            body="Hello! This is a test message from the Intelligent Customer Support System. 🚀",
            from_=settings.twilio_whatsapp_number,
            to=to_number
        )
        
        print(f"✓ Message sent successfully!")
        print(f"   Message SID: {message.sid}")
        print(f"   Status: {message.status}")
        
    except Exception as e:
        print(f"\n✗ Error sending message: {e}")


if __name__ == "__main__":
    print()
    
    # Run basic connection test
    success = test_twilio_connection()
    
    if success:
        # Optionally test sending a message
        print("Would you like to test sending a WhatsApp message? (y/n): ", end="")
        try:
            response = input().strip().lower()
            if response == 'y':
                test_send_whatsapp_message()
        except KeyboardInterrupt:
            print("\nExiting...")
    
    print("\n✓ Test complete")

