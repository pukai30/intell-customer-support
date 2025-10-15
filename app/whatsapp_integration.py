"""
WhatsApp integration using Twilio WhatsApp Business API
"""
from twilio.rest import Client
from typing import Optional
from app.config import settings
from app.database import db_manager, SupportTicket, ConversationMessage
from app.rag_system import rag_system
import uuid


class WhatsAppIntegration:
    """WhatsApp integration for customer support using Twilio"""
    
    def __init__(self):
        # Only initialize if Twilio credentials are provided
        if settings.twilio_account_sid and settings.twilio_auth_token:
            self.client = Client(
                settings.twilio_account_sid,
                settings.twilio_auth_token
            )
            self.whatsapp_number = settings.twilio_whatsapp_number
            self.enabled = True
        else:
            self.client = None
            self.whatsapp_number = None
            self.enabled = False
            print("⚠️  WhatsApp integration disabled - Twilio credentials not configured")
    
    async def send_whatsapp_message(self, to_phone: str, message: str) -> bool:
        """Send WhatsApp message"""
        if not self.enabled:
            print("⚠️  WhatsApp disabled - Twilio not configured")
            return False
            
        try:
            # Ensure phone number has whatsapp: prefix
            if not to_phone.startswith("whatsapp:"):
                to_phone = f"whatsapp:{to_phone}"
            
            self.client.messages.create(
                body=message,
                from_=self.whatsapp_number,
                to=to_phone
            )
            print(f"✓ WhatsApp message sent to {to_phone}")
            return True
        
        except Exception as e:
            print(f"✗ Error sending WhatsApp message: {e}")
            return False
    
    async def process_incoming_whatsapp(
        self,
        from_phone: str,
        message: str,
        message_sid: str,
        media_url: Optional[str] = None
    ):
        """Process incoming WhatsApp message"""
        try:
            # Remove whatsapp: prefix for storage
            customer_identifier = from_phone.replace("whatsapp:", "")
            
            # Check if ticket exists for this customer
            existing_tickets = await db_manager.get_tickets_by_customer(customer_identifier)
            
            if existing_tickets and existing_tickets[0].status == "open":
                # Use existing open ticket
                ticket = existing_tickets[0]
                ticket_id = ticket.ticket_id
            else:
                # Create new ticket
                ticket_id = f"WHATSAPP-{uuid.uuid4().hex[:8].upper()}"
                ticket = SupportTicket(
                    ticket_id=ticket_id,
                    channel="whatsapp",
                    customer_identifier=customer_identifier,
                    subject="WhatsApp Support Request",
                    status="open"
                )
                await db_manager.create_ticket(ticket)
            
            # Add customer message to conversation
            message_metadata = {
                "phone": from_phone,
                "message_sid": message_sid
            }
            
            if media_url:
                message_metadata["media_url"] = media_url
                message = f"{message}\n[Media attachment: {media_url}]"
            
            customer_message = ConversationMessage(
                role="user",
                content=message,
                metadata=message_metadata
            )
            await db_manager.add_message_to_ticket(ticket_id, customer_message)
            
            # Get ticket for conversation history
            ticket = await db_manager.get_ticket(ticket_id)
            conversation_history = [
                {"role": msg.role, "content": msg.content}
                for msg in ticket.conversation[-5:]
            ]
            
            # Query RAG system (skip if media only)
            if message.strip() or not media_url:
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
                
                # Send WhatsApp response if confidence is high
                if rag_response["can_auto_respond"]:
                    await self.send_whatsapp_message(from_phone, rag_response["answer"])
                    
                    # Mark as auto-resolved
                    await db_manager.update_ticket(ticket_id, {
                        "auto_resolved": True,
                        "status": "pending"
                    })
                    
                    print(f"✓ Auto-responded to WhatsApp from {from_phone}")
                else:
                    # Send message that human will follow up
                    await self.send_whatsapp_message(
                        from_phone,
                        "Thank you for your message. A support agent will respond to you shortly."
                    )
                    
                    await db_manager.update_ticket(ticket_id, {
                        "status": "pending",
                        "priority": "high",
                        "metadata": {"requires_human": True}
                    })
                    
                    print(f"⚠ WhatsApp from {from_phone} requires human review")
            else:
                # Media only message
                await self.send_whatsapp_message(
                    from_phone,
                    "Thank you for sharing. A support agent will review your media and respond shortly."
                )
                
                await db_manager.update_ticket(ticket_id, {
                    "status": "pending",
                    "priority": "medium",
                    "metadata": {"requires_human": True, "has_media": True}
                })
        
        except Exception as e:
            print(f"✗ Error processing WhatsApp message: {e}")
    
    async def get_recent_messages(self, limit: int = 20):
        """Get recent WhatsApp messages from Twilio"""
        if not self.enabled:
            return []
            
        try:
            messages = self.client.messages.list(limit=limit)
            # Filter for WhatsApp messages
            whatsapp_messages = [
                {
                    "from": msg.from_,
                    "to": msg.to,
                    "body": msg.body,
                    "date": msg.date_sent,
                    "sid": msg.sid,
                    "direction": msg.direction,
                    "num_media": msg.num_media
                }
                for msg in messages
                if "whatsapp" in msg.from_.lower() or "whatsapp" in msg.to.lower()
            ]
            return whatsapp_messages
        except Exception as e:
            print(f"✗ Error fetching WhatsApp messages: {e}")
            return []


# Global WhatsApp integration instance
whatsapp_integration = WhatsAppIntegration()

