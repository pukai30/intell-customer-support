# Twilio WhatsApp Connection Test

This guide explains how to test the Twilio WhatsApp integration for the Intelligent Customer Support System.

## Prerequisites

1. **Twilio Account**: You need an active Twilio account with WhatsApp messaging capability
2. **Environment Variables**: Your `.env` file should have Twilio credentials configured

## Required .env Configuration

Make sure your `.env` file contains:

```env
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+14155238886
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

## Running the Test

### Option 1: Quick Connection Test

Run the test script to verify Twilio connection:

```bash
python test_twilio_whatsapp_connection.py
```

This will:
- ✅ Check if Twilio credentials are configured
- ✅ Test connection to Twilio API
- ✅ Fetch account information
- ✅ Check for recent WhatsApp messages
- ✅ Verify message handling capabilities

### Option 2: Test Send WhatsApp Message

The script can also test sending a WhatsApp message:

```bash
python test_twilio_whatsapp_connection.py
```

When prompted, choose to send a test message. You'll need:
- A valid WhatsApp number (e.g., +1234567890)
- The number must have joined your Twilio WhatsApp sandbox

## Webhook Configuration

To receive WhatsApp messages, configure the webhook in Twilio Console:

### Steps:

1. **Go to Twilio Console**: https://console.twilio.com
2. **Navigate to**: Messaging → Settings → WhatsApp Sandbox
3. **Set Webhook URL**: `http://your-server:8000/api/webhooks/whatsapp`
4. **Save** the configuration

### For Local Development:

1. **Install ngrok**: `npm install -g ngrok` or download from ngrok.com
2. **Start ngrok**: `ngrok http 8000`
3. **Copy the URL**: e.g., `https://abc123.ngrok.io`
4. **Set webhook in Twilio**: `https://abc123.ngrok.io/api/webhooks/whatsapp`

## Testing Workflow

### 1. Test Connection

```bash
python test_twilio_whatsapp_connection.py
```

Expected output:
```
================================================================================
  TESTING TWILIO WHATSAPP CONNECTION
================================================================================

📋 Configuration Check:
   Twilio Account SID: ✓ Set
   Twilio Auth Token: ✓ Set
   Twilio WhatsApp Number: whatsapp:+14155238886
   Twilio Phone Number: +14155238886

🔌 Connecting to Twilio...
   → Fetching account information...
   ✓ Connected to account: Your Account Name

📱 Checking WhatsApp messages...
   ℹ️  No recent messages found

🔔 Testing message handling capabilities...
   ✓ Messages API accessible
   ✓ Can list messages
   ✓ Can send messages

💾 Testing database connection...
   ✓ Database configuration loaded

================================================================================
✓ TWILIO WHATSAPP CONNECTION TEST PASSED
================================================================================
```

### 2. Test Receiving Messages

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Send a WhatsApp message** to your Twilio WhatsApp number:
   - From your WhatsApp: Send "join <your-sandbox-keyword>" to join
   - Then send a message like: "I need help with my password"

3. **Check the logs** for incoming message processing:
   ```
   ✓ Processing WhatsApp message from whatsapp:+1234567890
   ✓ Auto-responded to WhatsApp
   ```

### 3. Test Sending Messages

Run the test with send option:
```bash
python test_twilio_whatsapp_connection.py
```

Choose 'y' when prompted, then enter a recipient number.

## Troubleshooting

### Error: "Twilio credentials not configured"

**Solution**: Make sure your `.env` file has:
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
```

### Error: "Authentication failed"

**Solution**: 
- Verify the Account SID and Auth Token are correct
- Check if your Twilio account is active
- Ensure no extra spaces in the credentials

### Error: "WhatsApp number not valid"

**Solution**:
- Use the Twilio Sandbox WhatsApp number: `whatsapp:+14155238886`
- Or configure your production WhatsApp number in Twilio Console

### No messages appearing

**Solution**:
1. Check if webhook is configured in Twilio Console
2. Verify webhook URL is accessible
3. Check server logs for incoming webhooks
4. Ensure recipient has joined the WhatsApp sandbox

## Twilio WhatsApp Sandbox

For testing, you can use Twilio's WhatsApp Sandbox:

1. **Go to Twilio Console** → Messaging → Settings → WhatsApp Sandbox
2. **Get your join code**: e.g., "join example-abcd"
3. **Have test users join**: Send the join code to `whatsapp:+1 415 523 8886`

## Production Setup

For production WhatsApp messaging:

1. **Apply for WhatsApp Business API** in Twilio Console
2. **Get approved** by Twilio (usually takes 1-2 days)
3. **Configure your business phone number**
4. **Update webhook URL** to production URL
5. **Test with real WhatsApp users**

## API Endpoints

The application uses these endpoints for WhatsApp:

- **Webhook**: `POST /api/webhooks/whatsapp` - Receives incoming messages
- **Send**: Uses Twilio API to send WhatsApp messages to customers

## Integration Flow

```
Customer WhatsApp
       ↓
Twilio Webhook → /api/webhooks/whatsapp
       ↓
WhatsApp Integration → Process Message
       ↓
RAG System → Generate Response
       ↓
Send WhatsApp Message to Customer
```

## Support

For issues or questions:
1. Check Twilio Console for webhook logs
2. Review application logs for errors
3. Verify environment variables are set correctly
4. Check Twilio account status

