"""
Comprehensive IT Support Knowledge Base for Traditional MNC Company
Run this script to populate the knowledge base with IT support content
"""
import requests
import json

API_URL = "http://localhost:8000"

# Comprehensive IT Support Knowledge Base for MNC
it_support_knowledge = [
    # Hardware Support
    {
        "title": "Desktop Computer Not Starting - Troubleshooting Guide",
        "content": """
**Issue**: Desktop computer won't power on

**Resolution Steps**:
1. **Check Power Connection**
   - Ensure power cable is firmly connected to both computer and wall outlet
   - Try a different power outlet
   - Check if power strip is turned on

2. **Verify Power Supply**
   - Check if PSU switch (back of computer) is in ON position
   - Listen for fan noise or LED indicators
   - If no power at all, PSU may be faulty - contact IT helpdesk for replacement

3. **Monitor Connection**
   - Ensure monitor is powered on
   - Check video cable connection (HDMI/DisplayPort/VGA)
   - Try different video port if available

4. **Hardware Issues**
   - Listen for beep codes during startup
   - Remove and reseat RAM modules
   - Check for loose internal connections (IT staff only)

5. **Escalation**
   - If issue persists after basic checks, log a ticket with IT helpdesk
   - Include error codes, beep patterns, or LED indicators
   - Request on-site support for hardware inspection

**Prevention**:
- Use UPS for power protection
- Ensure proper ventilation around computer
- Regular hardware maintenance as per IT schedule
        """,
        "category": "hardware",
        "tags": ["desktop", "power", "boot", "troubleshooting", "hardware"]
    },
    {
        "title": "Laptop Battery and Charging Issues",
        "content": """
**Common Battery/Charging Problems and Solutions**:

**1. Laptop Not Charging**
   - Remove and reconnect power adapter
   - Check adapter LED indicator (should be lit)
   - Try different power outlet
   - Clean charging port with compressed air
   - Check if adapter is correct model for your laptop
   - Restart laptop while connected to charger

**2. Battery Draining Quickly**
   - Close unnecessary applications
   - Reduce screen brightness
   - Disable Bluetooth/WiFi when not needed
   - Check battery health in Windows (powercfg /batteryreport)
   - Update power management drivers
   - Battery may need replacement after 2-3 years

**3. Battery Not Detected**
   - Shutdown laptop completely
   - Remove battery (if removable)
   - Hold power button for 30 seconds
   - Reinsert battery and power on
   - Update BIOS/firmware
   - Contact IT if battery still not recognized

**4. Overheating While Charging**
   - Ensure laptop is on hard, flat surface
   - Clean air vents with compressed air
   - Don't use laptop on bed or soft surfaces
   - Report to IT if excessive heat persists

**Company Policy**:
- Battery replacement requires IT approval
- Use only company-approved chargers
- Report any battery swelling immediately
- Laptop batteries are replaced after 500 charge cycles or 3 years
        """,
        "category": "hardware",
        "tags": ["laptop", "battery", "charging", "power", "hardware"]
    },
    {
        "title": "Printer Issues - Common Problems and Solutions",
        "content": """
**Printer Troubleshooting Guide for MNC Environment**:

**1. Printer Not Found/Offline**
   - Check if printer is powered on
   - Verify network cable connection (for network printers)
   - Go to Settings > Devices > Printers & Scanners
   - Remove and re-add printer
   - For network printers, verify connection to correct network (LAN not WiFi)
   - Restart print spooler service:
     - Open Services (services.msc)
     - Find "Print Spooler"
     - Right-click > Restart

**2. Print Job Stuck in Queue**
   - Open Devices and Printers
   - Double-click the printer
   - Right-click stuck job > Cancel
   - If stuck, restart print spooler service
   - Clear print queue folder: C:\\Windows\\System32\\spool\\PRINTERS

**3. Poor Print Quality**
   - Run printer cleaning cycle (from printer settings)
   - Check ink/toner levels
   - Ensure correct paper type is loaded
   - Update printer drivers
   - For laser printers: replace toner when at 10%
   - For inkjet: run nozzle check and cleaning

**4. Paper Jams**
   - Power off printer
   - Remove all paper from tray
   - Open access panels and remove jammed paper carefully
   - Check for torn pieces
   - Reload paper properly (don't overfill)
   - Power on and test

**5. Cannot Print from Network**
   - Ping printer IP address from Command Prompt
   - Check if others can print (helps isolate issue)
   - Verify you're on correct VLAN/network
   - Re-install printer driver
   - Contact IT if printer needs network reconfiguration

**IT Contact Required For**:
- Toner/ink cartridge replacement
- Printer hardware repairs
- Network printer configuration
- Adding new printers
- Driver installation on locked-down PCs

**Standard Printers by Department**:
- Finance: Floor 3, Printer-FIN-01 (Secure printing enabled)
- HR: Floor 2, Printer-HR-01 (Confidential mode)
- General: Each floor has 2 shared printers (Printer-FLR#-01/02)
        """,
        "category": "hardware",
        "tags": ["printer", "printing", "paper jam", "network printer", "hardware"]
    },

    # Software Support
    {
        "title": "Microsoft Office 365 - Common Issues and Solutions",
        "content": """
**Office 365 Support Guide for MNC Employees**:

**1. Cannot Open Office Applications (Word, Excel, PowerPoint)**
   - **Activation Issues**:
     - Open any Office app > File > Account
     - Check activation status
     - If not activated: Click "Activate Product"
     - Sign in with your company email (@company.com)
     - If still failing, run: "C:\\Program Files\\Microsoft Office\\Office16\\OSPPREARM.exe" as admin

   - **Licensing Issues**:
     - Your Office license is tied to your employee account
     - Contact IT if license shows as expired
     - Temporary workers use web versions only

**2. Excel Files Not Opening/Crashing**
   - Start Excel in Safe Mode: Hold Ctrl while opening
   - Disable add-ins: File > Options > Add-ins > Manage COM Add-ins > Go > Uncheck all
   - Repair Office: Control Panel > Programs > Microsoft Office > Change > Quick Repair
   - If persists: Online Repair (requires internet)

**3. Outlook Issues**
   - **Cannot Send/Receive Emails**:
     - Check internet connection
     - Verify Outlook is online (status bar should not say "Working Offline")
     - Send/Receive > Work Offline (toggle off)
     - Check mailbox size (max 50GB per company policy)

   - **Outlook Slow Performance**:
     - Archive old emails (older than 1 year)
     - Compact mailbox: File > Tools > Mailbox Cleanup
     - Disable unnecessary add-ins
     - Run inbox cleanup to remove large attachments

**4. OneDrive Sync Issues**
   - **Files Not Syncing**:
     - Check OneDrive icon in system tray
     - Click icon > Help & Settings > Pause syncing > Resume
     - Ensure adequate disk space (need 10% free)
     - Check file name for special characters (not allowed: < > : " / \\ | ? *)
     - File path must be under 400 characters

   - **Sync Conflicts**:
     - Open OneDrive folder
     - Look for files with "-conflict" suffix
     - Compare versions and keep the correct one
     - Delete conflict file

**5. Teams Issues**
   - **Cannot Join Meetings**:
     - Clear Teams cache:
       - Close Teams completely
       - Press Win+R, type: %appdata%\\Microsoft\\Teams
       - Delete all folders except "Cookies" and "Databases"
       - Restart Teams

   - **Audio/Video Not Working**:
     - Click profile picture > Settings > Devices
     - Test audio and video
     - Ensure correct devices are selected
     - Check if antivirus is blocking Teams

**Company Office 365 Policies**:
- License includes: Word, Excel, PowerPoint, Outlook, Teams, OneDrive (1TB)
- Office apps auto-update monthly
- Multi-factor authentication required
- OneDrive automatic backup enabled for Desktop, Documents, Pictures
- Email retention: 7 years (legal requirement)
- Maximum attachment size: 150MB (use OneDrive links for larger files)

**Getting Help**:
- Self-service: https://support.microsoft.com/office
- Company IT Portal: https://ithelp.company.com
- Call IT Helpdesk: Ext 4357 (HELP)
        """,
        "category": "software",
        "tags": ["office365", "microsoft", "word", "excel", "outlook", "teams", "software"]
    },
    {
        "title": "VPN Connection Issues and Setup",
        "content": """
**Corporate VPN Setup and Troubleshooting Guide**:

**VPN Setup for New Employees**:
1. **Download VPN Client**
   - Go to https://vpn.company.com
   - Login with your employee credentials
   - Download Cisco AnyConnect VPN Client (company standard)
   - Run installer with administrator rights

2. **Initial Configuration**
   - Open AnyConnect
   - Server Address: vpn.company.com
   - Username: Your employee ID (e.g., EMP12345)
   - Password: Your network password
   - Second Password: Authenticator code from mobile app (Duo Security)

3. **Mobile Authenticator Setup**
   - Install Duo Mobile app from app store
   - Scan QR code from IT during onboarding
   - Approve login requests when prompted

**Common VPN Issues**:

**1. Cannot Connect to VPN**
   - **Error**: "Connection Failed"
     - Check internet connection first
     - Ensure you're not on office network (VPN not needed internally)
     - Verify VPN credentials
     - Check if caps lock is on (password is case-sensitive)
     - Try different network (switch from WiFi to mobile hotspot)

   - **Error**: "Certificate Error"
     - Download latest VPN client from IT portal
     - Install company root certificate
     - Contact IT to reset your VPN account

**2. VPN Connects but Cannot Access Resources**
   - **Diagnosis**:
     - Open Command Prompt
     - Type: ping 10.10.10.1 (internal server)
     - If successful but still can't access: DNS issue
     
   - **Solution**:
     - Disconnect VPN
     - Open Network Adaptor Settings
     - Right-click VPN adapter > Properties
     - Internet Protocol Version 4 > Properties
     - Set DNS to:
       - Primary: 10.10.10.5
       - Secondary: 10.10.10.6
     - Reconnect VPN

**3. VPN Disconnects Frequently**
   - Increase timeout: AnyConnect > Preferences > VPN Timeout = 30 minutes
   - Disable power saving for network adapter
   - Use wired connection instead of WiFi
   - Update network drivers
   - Contact IT if issue persists (may need network optimization)

**4. Slow Performance on VPN**
   - Close unnecessary applications
   - Don't stream video while on VPN
   - Use terminal/remote desktop instead of file transfers
   - VPN is split-tunnel: Only company resources route through VPN
   - Contact IT if consistently slow (may need bandwidth upgrade)

**VPN Usage Policies**:
- ✅ **Allowed**:
  - Accessing company email, files, applications
  - Remote desktop to office computer
  - Using from home, cafe, airport
  
- ❌ **Not Allowed**:
  - Sharing VPN credentials
  - Using non-company VPN clients
  - P2P file sharing while connected
  - Leaving VPN connected when not in use
  - Using VPN from high-risk countries (check with security team)

**VPN Best Practices**:
- Always disconnect when finished
- Don't save password in VPN client
- Use VPN for all remote work
- Report any suspicious activity
- Keep VPN client updated

**Different VPN Access Levels**:
- **Standard**: Email, shared drives, intranet
- **Privileged**: Server access, admin tools (requires approval)
- **Contractor**: Limited to specific applications only
- **Executive**: Full access including sensitive systems

**Support**:
- VPN Setup: Self-service at vpn.company.com/setup
- Reset Password: Ext 4357 or selfservice.company.com
- Technical Issues: Log ticket at ithelp.company.com
- After Hours VPN Support: +1-800-COMPANY-IT (24/7)
        """,
        "category": "network",
        "tags": ["vpn", "remote access", "network", "connectivity", "security"]
    },
    {
        "title": "Password Reset and Account Unlock Procedures",
        "content": """
**Self-Service Password Management Guide**:

**Password Reset (When You Remember Old Password)**:

**Method 1: Self-Service Portal (Recommended)**
1. Go to https://selfservice.company.com
2. Click "Reset Password"
3. Enter your Employee ID
4. Verify identity using one of:
   - Mobile phone SMS (registered number)
   - Email code (personal email on file)
   - Security questions
5. Create new password following policy:
   - Minimum 12 characters
   - Mix of uppercase, lowercase, numbers, symbols
   - Cannot be same as last 10 passwords
   - Must not contain employee ID or name
6. Password changes apply to:
   - Windows login
   - Email
   - VPN
   - All company applications

**Method 2: While Logged In to Windows**
1. Press Ctrl + Alt + Delete
2. Click "Change Password"
3. Enter old password
4. Enter new password twice
5. Click OK

**Password Reset (When You Forgot Password)**:

**If Self-Service is Configured**:
1. At Windows login screen, click "Reset Password"
2. Answer security questions
3. Receive code on registered mobile/email
4. Create new password

**If Self-Service Not Configured**:
- Call IT Helpdesk: Ext 4357 (office hours)
- After hours: +1-800-COMPANY-IT
- Provide:
  - Employee ID
  - Full name
  - Department
  - Manager's name
  - Last 4 digits of registered mobile number
- IT will verify identity and reset password
- Temporary password sent to personal email
- Must change at next login

**Account Locked Out**:

**Common Causes**:
- 5 failed login attempts (auto-locks for 30 minutes)
- Multiple devices with old password saved
- VPN trying old credentials
- Mobile device with wrong password

**Immediate Unlock**:
1. Go to https://selfservice.company.com
2. Click "Unlock Account"
3. Verify identity (SMS/Email/Questions)
4. Account unlocked immediately

OR

- Call IT Helpdesk for immediate unlock
- IT can unlock remotely in <2 minutes

**After Unlock**:
- Update password on all devices:
  - Desktop/Laptop
  - Mobile phone (email account)
  - VPN saved credentials
  - Any saved browser passwords

**Password Policy - Must Know**:
- **Length**: 12-20 characters
- **Complexity**: 3 of 4 (Upper, Lower, Number, Special)
- **Expiry**: 90 days (reminder at 14, 7, 1 days before)
- **Reuse**: Cannot use last 10 passwords
- **Lockout**: 5 failed attempts = 30 min lock

**Strong Password Examples** (Don't use these exact ones!):
- C0mpany@2024!Secure
- MyP@ssw0rd#Company24
- S3cur3!Work*2024

**Weak Passwords** (Never use these):
- Password123
- Company2024
- Your name or employee ID
- Keyboard patterns (Qwerty123)

**Multi-Factor Authentication (MFA)**:
- Required for:
  - VPN access
  - Email (external access)
  - Cloud applications
  - Remote desktop
  
- Setup MFA:
  1. Install Duo Mobile app
  2. Go to https://mfa.company.com
  3. Scan QR code with app
  4. Approve test authentication
  
- Lost MFA Device:
  - Contact IT immediately
  - Temporary codes available from helpdesk
  - Re-enrollment required

**Security Best Practices**:
- ✅ Use unique password for company account
- ✅ Enable password manager (1Password provided by company)
- ✅ Never share password with anyone (including IT)
- ✅ Change password if you suspect compromise
- ✅ Use MFA on all supported systems
- ❌ Don't write password down
- ❌ Don't email passwords
- ❌ Don't use same password across accounts
- ❌ Don't save passwords on shared computers

**Special Scenarios**:

**New Employee First Login**:
- Temporary password received via personal email
- Must change at first login
- Setup security questions
- Enroll in MFA

**Leaving on Extended Leave**:
- Account remains active for 30 days
- After 30 days: Account disabled (can be re-enabled)
- After 90 days: Account deactivated (requires manager approval to reactivate)

**Contractor/Vendor Accounts**:
- 60-day password expiry
- Must renew access every 90 days
- Limited to specific systems

**Emergency Access**:
- For critical systems during password reset
- Manager can request break-glass access
- Requires VP approval
- All actions logged and audited

**Contact Information**:
- Self-Service Portal: https://selfservice.company.com
- IT Helpdesk Phone: Ext 4357 (HELP)
- After Hours: +1-800-COMPANY-IT
- Email: ithelpdesk@company.com
- IT Portal: https://ithelp.company.com
        """,
        "category": "security",
        "tags": ["password", "reset", "account", "locked", "security", "mfa"]
    },

    # Email and Communication
    {
        "title": "Email Issues - Outlook Troubleshooting",
        "content": """
**Complete Outlook Email Troubleshooting Guide**:

**1. Cannot Send Emails**

**Symptom**: Email stuck in Outbox
- **Solutions**:
  - Check Outbox folder - delete corrupted email if stuck
  - Verify internet connection
  - Check email size (max 150MB including attachments)
  - Large attachment? Use OneDrive share link instead
  - Ensure Outlook is not in Offline mode
    - Ribbon should not show "Working Offline"
    - Go to Send/Receive tab > Work Offline (ensure it's unchecked)
  
**Symptom**: Error "The message could not be sent"
- Check recipient email address for typos
- Verify you have send permissions (some shared mailboxes are receive-only)
- Check if recipient domain is blocked (external email policy)
- Try sending without attachment to isolate issue

**2. Cannot Receive Emails**

**Check These First**:
- Verify internet connection
- Check Junk/Spam folder
- Review Inbox rules (might be auto-filing)
- Check mailbox quota: File > Info > Cleanup Tools > Mailbox Cleanup
  - Company limit: 50GB
  - Warning at 45GB
  - Sending blocked at 49GB

**Mailbox Full Solutions**:
1. Delete items from "Deleted Items" permanently
2. Archive old emails (>1 year) to archive mailbox
3. Remove large attachments:
   - File > Tools > Mailbox Cleanup > Find > Items larger than 10MB
4. Empty "Sent Items" of emails >3 months old

**3. Outlook Running Slow**

**Immediate Fixes**:
- Close and reopen Outlook
- Disable cached mode temporarily: File > Account Settings > Disable "Use Cached Exchange Mode"
- Compact OST file:
  - Go to File > Account Settings > Account Settings
  - Data Files tab > Select account > Settings
  - Advanced > Outlook Data File Settings > Compact Now

**Long-term Solutions**:
- Archive old emails regularly
- Limit inbox to current year only
- Disable unnecessary add-ins:
  - File > Options > Add-ins
  - Manage: COM Add-ins > Go
  - Uncheck unused add-ins
- Run Outlook in Safe Mode to test: outlook.exe /safe

**4. Missing Emails or Folders**

**Emails Disappeared**:
- Check "Deleted Items" folder
- Review "Junk Email" folder
- Check if sorting is applied (clear all sorts)
- Search for specific email: Ctrl + E
- Check "Recoverable Items":
  - Folder pane > Deleted Items > Recover Deleted Items from Server

**Folders Missing**:
- Right-click on mailbox root > Update Folder
- Check if accidentally moved to another folder
- Restore from backup (contact IT - backups kept for 30 days)

**5. Shared Mailbox Access Issues**

**Cannot See Shared Mailbox**:
1. Verify you have permission (check with mailbox owner)
2. Add manually:
   - File > Account Settings > Account Settings
   - Email tab > Change > More Settings
   - Advanced tab > Add > Enter shared mailbox email
3. Close and reopen Outlook

**Access Denied Error**:
- Permission may have been revoked - contact mailbox owner
- Could be temporary Active Directory replication delay (wait 15 min)
- Log out and back in to Windows to refresh credentials

**6. Calendar Issues**

**Meeting Invites Not Sending**:
- Check delegate permissions
- Verify free/busy settings: File > Options > Calendar > Free/Busy Options
- Ensure timezone is correct
- Try creating meeting from OWA (Outlook Web Access)

**Cannot See Others' Calendars**:
- They must share calendar with you first
- Check if calendar sharing is enabled: File > Options > Calendar > Free/Busy Options
- Use scheduling assistant for meeting planning

**7. Outlook Crashes or Won't Open**

**Quick Fixes**:
1. Start in Safe Mode: Press Windows key, type: outlook.exe /safe
2. If Safe Mode works:
   - Disable all add-ins
   - Re-enable one by one to find culprit
3. Create new Outlook profile:
   - Control Panel > Mail > Show Profiles
   - Add > Create new profile
   - Set as default

**Repair Outlook**:
1. Close Outlook
2. Control Panel > Programs > Microsoft Office
3. Change > Quick Repair (try first)
4. If still failing: Online Repair (requires internet)

**8. Mobile Device Email Issues**

**Cannot Setup Email on Mobile**:
- Use Outlook mobile app (company standard)
- Download from:
  - iOS: App Store
  - Android: Google Play Store
- Setup:
  - Enter work email: yourname@company.com
  - Password: Your network password
  - MFA: Approve on Duo Mobile
  
**Mobile Email Not Syncing**:
- Check internet connection
- Sign out and back in
- Reinstall Outlook app
- Verify no MDM (Mobile Device Management) blocks

**9. Out of Office (OOF) Setup**

**Standard Setup**:
1. File > Automatic Replies
2. Select "Send automatic replies"
3. Set time range (optional)
4. Configure:
   - Inside My Organization: Message for internal staff
   - Outside My Organization: Message for external contacts
5. Preview before enabling

**Best Practices**:
- Include:
  - Dates you'll be away
  - Return date
  - Alternate contact (with permission)
  - Urgent contact method (if applicable)
- Don't include:
  - Personal details (vacation location)
  - Home phone number
  - Overly detailed explanations

**10. Email Signature Management**

**Create/Update Signature**:
1. File > Options > Mail > Signatures
2. New > Name your signature
3. Edit signature (company template available at \\\\shared\\IT\\Email-Signature-Template.htm)
4. Include:
   - Full name and title
   - Department
   - Phone extension
   - Company address
   - Company logo (IT provides)
5. Set defaults for New messages and Replies/Forwards

**Company Signature Policy**:
- Must include: Name, title, department, phone, email
- Optional: Mobile (if client-facing), LinkedIn (approved roles)
- Not allowed: Personal quotes, political statements, large images

**11. Search Not Working**

**Rebuild Search Index**:
1. Control Panel > Indexing Options
2. Advanced > Rebuild
3. Wait 15-30 minutes for completion
4. Don't use Outlook during rebuild

**12. Rules Not Working**

**Diagnose Rule Issues**:
1. File > Rules and Alerts > Manage Rules & Alerts
2. Check if rule is enabled (checkbox)
3. Verify conditions are correct
4. Test with "Run Rules Now"
5. Rules applied in order - check priority

**Rule Limitations**:
- Maximum 256KB total rule size
- Cannot create rules for shared mailboxes (server-side rules only)
- Some conditions don't work on mobile

**When to Contact IT**:
- Mailbox corruption (unusual errors persisting)
- Need mailbox quota increase (requires manager approval)
- Shared mailbox setup (requires security approval)
- Email retention policy questions
- Suspicious emails or security concerns
- Email archiving and e-discovery
- Distribution list management

**Quick Self-Service Links**:
- OWA (Web Access): https://mail.company.com
- Reset Password: https://selfservice.company.com
- IT Portal: https://ithelp.company.com
- Email Training: https://training.company.com/outlook

**Contact IT Helpdesk**:
- Phone: Ext 4357 (HELP)
- Email: ithelpdesk@company.com
- Teams: @IT Helpdesk
- Portal: https://ithelp.company.com/submit-ticket
        """,
        "category": "email",
        "tags": ["email", "outlook", "mail", "calendar", "communication"]
    },

    # File and Storage
    {
        "title": "Network Drive Access and Mapping",
        "content": """
**Network Drive (Shared Drive) Access Guide**:

**Company Network Drives Structure**:
- **H: Drive** - Personal home folder (Private, 50GB quota)
- **P: Drive** - Department shared folder (Varies by department)
- **S: Drive** - Project shared folders (Access by request)
- **T: Drive** - Team collaboration (Department specific)
- **U: Drive** - Temporary storage (Auto-cleaned after 90 days)

**Map Network Drive - Windows 10/11**:

**Method 1: Automatic (Group Policy)**
- Drives auto-map at login if you have permissions
- Reboot computer if drives don't appear
- Log out and back in to refresh

**Method 2: Manual Mapping**
1. Open File Explorer
2. Click "This PC" > Map network drive
3. Choose drive letter
4. Enter path: \\\\fileserver.company.com\\[share name]
5. Check "Reconnect at sign-in"
6. Check "Connect using different credentials" (if needed)
7. Click Finish
8. Enter credentials if prompted:
   - Username: COMPANY\\[your employee ID]
   - Password: Your network password

**Common Network Paths**:
- Home: \\\\fileserver.company.com\\home\\[employee_id]
- Department: \\\\fileserver.company.com\\departments\\[dept_name]
- Projects: \\\\fileserver.company.com\\projects\\[project_code]
- Shared: \\\\fileserver.company.com\\shared

**Troubleshooting Network Drive Issues**:

**1. Cannot Access Network Drive**
- **Error**: "Network path not found"
  - Check if connected to company network (or VPN if remote)
  - Ping file server: ping fileserver.company.com
  - Check if you have permission to the folder
  - Verify correct path/share name
  - Contact IT to verify account permissions

- **Error**: "Access is denied"
  - Permission issue - contact folder owner
  - May need to request access via IT portal
  - Check if account is locked
  - Clear cached credentials: Control Panel > Credential Manager

**2. Drive Disconnected (Red X)**
- Disconnect and reconnect drive
- Restart computer
- Check network connectivity
- Re-map drive manually

**3. Cannot Save Files to Network Drive**
- **Check disk quota**:
  - Right-click drive > Properties > See available space
  - Personal (H:) limit: 50GB
  - Request quota increase via IT portal (requires manager approval)
  
- **File path too long**:
  - Windows limit: 260 characters (full path)
  - Solution: Move file closer to root or shorten file/folder names
  
- **File in use**:
  - Someone else has file open
  - Check who: Right-click file > Properties > Details
  - Ask them to close or open read-only

**4. Slow Performance**
- **Large files**:
  - Files >1GB should be on project drives, not personal
  - Use compression for archives
  
- **Many small files**:
  - Zip folders with many small files
  - Don't store email archives on network drives
  
- **Peak hours**:
  - Network congestion (9-10 AM, 2-3 PM)
  - Schedule large transfers for off-peak hours
  
- **Remote access**:
  - Use VPN for remote access
  - Consider using Remote Desktop instead for heavy file work

**File Sharing Best Practices**:

**1. Share Folder with Colleague**:
- Right-click folder > Properties > Sharing > Advanced Sharing
- Check "Share this folder"
- Permissions > Add user
- Set appropriate permissions:
  - **Read**: View and copy files only
  - **Change**: Read + edit + delete
  - **Full Control**: All permissions + change permissions

**2. Department Shared Folders**:
- Managed by IT and department heads
- Request access: https://ithelp.company.com/access-request
- Typical approval time: 1-2 business days
- Access audited quarterly

**3. Project Folders**:
- Created for specific projects
- Project manager controls access
- Automatically archived 90 days after project closure

**Storage Quota Management**:

**Check Your Quota**:
1. Open network drive
2. Right-click drive > Properties
3. See "Used space" vs "Total capacity"

**When Near Limit**:
- Delete unnecessary files
- Move old projects to archive
- Compress large files
- Request quota increase (requires justification)

**Quota Limits**:
- Personal (H:): 50GB
- Department shared: 500GB-2TB
- Project folders: 100GB-1TB (project dependent)
- Temporary (U:): 10GB per user

**File Retention Policy**:
- **Active projects**: Retained indefinitely
- **Completed projects**: 7 years (regulatory requirement)
- **Personal files**: Backup for 30 days after deletion
- **Temporary drive**: Auto-deleted after 90 days

**Data Backup**:
- Network drives backed up nightly
- Retention: 30 daily backups
- File restoration: Contact IT helpdesk
- Personal responsibility: Don't rely solely on backups

**Mobile/Remote Access**:

**Access from Home**:
1. Connect to VPN
2. Open File Explorer
3. Navigate to \\\\fileserver.company.com\\[share]
4. Same as office access

**Access from Mobile**:
- Use Microsoft Teams for shared files
- OneDrive for personal files
- No direct mobile drive mapping

**Access from Mac**:
1. Finder > Go > Connect to Server
2. Enter: smb://fileserver.company.com/[share]
3. Enter credentials
4. Click Connect

**Security Guidelines**:
- ✅ Only share files with authorized personnel
- ✅ Remove access when no longer needed
- ✅ Use appropriate permission levels (least privilege)
- ✅ Report suspicious files to security team
- ✅ Encrypt sensitive data (IT provides tools)

- ❌ Don't share drives with external parties
- ❌ Don't store passwords in files
- ❌ Don't bypass security controls
- ❌ Don't use personal cloud storage for company files

**Common Errors and Solutions**:

**Error 0x80070035**: "Network path not found"
- Check network connection
- Verify correct path
- Ensure file server is online (check IT status page)

**Error 0x80004005**: Unspecified error
- Disable offline files:
  - Control Panel > Sync Center > Manage offline files
  - Disable offline files
  - Restart computer

**Error 0x800704CF**: Network location cannot be reached
- Network timeout issue
- Check VPN connection if remote
- Restart network services: services.msc > Workstation > Restart

**Access Denied (0x80070005)**:
- Request permission from folder owner
- Check with IT if permission should be granted
- Verify account is active and not locked

**Need Help?**:
- Access request: https://ithelp.company.com/access-request
- Quota increase: https://ithelp.company.com/quota-increase
- File restore: Contact IT helpdesk
- IT Helpdesk: Ext 4357 or ithelpdesk@company.com
        """,
        "category": "storage",
        "tags": ["network drive", "file share", "storage", "mapping", "access"]
    },

    # System and Performance
    {
        "title": "Computer Running Slow - Performance Optimization",
        "content": """
**Computer Performance Troubleshooting Guide**:

**Immediate Quick Fixes** (Try these first):

**1. Restart Computer**
- Sounds simple, but fixes 70% of issues
- Full restart (not just sleep/hibernate)
- Close all applications before restart
- Wait for all updates to install

**2. Close Unnecessary Programs**
- Press Ctrl + Shift + Esc (Task Manager)
- Check "Processes" tab
- Sort by Memory or CPU
- Close programs you're not using
- Look for: Chrome (multiple tabs), Outlook, Teams, Excel with large files

**3. Check Disk Space**
- Open This PC
- Check C: drive space
- Need minimum 20GB free (15% of total)
- If low:
  - Empty Recycle Bin
  - Delete Downloads folder files
  - Run Disk Cleanup (cleanmgr.exe)
  - Remove temporary files

**Detailed Performance Analysis**:

**1. High CPU Usage**
- **Check Task Manager**: Ctrl + Shift + Esc > Performance tab
- **Identify culprit**:
  - Consistent 100% CPU = problematic process
  - Common causes:
    - Windows Update (let it finish)
    - Antivirus scan (let it complete)
    - Browser with many tabs
    - Excel with complex formulas/macros

- **Solutions**:
  - Close intensive applications
  - Restart problematic program
  - Update software to latest version
  - For persistent issues: Escalate to IT

**2. High Memory Usage**
- **Check available RAM**:
  - Task Manager > Performance > Memory
  - Company standard: 16GB RAM
  - Anything >90% usage causes slowdown

- **Memory hogs**:
  - Google Chrome (each tab uses RAM)
  - Outlook with large mailbox
  - Excel with large datasets
  - Multiple PDFs open

- **Solutions**:
  - Close unused browser tabs (use OneTab extension)
  - Archive old emails in Outlook
  - Close unused applications
  - Reboot to clear memory
  - Request RAM upgrade if consistently >80% (IT approval needed)

**3. Disk Usage at 100%**
- **Common causes**:
  - Windows Update
  - Antivirus scan
  - SuperFetch/SysMain service
  - Background backup
  - Failing hard drive

- **Solutions**:
  - Wait for updates/scans to complete
  - Disable Windows Search temporarily:
    - services.msc > Windows Search > Stop
  - Disable SysMain:
    - services.msc > SysMain > Stop
  - If persistent: May indicate failing drive - Contact IT immediately

**4. Startup Programs Optimization**
- **Too many startup programs slow boot**:
  - Task Manager > Startup tab
  - Disable unnecessary programs:
    - Keep: Antivirus, VPN client, Company apps
    - Disable: Spotify, Personal apps, Gaming software

- **How to disable**:
  - Right-click program > Disable
  - Doesn't uninstall, just prevents auto-start

**5. Browser Performance**

**Chrome/Edge Running Slow**:
- Clear browser cache:
  - Chrome: Ctrl + Shift + Delete > Clear browsing data
  - Select "Cached images and files"
  - Time range: All time
  
- Disable extensions:
  - chrome://extensions
  - Disable unused extensions
  - Keep: Company required extensions only

- Reset browser if very slow:
  - Settings > Reset settings > Restore to defaults

**6. Network Performance Issues**

**Slow Internet/Network**:
- Run speed test: https://speedtest.company.com
- Company standard:
  - Office: 100Mbps download, 100Mbps upload
  - VPN: 50Mbps+ expected
  
- **Troubleshooting**:
  - Restart network adapter:
    - Network icon > Network settings > Change adapter > Disable/Enable
  - Forget and reconnect WiFi
  - Try wired connection (Ethernet)
  - Check if others experiencing same issue
  - Contact IT if building-wide issue

**7. Windows Updates**

**Updates Slowing Computer**:
- Check update status: Windows Update settings
- Let updates complete (don't interrupt)
- Schedule updates for off-hours:
  - Settings > Update & Security > Change active hours
  - Set to your work hours (e.g., 8 AM - 6 PM)

**Failed Updates**:
- Run Windows Update Troubleshooter:
  - Settings > Update & Security > Troubleshoot
- If stuck, contact IT (may need manual intervention)

**8. Disk Cleanup and Maintenance**

**Run Disk Cleanup**:
1. Open File Explorer
2. Right-click C: drive > Properties
3. Click "Disk Cleanup"
4. Select:
   - Temporary files
   - Downloaded Program Files
   - Recycle Bin
   - Thumbnails
5. Click "Clean up system files" for more options
6. Select Windows Update cleanup, Old Windows installations
7. Run cleanup

**Optimize Disk** (SSD: monthly, HDD: weekly):
1. This PC > Right-click C: drive > Properties
2. Tools tab > Optimize
3. Select drive > Optimize
4. SSD: Runs TRIM
5. HDD: Defragments

**9. Malware/Virus Check**

**If Computer Acting Strange**:
- Run Windows Defender scan:
  - Windows Security > Virus & threat protection
  - Quick scan first
  - If issues found: Full scan
- Company antivirus (Symantec Endpoint Protection):
  - Should auto-scan weekly
  - Manual scan: Open SEP > Scan now
- Report suspicious behavior to security team

**10. Temperature/Overheating**

**Signs of Overheating**:
- Computer hot to touch
- Fan constantly running loud
- Random shutdowns
- Performance throttling

**Immediate Actions**:
- Ensure proper ventilation
- Use laptop on hard, flat surface (not bed/lap)
- Clean air vents with compressed air
- Close resource-intensive apps
- If desktop: Ensure case fans working
- Contact IT if persistent (may need hardware service)

**11. Software Conflicts**

**Recently Installed Software Causing Issues**:
- Uninstall problematic software:
  - Settings > Apps > Uninstall
- Restore to previous state:
  - System Restore (if enabled)
  - Contact IT for assistance
- Check with IT before installing new software (policy requirement)

**12. Profile/User Account Issues**

**Corrupt User Profile**:
- Symptoms:
  - Settings not saving
  - Desktop icons missing
  - Applications won't start
  
- **Solution**:
  - Create temporary local profile (IT task)
  - Migrate data to new profile
  - Contact IT - don't attempt yourself

**Performance Benchmarks**:

**Expected Performance** (Standard corporate laptop):
- **Boot time**: <60 seconds to desktop
- **Application launch**: 
  - Outlook: <10 seconds
  - Chrome: <5 seconds
  - Word/Excel: <8 seconds
- **System responsiveness**: No lag on basic operations

**When Performance Below Par**:
- Run Performance Monitor:
  - perfmon.exe > Create new Data Collector Set
  - Send results to IT for analysis

**Upgrade Considerations**:

**Request Hardware Upgrade**:
- Via IT portal: https://ithelp.company.com/hardware-request
- Eligibility:
  - Computer >4 years old
  - Role requires higher specs (development, design, etc.)
  - Performance consistently poor despite optimization
- Typical upgrades:
  - RAM: 16GB → 32GB
  - Storage: HDD → SSD
  - Full laptop replacement

**Company Hardware Refresh Cycle**:
- Standard laptops: 4 years
- Power users (dev/design): 3 years
- Desktops: 5 years
- Executives: 3 years

**Prevention Tips**:
- ✅ Restart weekly
- ✅ Keep <100 emails in inbox
- ✅ Close applications when done
- ✅ Don't install unnecessary software
- ✅ Run monthly disk cleanup
- ✅ Keep system updated
- ✅ Use OneDrive for files (not local storage)
- ✅ Archive old projects

**Contact IT If**:
- Performance degradation is sudden
- Tried all troubleshooting steps
- Computer >4 years old
- Need hardware upgrade
- Suspect hardware failure
- Business-critical work affected

**IT Support**:
- Phone: Ext 4357
- Email: ithelpdesk@company.com
- Portal: https://ithelp.company.com
- Remote support: Request via portal
- On-site support: Book appointment for hardware issues
        """,
        "category": "performance",
        "tags": ["slow computer", "performance", "optimization", "troubleshooting", "speed"]
    },

    # Security
    {
        "title": "Phishing and Security Threats - Identification and Reporting",
        "content": """
**Comprehensive Security Awareness Guide for MNC Employees**:

**What is Phishing?**
Phishing is a cyber attack where criminals impersonate legitimate entities to steal:
- Passwords and credentials
- Financial information
- Personal data
- Company secrets

**Types of Phishing Attacks**:

**1. Email Phishing** (Most Common)
- Fake emails appearing to be from: IT, HR, executives, banks, vendors
- Goal: Get you to click link, download attachment, or provide credentials

**2. Spear Phishing**
- Targeted attacks using personal information
- Appears to be from someone you know
- Highly convincing and personalized

**3. Whaling**
- Targets high-level executives
- Business email compromise (BEC)
- Often involves fake wire transfer requests

**4. Smishing** (SMS Phishing)
- Phishing via text messages
- Fake delivery notifications, account alerts

**5. Vishing** (Voice Phishing)
- Phone calls from "IT support", "bank", or "vendor"
- Requests for remote access or sensitive information

**How to Identify Phishing Emails**:

**RED FLAGS - WARNING SIGNS**:

1. **Sender Email Address**:
   - ❌ From: IT Support <it-support@cornpany.com> (note the 'corn' instead of 'com')
   - ❌ From: CEO <ceo.john@gmail.com> (CEO would use company email)
   - ❌ From: admin@company-helpdesk.com (extra dash, wrong domain)
   - ✅ Legitimate: ithelpdesk@company.com

2. **Urgent or Threatening Language**:
   - "Your account will be suspended in 24 hours!"
   - "Urgent action required immediately!"
   - "You must verify your account now!"
   - "Security alert - click here immediately!"

3. **Generic Greetings**:
   - "Dear User" (company emails use your name)
   - "Dear Customer"
   - "Hello Employee"
   - vs. Legitimate: "Hi [Your Name],"

4. **Suspicious Links**:
   - Hover over link (don't click!) to see actual URL
   - ❌ https://company-login.suspicious-site.com
   - ❌ http://10.123.45.67/login (IP address instead of domain)
   - ❌ https://cornpany.com (typosquatting)
   - ✅ https://company.com or https://login.company.com

5. **Unexpected Attachments**:
   - Especially: .exe, .zip, .scr, .js, .vbs files
   - Invoice from vendor you don't work with
   - HR document when you're not expecting one

6. **Poor Grammar and Spelling**:
   - Legitimate companies proofread emails
   - Typos, odd phrasing, grammatical errors
   - Example: "You account has been compromise"

7. **Requests for Sensitive Information**:
   - Password (IT NEVER asks for passwords)
   - SSN, bank details, personal information
   - Multi-factor authentication codes
   - Credit card information

8. **Too Good to Be True**:
   - "You've won $1,000,000!"
   - "Free company bonus - click here!"
   - "CEO wants to give you a special reward!"

**Common Phishing Scenarios**:

**Scenario 1: Fake IT Alert**
```
From: IT Security <itsecurity@company-alerts.com>
Subject: URGENT: Your password will expire in 1 hour

Your company password will expire in 1 hour. Click below to reset:
[Reset Password Now]

If you don't reset, you'll be locked out.

IT Department
```

**RED FLAGS**:
- Wrong domain (company-alerts.com vs company.com)
- Urgent time pressure
- Suspicious link
- IT doesn't send password reset links via email

**Scenario 2: CEO Fraud (Whaling)**
```
From: John Smith, CEO <jsmith@gmail.com>
Subject: Urgent Request

I need you to purchase gift cards for a client meeting. $2,000 in iTunes gift cards.
Please handle this quietly and send me the codes by EOD.

Thanks,
John
```

**RED FLAGS**:
- CEO using personal email
- Unusual request (gift cards)
- Urgency and secrecy
- No official purchase process

**Scenario 3: Fake Invoice**
```
From: accounting@vendor-company.com
Subject: Invoice #12345 - Payment Overdue

Your payment is overdue. Please see attached invoice and remit payment.

[Attachment: Invoice_12345.zip]
```

**RED FLAGS**:
- Unexpected invoice
- .zip attachment (could contain malware)
- Not from known vendor
- No previous communication

**What to Do If You Receive Suspicious Email**:

**IMMEDIATE ACTIONS**:

1. **DO NOT CLICK** any links
2. **DO NOT OPEN** attachments
3. **DO NOT RESPOND** to the email
4. **DO NOT PROVIDE** any information

**REPORT IT**:

**Method 1: Outlook Report Button**
- Click "Report Message" button in Outlook ribbon
- Select "Phishing"
- Email forwarded to security team automatically

**Method 2: Forward to Security**
- Forward suspicious email to: phishing@company.com
- Include original email as attachment
- Add any relevant context

**Method 3: IT Portal**
- Go to: https://ithelp.company.com/report-phishing
- Fill out incident form
- Attach screenshot or forward email

**VERIFY IF UNSURE**:
- Call sender directly (use number from company directory, NOT from email)
- Check with your manager
- Contact IT helpdesk to verify legitimacy

**If You Already Clicked/Responded**:

**YOU CLICKED A LINK**:
1. **Immediately disconnect from network**:
   - Unplug Ethernet cable OR
   - Disable WiFi
2. **Don't enter any credentials** if prompted
3. **Call IT immediately**: Ext 4357 (HELP)
4. **Report**: phishing@company.com
5. **IT will**:
   - Scan your computer for malware
   - Monitor your account for suspicious activity
   - Force password reset if needed

**YOU PROVIDED CREDENTIALS**:
1. **Change password IMMEDIATELY**:
   - https://selfservice.company.com
   - Change from different device if possible
2. **Call IT Helpdesk**: Ext 4357
3. **Enable account monitoring**
4. **Report**: phishing@company.com
5. **IT will**:
   - Reset all sessions
   - Enable enhanced monitoring
   - Check for unauthorized access

**YOU OPENED ATTACHMENT**:
1. **Disconnect from network immediately**
2. **DO NOT shut down** computer (preserves evidence)
3. **Call IT immediately**: Ext 4357
4. **Do not delete** email or attachment
5. **IT will**:
   - Quarantine your computer
   - Run malware scan
   - Check for data exfiltration
   - Restore from backup if needed

**Company Security Measures**:

**Email Protections in Place**:
- Advanced email filtering (blocks 99%+ of phishing)
- Link scanning and rewriting
- Attachment sandboxing
- SPF/DKIM/DMARC verification
- But some sophisticated attacks get through!

**User Responsibilities**:
- ✅ Complete annual security awareness training (mandatory)
- ✅ Report all suspicious emails
- ✅ Verify unusual requests
- ✅ Keep security knowledge current
- ✅ Use strong, unique passwords
- ✅ Enable MFA on all accounts

**Other Security Threats**:

**1. Malware/Ransomware**:
- Don't download from untrusted sources
- Keep antivirus updated (automatic)
- Scan USB drives before use
- Don't disable security software

**2. Social Engineering**:
- Verify identity before sharing info
- Don't discuss sensitive topics in public
- Badge tailgaters (report to security)
- Lock screen when away: Win+L

**3. Physical Security**:
- Lock laptop when unattended
- Don't leave devices in car
- Use privacy screen in public
- Shred sensitive documents
- Report lost devices immediately

**4. Remote Work Security**:
- Always use VPN for company resources
- Secure home WiFi (WPA3 encryption)
- Don't use public WiFi without VPN
- Keep work and personal devices separate

**Data Classification**:

**Public**: Can be shared freely
- Marketing materials
- Published reports
- Public website content

**Internal**: For employees only
- Company policies
- Internal announcements
- Employee directory

**Confidential**: Need-to-know basis
- Financial data
- Customer information
- Strategic plans
- HR records

**Restricted**: Highest security
- Trade secrets
- M&A information
- Security credentials
- Executive communications

**Best Practices**:

**Email Safety**:
- Verify sender before clicking links
- Type URLs manually instead of clicking
- Use bookmarks for frequent sites
- Hover over links to check destination
- Be skeptical of unexpected emails

**Password Security**:
- Never share passwords (even with IT)
- Use unique password for work account
- Use company password manager (1Password)
- Change password if suspicious activity
- Never email passwords

**Device Security**:
- Keep OS and software updated
- Use full disk encryption (enabled by default)
- Enable screen lock (15-min timeout)
- Don't jailbreak/root devices
- Report lost devices within 1 hour

**Incident Response**:

**If Security Incident Occurs**:
1. **Contain**: Disconnect from network
2. **Report**: Call IT immediately (Ext 4357)
3. **Preserve**: Don't delete evidence
4. **Document**: Note what happened, when, and actions taken
5. **Cooperate**: Work with IT and security team

**Escalation Path**:
- Level 1: IT Helpdesk (Ext 4357)
- Level 2: Security Operations Center (SOC)
- Level 3: Chief Information Security Officer (CISO)
- Legal: For regulatory/compliance issues

**Reporting Channels**:
- **Phishing**: phishing@company.com
- **Security Incident**: security@company.com or Ext 4911 (SECURITY)
- **Data Breach**: privacy@company.com + Ext 4911
- **Physical Security**: Ext 4999 (SECURITY DESK)
- **Anonymous Report**: https://company.ethicspoint.com

**Monthly Security Challenges** (Gamification):
- Test phishing simulations (don't worry if you fall for them - learning opportunity!)
- Security awareness quizzes
- Top performers recognized monthly
- Prizes for catching real phishing

**Training and Resources**:
- Annual mandatory security training: https://training.company.com/security
- Monthly security newsletter: Subscribe at https://security.company.com/newsletter
- Security awareness videos: https://security.company.com/videos
- Phishing examples: https://security.company.com/phishing-examples
- Report card: Check how you're doing at https://security.company.com/my-score

**Remember**:
> **When in doubt, don't click it out!** 
> It's better to verify and be safe than to click and be sorry.

**Emergency Contacts**:
- IT Helpdesk: Ext 4357 (HELP) or ithelpdesk@company.com
- Security Team: Ext 4911 or security@company.com
- After Hours: +1-800-COMPANY-IT (24/7)
- Emergency: 911 (physical threats)

**Quick Decision Tree**:
```
Received email with link/attachment?
├─ Do I expect this?
│  ├─ No → DON'T CLICK → Report to security
│  └─ Yes → Verify sender
│     ├─ Sender looks wrong → DON'T CLICK → Report
│     └─ Sender looks right → Hover over link
│        ├─ URL suspicious → DON'T CLICK → Report  
│        └─ URL looks right → Still verify by phone
│           ├─ Not verified → DON'T CLICK → Report
│           └─ Verified → Safe to proceed
```

**You are the first line of defense. Stay vigilant!** 🛡️
        """,
        "category": "security",
        "tags": ["phishing", "security", "scam", "cybersecurity", "threats", "malware"]
    },

    # Mobile and BYOD
    {
        "title": "Mobile Device Setup and Management (BYOD)",
        "content": """
**Company Mobile Device and BYOD Policy Guide**:

**BYOD (Bring Your Own Device) Policy Overview**:

The company allows personal mobile devices for work under specific conditions:
- Device must be enrolled in Mobile Device Management (MDM)
- Must meet minimum security requirements
- Company can wipe corporate data remotely (not personal data)
- You maintain ownership of device
- Company doesn't pay for personal device/plan

**Eligible Devices**:
- ✅ iOS 14.0 or later (iPhone, iPad)
- ✅ Android 10.0 or later
- ❌ Jailbroken/Rooted devices (not allowed)
- ❌ Devices with known security vulnerabilities

**Device Enrollment Process**:

**Step 1: Initial Setup Request**
1. Go to: https://mdm.company.com/enroll
2. Login with employee credentials
3. Select device type (iOS/Android)
4. Accept BYOD agreement
5. Receive enrollment email/SMS

**Step 2: Install Company Portal App**

**For iOS**:
1. App Store > Search "Company Portal"
2. Download and install
3. Open app > Sign in with work email
4. Follow enrollment wizard

**For Android**:
1. Google Play Store > Search "Company Portal"
2. Download and install
3. Open app > Sign in with work email
4. Follow enrollment wizard
5. May need to activate Device Admin

**Step 3: Install Required Apps**
Once enrolled, install:
- Microsoft Outlook (Email)
- Microsoft Teams (Chat/Meetings)
- OneDrive (File access)
- Authenticator (MFA)
- Company VPN app (if applicable)

**Step 4: Configure Email**

**iOS - Outlook Setup**:
1. Open Outlook app
2. Enter work email: yourname@company.com
3. Tap "Add Account"
4. Enter password
5. Approve MFA request (Duo)
6. Email will sync automatically

**Android - Outlook Setup**:
1. Open Outlook app
2. Tap "Get Started"
3. Enter work email: yourname@company.com
4. Tap "Continue"
5. Enter password
6. Approve MFA prompt
7. Select sync settings

**Email Sync Settings** (Company Standard):
- Sync period: 1 month
- Attachments: Download on WiFi only
- Notifications: Enabled
- Badge count: Enabled

**MDM Security Policies Enforced**:

**On Your Personal Device**:
- ✅ PIN/Passcode required (minimum 6 digits)
- ✅ Biometric authentication allowed (Face ID, Fingerprint)
- ✅ Screen lock after 15 minutes
- ✅ Encryption enabled
- ✅ Find My Device enabled

**Corporate Data Protection**:
- Work data stored in separate container
- Copy/paste between work and personal apps may be restricted
- Screenshots of corporate data prevented
- Corporate data wiped if device lost/stolen (personal data untouched)

**What MDM Can Do**:
- ✅ View device model, OS version
- ✅ Enforce security policies
- ✅ Remotely wipe corporate data
- ✅ See installed company apps
- ✅ Require device updates

**What MDM Cannot Do**:
- ❌ See personal apps
- ❌ Read personal messages/emails
- ❌ Track location (unless you enable corporate location services)
- ❌ Access personal photos/files
- ❌ Wipe personal data
- ❌ Monitor browsing history

**Corporate Email on Mobile**:

**Best Practices**:
- Use Outlook app (company standard)
- Don't use native mail apps (Mail app on iOS, Gmail on Android)
- Enable MFA for email access
- Don't save password on device
- Use work account only for work emails

**Syncing Options**:
- Email: Last 1 month (adjustable)
- Calendar: Last 6 months
- Contacts: All (synced with company directory)

**Offline Access**:
- Emails: Cached for offline reading
- Attachments: Download as needed
- Calendar: Synced for offline access

**Mobile Security Guidelines**:

**1. Device Security**:
- ✅ Keep OS updated (auto-update recommended)
- ✅ Use strong passcode (6+ digits or alphanumeric)
- ✅ Enable biometric authentication
- ✅ Install apps only from official stores
- ✅ Enable Find My Device
- ✅ Encrypt device (should be default on modern phones)

**2. Network Security**:
- ✅ Avoid public WiFi for work tasks
- ✅ Use VPN when accessing company resources remotely
- ✅ Use cellular data for sensitive tasks if WiFi untrusted
- ✅ Forget WiFi networks when no longer needed

**3. App Security**:
- ✅ Only install company-approved apps for work
- ✅ Review app permissions
- ✅ Keep apps updated
- ✅ Don't install apps from unknown sources
- ❌ Don't sideload apps
- ❌ Don't jailbreak/root device

**Common Issues and Troubleshooting**:

**1. Cannot Receive Email**:
- Check internet connection (WiFi/cellular)
- Verify email account is active (test on PC)
- Check mailbox size (may be full)
- Sign out and back in to Outlook app
- Re-sync account:
  - Outlook > Settings > Account > Remove
  - Add account again

**2. Calendar Not Syncing**:
- Outlook > Settings > Account > Sync
- Enable Calendar sync
- Check sync period (extend if needed)
- Force sync: Pull down to refresh

**3. Cannot Join Teams Meeting**:
- Update Teams app to latest version
- Check microphone/camera permissions:
  - iOS: Settings > Teams > Allow Camera & Microphone
  - Android: Settings > Apps > Teams > Permissions
- Test with test call: Teams > More > Settings > Devices
- Restart app if issues persist

**4. MFA Not Working**:
- Ensure time on device is correct (auto-set)
- Re-install Duo Mobile app
- Use backup codes if you have them
- Contact IT to re-register device

**5. OneDrive Files Not Accessible**:
- Check internet connection
- Sign out and back in to OneDrive app
- Clear app cache:
  - iOS: Offload app and reinstall
  - Android: Settings > Apps > OneDrive > Clear Cache
- Check file permissions (may be restricted)

**6. MDM Compliance Issues**:
- Device flagged as non-compliant:
  - Check email for compliance alert
  - Common reasons:
    - OS version too old (update required)
    - Jailbroken device detected
    - Password policy violation
    - Missing required app
  - Fix issue as indicated
  - Compliance check runs every 24 hours

**7. Device Wipe Notification**:
- Received wipe notification?
  - Don't panic - only corporate data wiped
  - Personal data remains intact
  - Re-enroll device if needed
  - Restore corporate apps

**Device Lost or Stolen**:

**IMMEDIATE ACTIONS** (Within 1 hour):

**1. Report to IT** (Critical - Do this FIRST):
- Call: Ext 4357 or +1-800-COMPANY-IT
- Email: ithelpdesk@company.com (if you have access)
- Provide:
  - Device type (iPhone/Android)
  - When/where lost
  - If it's stolen vs just lost
  - Device identifier (if known)

**2. IT Will Immediately**:
- Trigger remote wipe of corporate data
- Revoke device access to company resources
- Disable email access from device
- Monitor for suspicious activity
- Log security incident

**3. You Should Also**:
- Try to locate device:
  - iOS: iCloud.com > Find My iPhone
  - Android: google.com/android/find
- Change password: https://selfservice.company.com
- Enable lost mode if Find My Device available
- File police report if stolen (required for insurance)

**4. After Device Recovered**:
- Contact IT to re-enable access
- Re-enroll device in MDM
- Change password again (if it was accessed)
- Review account activity for suspicious actions

**Changing Devices**:

**Getting New Personal Device**:
1. **Before Switching**:
   - Backup personal data
   - Note your company apps
   - Have MFA backup codes ready

2. **On Old Device**:
   - Company Portal > Devices > Remove
   - Uninstall company apps
   - Sign out of work accounts

3. **On New Device**:
   - Set up personal settings first
   - Enroll new device (same process as initial)
   - Reinstall company apps
   - Sign in to work accounts

**Leaving Company or Switching to Corporate Device**:
1. Company Portal > Settings > Remove Account
2. Uninstall all company apps
3. Personal data remains on your device
4. Corporate data removed
5. No longer managed by MDM

**Corporate-Owned Devices** (Company-provided phones):

**If Company Provides Phone**:
- Full management by IT
- Company owns device and data
- No expectation of privacy on company device
- Must return upon termination
- Can be wiped remotely at any time
- Subject to audit and monitoring

**Allowed Personal Use**:
- Reasonable personal use permitted
- Subject to company policies
- No illegal or inappropriate content
- Personal apps must be approved

**Corporate Device Policies**:
- Cannot jailbreak/root
- Cannot remove MDM profile
- Must keep password/PIN enabled
- Must report lost/stolen immediately
- Return within 3 days of termination

**Data Usage and Costs**:

**BYOD Devices**:
- You pay for data plan
- Company doesn't reimburse
- Use WiFi when possible to save data
- Download large files on WiFi only

**Corporate Devices**:
- Company pays for plan
- Unlimited data (subject to fair use)
- International roaming requires approval
- Personal use allowed within reason

**Application Access**:

**Available on Mobile**:
- ✅ Email (Outlook)
- ✅ Calendar (Outlook)
- ✅ Teams (chat, meetings)
- ✅ OneDrive (file access)
- ✅ SharePoint (approved sites)
- ✅ Company intranet (browser)

**Not Available on Mobile** (PC only):
- ❌ Full desktop applications
- ❌ Network drives
- ❌ VPN (most resources accessible without it)
- ❌ Some internal tools (security restriction)

**Troubleshooting Decision Tree**:

```
Issue with mobile device?
├─ Cannot access email
│  ├─ Check internet → No connection → Connect to WiFi/Cellular
│  ├─ Account issue → Sign out/in → Still failing → Call IT
│  └─ Mailbox full → Archive emails → Contact IT for quota increase
│
├─ MDM/Compliance issue
│  ├─ Non-compliant alert → Read email → Fix issue → Wait 24h for re-check
│  ├─ Update required → Update OS → May need IT to re-enroll
│  └─ Can't enroll → Jailbroken? → Not allowed → Use corporate device
│
├─ App not working
│  ├─ Update app → Still failing → Reinstall → Still failing → Call IT
│  ├─ Permission denied → Check device settings → Grant permissions
│  └─ Crashes → Clear cache → Reinstall → Report to IT
│
└─ Lost/Stolen device
   └─ CALL IT IMMEDIATELY → Ext 4357 → Remote wipe → Change password → File report
```

**Mobile Access Best Practices**:
- ✅ Use company apps for work (Outlook, Teams, OneDrive)
- ✅ Keep device and apps updated
- ✅ Use strong passcode + biometrics
- ✅ Enable Find My Device
- ✅ Report lost devices immediately (<1 hour)
- ✅ Don't store sensitive data locally
- ✅ Lock device when not in use
- ✅ Be cautious on public WiFi

**Support Resources**:
- MDM Portal: https://mdm.company.com
- App Downloads: Company Portal app
- Self-Service: https://selfservice.company.com
- IT Helpdesk: Ext 4357 or ithelpdesk@company.com
- Emergency (lost device): +1-800-COMPANY-IT (24/7)
- BYOD Policy: https://policy.company.com/byod

**FAQ**:

Q: Can IT see my personal data?
A: No, only corporate data and basic device info (model, OS version)

Q: What happens to personal data if I leave?
A: Only corporate data is wiped, personal data remains

Q: Can I use personal apps?
A: Yes, on BYOD devices you can use any personal apps

Q: Will I get reimbursed for data usage?
A: No, BYOD program doesn't include reimbursement

Q: Can I opt out of MDM?
A: You can opt out, but then cannot access email on mobile device

Q: What if my device is too old to enroll?
A: Request corporate device or use webmail only (mail.company.com)

**Need Help?**
- Enrollment issues: https://mdm.company.com/help
- Device issues: IT Helpdesk Ext 4357
- Lost device: Call +1-800-COMPANY-IT immediately
        """,
        "category": "mobile",
        "tags": ["mobile", "byod", "smartphone", "mdm", "device management", "iphone", "android"]
    }
]


