"""
Sample script to populate the knowledge base with example data
Run this after starting the application to add sample knowledge
"""
import requests
import json

API_URL = "http://localhost:8000"

sample_knowledge = [
    {
        "title": "Account Creation",
        "content": """
To create a new account:
1. Visit our website and click 'Sign Up'
2. Enter your email address and create a strong password
3. Verify your email by clicking the link sent to your inbox
4. Complete your profile information
5. You're ready to start using our service!

Note: Passwords must be at least 8 characters and include letters, numbers, and special characters.
        """,
        "category": "account",
        "tags": ["signup", "registration", "new account"]
    },
    {
        "title": "Password Reset",
        "content": """
If you've forgotten your password:
1. Go to the login page
2. Click 'Forgot Password' link
3. Enter your registered email address
4. Check your email for a password reset link
5. Click the link and create a new password
6. Log in with your new password

The reset link expires in 24 hours. If it expires, request a new one.
        """,
        "category": "account",
        "tags": ["password", "reset", "security", "login"]
    },
    {
        "title": "Business Hours",
        "content": """
Our customer support team is available:
- Monday to Friday: 9:00 AM - 6:00 PM EST
- Saturday: 10:00 AM - 4:00 PM EST
- Sunday: Closed

For urgent issues outside business hours, you can:
- Use our 24/7 chatbot for instant help
- Send an email to support@company.com
- Leave a voicemail at 1-800-SUPPORT
        """,
        "category": "general",
        "tags": ["hours", "availability", "contact"]
    },
    {
        "title": "Payment Methods",
        "content": """
We accept the following payment methods:
- Credit Cards (Visa, MasterCard, American Express)
- Debit Cards
- PayPal
- Bank Transfer (for enterprise accounts)
- Cryptocurrency (Bitcoin, Ethereum)

All transactions are secured with 256-bit SSL encryption.
Payment processing is handled by our certified payment partner.
        """,
        "category": "billing",
        "tags": ["payment", "billing", "credit card", "paypal"]
    },
    {
        "title": "Subscription Plans",
        "content": """
We offer three subscription tiers:

1. Basic Plan ($9.99/month):
   - Up to 5 users
   - 10 GB storage
   - Email support
   - Basic features

2. Professional Plan ($29.99/month):
   - Up to 20 users
   - 100 GB storage
   - Priority email and chat support
   - Advanced features
   - API access

3. Enterprise Plan (Custom pricing):
   - Unlimited users
   - Unlimited storage
   - 24/7 dedicated support
   - All features
   - Custom integrations
   - SLA guarantee

Annual subscriptions get 20% discount!
        """,
        "category": "billing",
        "tags": ["subscription", "pricing", "plans", "upgrade"]
    },
    {
        "title": "Cancellation Policy",
        "content": """
You can cancel your subscription at any time:

1. Log into your account
2. Go to Settings > Subscription
3. Click 'Cancel Subscription'
4. Confirm cancellation

Important notes:
- You'll have access until the end of your billing period
- No refunds for partial months
- You can reactivate anytime
- Your data is retained for 30 days after cancellation
- After 30 days, all data is permanently deleted

Need help? Contact our retention team who may offer special deals.
        """,
        "category": "billing",
        "tags": ["cancel", "cancellation", "unsubscribe", "refund"]
    },
    {
        "title": "Data Export",
        "content": """
To export your data:

1. Navigate to Settings > Data Management
2. Click 'Export Data'
3. Select the data types you want to export:
   - User profiles
   - Messages
   - Files
   - Analytics
4. Choose format (JSON, CSV, or XML)
5. Click 'Start Export'
6. You'll receive a download link via email within 24 hours

Note: Large exports may take longer. Maximum export size is 10 GB per request.
        """,
        "category": "data",
        "tags": ["export", "data", "download", "backup"]
    },
    {
        "title": "Two-Factor Authentication",
        "content": """
Enable Two-Factor Authentication (2FA) for added security:

1. Go to Settings > Security
2. Click 'Enable 2FA'
3. Choose your preferred method:
   - Authenticator app (recommended)
   - SMS code
   - Email code
4. Follow the setup instructions
5. Save your backup codes in a safe place

With 2FA enabled, you'll need both your password and a second verification code to log in.

Supported authenticator apps:
- Google Authenticator
- Microsoft Authenticator
- Authy
        """,
        "category": "security",
        "tags": ["2fa", "security", "authentication", "mfa"]
    },
    {
        "title": "API Access",
        "content": """
API access is available for Professional and Enterprise plans.

Getting Started:
1. Go to Settings > Developer
2. Click 'Generate API Key'
3. Copy and securely store your API key
4. Review API documentation at docs.api.company.com

API Features:
- RESTful endpoints
- Rate limit: 1000 requests/hour (Pro), 10000/hour (Enterprise)
- JSON responses
- OAuth 2.0 authentication
- Webhooks support
- Comprehensive documentation

Need higher rate limits? Contact our Enterprise team.
        """,
        "category": "technical",
        "tags": ["api", "developer", "integration", "webhook"]
    },
    {
        "title": "Mobile App",
        "content": """
Our mobile app is available for iOS and Android:

Download:
- iOS: Search 'Company Name' in the App Store
- Android: Search 'Company Name' in the Google Play Store

Features:
- Full feature parity with web version
- Offline mode
- Push notifications
- Biometric login
- Dark mode

System Requirements:
- iOS 14.0 or later
- Android 8.0 or later

Having issues? Try:
1. Update to the latest version
2. Clear app cache
3. Reinstall the app
4. Contact mobile support team
        """,
        "category": "technical",
        "tags": ["mobile", "app", "ios", "android", "download"]
    }
]


def add_knowledge():
    """Add sample knowledge to the system"""
    print("Adding sample knowledge to the system...")
    print(f"API URL: {API_URL}")
    print("-" * 60)
    
    success_count = 0
    
    for idx, knowledge in enumerate(sample_knowledge, 1):
        try:
            response = requests.post(
                f"{API_URL}/api/knowledge/add",
                json=knowledge,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ [{idx}/{len(sample_knowledge)}] Added: {knowledge['title']}")
                success_count += 1
            else:
                print(f"✗ [{idx}/{len(sample_knowledge)}] Failed: {knowledge['title']}")
                print(f"  Error: {response.text}")
        
        except requests.exceptions.ConnectionError:
            print(f"✗ Cannot connect to API at {API_URL}")
            print("  Make sure the application is running (python main.py)")
            return
        
        except Exception as e:
            print(f"✗ [{idx}/{len(sample_knowledge)}] Error: {e}")
    
    print("-" * 60)
    print(f"✓ Successfully added {success_count}/{len(sample_knowledge)} documents")
    print("\nYou can now test the system by asking questions like:")
    print("  - 'How do I reset my password?'")
    print("  - 'What are your business hours?'")
    print("  - 'How do I cancel my subscription?'")
    print("  - 'Do you have a mobile app?'")


if __name__ == "__main__":
    add_knowledge()

