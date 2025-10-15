"""
SMS integration using Twilio
"""
from twilio.rest import Client
from typing import Optional
from app.config import settings
from app.database import db_manager, SupportTicket, ConversationMessage
from app.rag_system import rag_system
import uuid


class SMSIntegration:
    """SMS integration for customer support using Twilio"""
    
    def __init__(self):
        # Only initialize if Twilio credentials are provided
        if settings.twilio_account_sid and settings.twilio_auth_token:
            self.client = Client(
                settings.twilio_account_sid,
                settings.twilio_auth_token
            )
            self.phone_number = settings.twilio_phone_number
            self.enabled = True
        else:
            self.client = None
            self.phone_number = None
            self.enabled = False
            print("⚠️  SMS integration disabled - Twilio credentials not configured")
    
    async def send_sms(self, to_phone: str, message: str) -> bool:
        """Send SMS message"""
        if not self.enabled:
            print("⚠️  SMS disabled - Twilio not configured")
            return False
            
        try:
            self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_phone
            )
            print(f"✓ SMS sent to {to_phone}")
            return True
        
        except Exception as e:
            print(f"✗ Error sending SMS: {e}")
            return False
    
    async def process_incoming_sms(
        self,
        from_phone: str,
        message: str,
        message_sid: str
    ):
        """Process incoming SMS message"""
        try:
            # Check if ticket exists for this customer
            existing_tickets = await db_manager.get_tickets_by_customer(from_phone)
            
            if existing_tickets and existing_tickets[0].status == "open":
                # Use existing open ticket
                ticket = existing_tickets[0]
                ticket_id = ticket.ticket_id
            else:
                # Create new ticket
                ticket_id = f"SMS-{uuid.uuid4().hex[:8].upper()}"
                ticket = SupportTicket(
                    ticket_id=ticket_id,
                    channel="sms",
                    customer_identifier=from_phone,
                    subject="SMS Support Request",
                    status="open"
                )
                await db_manager.create_ticket(ticket)
            
            # Add customer message to conversation
            customer_message = ConversationMessage(
                role="user",
                content=message,
                metadata={"phone": from_phone, "message_sid": message_sid}
            )
            await db_manager.add_message_to_ticket(ticket_id, customer_message)
            
            # Get ticket for conversation history
            ticket = await db_manager.get_ticket(ticket_id)
            conversation_history = [
                {"role": msg.role, "content": msg.content}
                for msg in ticket.conversation[-5:]
            ]
            
            # Query RAG system
            rag_response = await rag_system.query(message, conversation_history)
            
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
            
            # Send SMS response if confidence is high
            if rag_response["can_auto_respond"]:
                # Truncate response for SMS (160 char limit consideration)
                response = rag_response["answer"]
                if len(response) > 1600:  # Allow for 10 SMS segments
                    response = response[:1597] + "..."
                
                await self.send_sms(from_phone, response)
                
                # Mark as auto-resolved
                await db_manager.update_ticket(ticket_id, {
                    "auto_resolved": True,
                    "status": "pending"
                })
                
                print(f"✓ Auto-responded to SMS from {from_phone}")
            else:
                # Send message that human will follow up
                await self.send_sms(
                    from_phone,
                    "Thank you for your message. A support agent will respond to you shortly."
                )
                
                await db_manager.update_ticket(ticket_id, {
                    "status": "pending",
                    "priority": "high",
                    "metadata": {"requires_human": True}
                })
                
                print(f"⚠ SMS from {from_phone} requires human review")
        
        except Exception as e:
            print(f"✗ Error processing SMS: {e}")
    
    async def get_recent_messages(self, limit: int = 20):
        """Get recent SMS messages from Twilio"""
        if not self.enabled:
            return []
            
        try:
            messages = self.client.messages.list(limit=limit)
            return [
                {
                    "from": msg.from_,
                    "to": msg.to,
                    "body": msg.body,
                    "date": msg.date_sent,
                    "sid": msg.sid,
                    "direction": msg.direction
                }
                for msg in messages
            ]
        except Exception as e:
            print(f"✗ Error fetching SMS messages: {e}")
            return []


# Global SMS integration instance
sms_integration = SMSIntegration()