def add_it_support_knowledge():
    """Add IT support knowledge to the system"""
    print("=" * 80)
    print("  ADDING IT SUPPORT KNOWLEDGE BASE FOR MNC")
    print("=" * 80)
    print(f"API URL: {API_URL}")
    print(f"Total documents to add: {len(it_support_knowledge)}")
    print("-" * 80)
    
    success_count = 0
    failed = []
    
    for idx, knowledge in enumerate(it_support_knowledge, 1):
        try:
            print(f"\n[{idx}/{len(it_support_knowledge)}] Adding: {knowledge['title']}")
            print(f"  Category: {knowledge['category']}")
            print(f"  Tags: {', '.join(knowledge['tags'])}")
            print(f"  Content size: {len(knowledge['content'])} characters")
            
            response = requests.post(
                f"{API_URL}/api/knowledge/add",
                json=knowledge,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✓ Success! Document ID: {result['document_ids'][0]}")
                success_count += 1
            else:
                print(f"  ✗ Failed: {response.status_code} - {response.text}")
                failed.append(knowledge['title'])
        
        except requests.exceptions.ConnectionError:
            print(f"\n✗ Cannot connect to API at {API_URL}")
            print("  Make sure the application is running:")
            print("    python main.py")
            return
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed.append(knowledge['title'])
    
    print("\n" + "=" * 80)
    print("  SUMMARY")
    print("=" * 80)
    print(f"✓ Successfully added: {success_count}/{len(it_support_knowledge)} documents")
    
    if failed:
        print(f"\n✗ Failed documents:")
        for title in failed:
            print(f"  - {title}")
    
    print("\n" + "-" * 80)
    print("Categories added:")
    categories = {}
    for doc in it_support_knowledge:
        cat = doc['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    for category, count in sorted(categories.items()):
        print(f"  - {category}: {count} documents")
    
    print("\n" + "-" * 80)
    print("You can now ask questions like:")
    print("  - 'My computer won't start, what should I do?'")
    print("  - 'How do I reset my password?'")
    print("  - 'I think I received a phishing email'")
    print("  - 'How do I connect to the VPN?'")
    print("  - 'My Outlook is very slow'")
    print("  - 'I can't access network drives'")
    print("  - 'How do I set up email on my iPhone?'")
    print("  - 'My laptop battery drains quickly'")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    add_it_support_knowledge()

