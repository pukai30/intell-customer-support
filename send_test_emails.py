"""
Send test emails to trigger auto-assignment
Run this script to test the auto-assignment feature
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# Test email scenarios
TEST_EMAILS = {
    "1": {
        "subject": "Need new workstation for AutoCAD",
        "body": """Hi IT Support,

I need a new high-performance workstation for running AutoCAD and 3D rendering software. 
My current computer is too slow for the new projects. Can someone help me get approval and 
configure the right specs? I also need it integrated with our domain and all software licenses transferred.

Thanks,
John Doe
Engineering Department"""
    },
    "2": {
        "subject": "Suspicious email with attachment",
        "body": """Hi,

I received a suspicious email claiming to be from IT asking me to download an attachment 
and enter my credentials. I didn't click it, but I'm worried it might be a phishing attempt. 
Several colleagues also received similar emails. Should I report this somewhere?

Please advise urgently.

Best regards,
Jane Smith"""
    },
    "3": {
        "subject": "Need custom Excel macro for reporting",
        "body": """Hello IT Team,

Our team needs a custom Excel macro to automate our monthly sales reports. The macro 
should pull data from multiple sheets, calculate totals, and generate charts. Can someone 
from IT help develop this?

This would save us about 10 hours per month.

Thanks,
Mike Johnson
Sales Department"""
    },
    "4": {
        "subject": "Entire floor has no internet",
        "body": """URGENT - IT Support,

The entire 3rd floor has lost internet connectivity since this morning. Around 50 
employees are affected. The network switches seem to be working but there's no internet access. 
This is urgent as it's impacting business operations.

Please respond ASAP.

Tom Wilson
Operations Manager"""
    },
    "5": {
        "subject": "Need access to SAP and SharePoint",
        "body": """Hi IT,

I'm a new employee in the Finance department starting today. I need access to:
- SAP for financial reporting
- SharePoint for the Finance shared drive
- Finance email distribution list

My manager is John Smith. When can this be set up?

Thanks,
Emily Davis
Finance Department"""
    },
    "6": {
        "subject": "Accidentally deleted important files",
        "body": """Hi IT Support,

URGENT: I accidentally deleted an entire folder of important project files from my computer yesterday. 
They're not in the Recycle Bin. Is there any way to recover them? These files are critical for 
tomorrow's client presentation.

The folder was called "ClientProposal_2025" and had about 50 files.

Please help!

Robert Brown
Project Manager"""
    },
    "7": {
        "subject": "Computer acting weird",
        "body": """Hey IT,

My computer is doing strange things lately. Sometimes it's very slow, sometimes programs crash, 
and today it showed a blue screen once. Not sure what's wrong but it's making it hard to work.

Can someone take a look?

Thanks,
Lisa White"""
    },
    "8": {
        "subject": "CRM not syncing with Outlook calendar",
        "body": """Hi IT Team,

Our CRM system is not syncing appointments to Outlook calendars. I've tried reconnecting 
the integration but it still doesn't work. This is affecting the whole sales team's scheduling. 
Can someone look into the API connection?

This started happening since last week's system update.

Best regards,
Steve Martinez
Sales Director"""
    },
    "9": {
        "subject": "Can I use personal cloud storage?",
        "body": """Hello,

I want to use my personal Dropbox account to sync work files between my office computer 
and home laptop. Is this allowed according to company IT policy? 

If not, what are the approved alternatives for working from home?

Thanks,
Anna Lee
Marketing Department"""
    },
    "10": {
        "subject": "Setting up email forwarding for team mailbox",
        "body": """Hi IT,

I need to set up automatic email forwarding from our team mailbox (support@company.com) 
to three different team members:
- john@company.com
- sarah@company.com  
- mike@company.com

Also, I need to configure an auto-reply for when we're out of office. Can someone help 
with the Exchange server settings?

Thanks,
Team Lead
Customer Support"""
    }
}

def send_test_email(from_email, to_email, password, subject, body):
    """Send a test email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        
        print(f"✓ Email sent: {subject}")
        return True
        
    except Exception as e:
        print(f"✗ Error sending email: {e}")
        return False

def main():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║     Auto-Assignment Test Email Generator              ║
    ║     Send test emails to trigger auto-assignment       ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Get email configuration
    from_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    to_email = os.getenv("EMAIL_USER")  # Send to self for testing
    
    if not from_email or not password:
        print("❌ Error: EMAIL_USER and EMAIL_PASSWORD not found in .env file")
        return
    
    print(f"📧 Sending test emails from: {from_email}")
    print(f"📧 Sending test emails to: {to_email}")
    print()
    
    # Display menu
    print("Available test scenarios:")
    print()
    for key, email in TEST_EMAILS.items():
        print(f"  {key}. {email['subject']}")
    print()
    print("  all. Send all test emails")
    print("  0. Exit")
    print()
    
    while True:
        choice = input("Select email to send (1-10, 'all', or '0' to exit): ").strip().lower()
        
        if choice == '0':
            print("👋 Goodbye!")
            break
        
        elif choice == 'all':
            print(f"\n📨 Sending all {len(TEST_EMAILS)} test emails...")
            print("=" * 60)
            success_count = 0
            for key, email in TEST_EMAILS.items():
                if send_test_email(from_email, to_email, password, email['subject'], email['body']):
                    success_count += 1
                    print(f"   [{key}/{len(TEST_EMAILS)}] ✓")
                else:
                    print(f"   [{key}/{len(TEST_EMAILS)}] ✗")
            print("=" * 60)
            print(f"✅ Sent {success_count}/{len(TEST_EMAILS)} emails successfully!")
            print()
            print("💡 Check the backend logs and UI in ~1 minute to see auto-assignments")
            print()
            
        elif choice in TEST_EMAILS:
            email = TEST_EMAILS[choice]
            print(f"\n📨 Sending: {email['subject']}")
            print("-" * 60)
            if send_test_email(from_email, to_email, password, email['subject'], email['body']):
                print("✅ Email sent successfully!")
                print("💡 Check backend logs in ~1 minute to see the auto-assignment")
            print()
        
        else:
            print("❌ Invalid choice. Please try again.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")

