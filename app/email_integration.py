"""
Email integration for receiving and sending support emails
"""
import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from imap_tools import MailBox, AND
from datetime import datetime, timedelta
from typing import List, Optional
from app.config import settings
from app.database import db_manager, SupportTicket, ConversationMessage
from app.rag_system import rag_system
import uuid


class EmailIntegration:
    """Email integration for customer support"""
    
    def __init__(self):
        self.smtp_host = settings.email_host
        self.smtp_port = settings.email_port
        self.imap_host = settings.imap_host
        self.imap_port = settings.imap_port
        self.email_user = settings.email_user
        self.email_password = settings.email_password
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        reply_to: Optional[str] = None
    ):
        """Send an email response"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if reply_to:
                msg['In-Reply-To'] = reply_to
                msg['References'] = reply_to
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self._send_smtp_email,
                msg
            )
            
            print(f"✓ Email sent to {to_email}")
            return True
        
        except Exception as e:
            print(f"✗ Error sending email: {e}")
            return False
    
    def _send_smtp_email(self, msg: MIMEMultipart):
        """Send email via SMTP (blocking operation)"""
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.email_user, self.email_password)
            server.send_message(msg)
    
    async def check_new_emails(self, since_minutes: int = 5) -> List[dict]:
        """Check for new emails"""
        try:
            since_date = datetime.now() - timedelta(minutes=since_minutes)
            
            # Run IMAP operations in thread pool
            loop = asyncio.get_event_loop()
            emails = await loop.run_in_executor(
                None,
                self._fetch_emails_imap,
                since_date
            )
            
            return emails
        
        except Exception as e:
            print(f"✗ Error checking emails: {e}")
            return []
    
    def _fetch_emails_imap(self, since_date: datetime) -> List[dict]:
        """Fetch emails via IMAP (blocking operation)"""
        emails = []
        
        with MailBox(self.imap_host).login(
            self.email_user,
            self.email_password
        ) as mailbox:
            # Fetch unseen messages
            for msg in mailbox.fetch(
                AND(date_gte=since_date.date(), seen=False)
            ):
                emails.append({
                    'from': msg.from_,
                    'subject': msg.subject,
                    'body': msg.text or msg.html,
                    'date': msg.date,
                    'message_id': msg.uid
                })
        
        return emails
    
    async def process_email(self, email_data: dict):
        """Process an incoming email and generate response"""
        try:
            customer_email = email_data['from']
            subject = email_data['subject']
            body = email_data['body']
            
            # Check if ticket exists for this EXACT subject (to avoid mixing different issues)
            existing_tickets = await db_manager.get_tickets_by_customer(customer_email)
            
            # ONLY reuse ticket if EXACT same subject and still open (same conversation thread)
            existing_ticket = next(
                (t for t in existing_tickets if t.subject == subject and t.status == "open"),
                None
            )
            
            if existing_ticket:
                # Same subject, same open ticket - continue conversation
                ticket_id = existing_ticket.ticket_id
                print(f"  → Continuing existing ticket {ticket_id} (same subject)")
            else:
                # Different subject or no open ticket - create NEW ticket (prevent context mixing)
                ticket_id = f"EMAIL-{uuid.uuid4().hex[:8].upper()}"
                ticket = SupportTicket(
                    ticket_id=ticket_id,
                    channel="email",
                    customer_identifier=customer_email,
                    subject=subject,
                    status="open"
                )
                await db_manager.create_ticket(ticket)
                print(f"  → Created new ticket {ticket_id} (new subject: {subject})")
            
            # Add customer message to conversation
            customer_message = ConversationMessage(
                role="user",
                content=body,
                metadata={"email": customer_email, "subject": subject}
            )
            await db_manager.add_message_to_ticket(ticket_id, customer_message)
            
            # Get ticket for conversation history
            ticket = await db_manager.get_ticket(ticket_id)
            
            # IMPORTANT: Only use conversation history if more than 1 message in THIS ticket
            # This prevents context bleeding from unrelated previous tickets
            conversation_history = []
            if len(ticket.conversation) > 1:  # More than just the current message
                # Get last 3 messages (exclude current one) for context
                conversation_history = [
                    {"role": msg.role, "content": msg.content}
                    for msg in ticket.conversation[-4:-1]  # Last 3 messages before current
                ]
                print(f"  → Using {len(conversation_history)} previous messages for context")
            else:
                print(f"  → First message in ticket - no conversation history used (fresh context)")
            
            # Query RAG system with appropriate context
            rag_response = await rag_system.query(body, conversation_history)
            
            # Log RAG response details
            print(f"  → RAG Analysis:")
            print(f"     - Confidence: {rag_response['confidence']:.2f}")
            print(f"     - Can auto-respond: {rag_response['can_auto_respond']}")
            print(f"     - Answer preview: {rag_response['answer'][:100]}...")
            
            # Add assistant response to conversation
            assistant_message = ConversationMessage(
                role="assistant",
                content=rag_response["answer"],
                metadata={
                    "confidence": rag_response["confidence"],
                    "auto_generated": True
                }
            )
            await db_manager.add_message_to_ticket(ticket_id, assistant_message)
            
            # Send email response if confidence is high
            if rag_response["can_auto_respond"]:
                response_subject = f"Re: {subject}" if not subject.startswith("Re:") else subject
                await self.send_email(
                    to_email=customer_email,
                    subject=response_subject,
                    body=rag_response["answer"],
                    reply_to=email_data.get('message_id')
                )
                
                # Mark as auto-resolved if appropriate
                await db_manager.update_ticket(ticket_id, {
                    "auto_resolved": True,
                    "status": "pending"
                })
                
                print(f"✓ Auto-responded to email from {customer_email}")
            else:
                # Low confidence - try to auto-assign to skilled agent
                print(f"  → Low confidence - attempting auto-assignment...")
                from app.auto_assignment import auto_assignment
                
                assignment_result = await auto_assignment.auto_assign_ticket(
                    ticket_id=ticket_id,
                    subject=subject,
                    body=body,
                    channel="email"
                )
                
                if assignment_result and assignment_result["assigned"]:
                    print(f"✓ Email from {customer_email} auto-assigned to {assignment_result['agent_name']}")
                    print(f"  → Agent: {assignment_result['agent_email']}")
                    print(f"  → Skills matched: {assignment_result.get('skills_matched', [])}")
                    print(f"  → Current load: {assignment_result.get('current_load', 0)} tickets")
                else:
                    # No agent available - mark for manual review
                    await db_manager.update_ticket(ticket_id, {
                        "status": "pending",
                        "priority": "high",
                        "requires_human": True
                    })
                    reason = assignment_result.get("reason", "no agent available") if assignment_result else "no agent available"
                    print(f"⚠ Email from {customer_email} requires human review")
                    print(f"  → Reason: {reason}")
        
        except Exception as e:
            print(f"✗ Error processing email: {e}")


# Global email integration instance
email_integration = EmailIntegration()

