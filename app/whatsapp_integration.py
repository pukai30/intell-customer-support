"""
WhatsApp integration using Twilio WhatsApp Business API
"""
from datetime import datetime
from twilio.rest import Client
from typing import Optional, List, Dict
from app.config import settings
from app.database import db_manager, SupportTicket, ConversationMessage
from app.rag_system import rag_system
import uuid


class WhatsAppIntegration:
    """WhatsApp integration for customer support using Twilio"""
    
    def __init__(self):
        # Initialize from settings
        self._init_from_settings()
    
    def _init_from_settings(self):
        """Initialize or reinitialize from current settings"""
        # Only initialize if Twilio credentials are provided
        if settings.twilio_account_sid and settings.twilio_auth_token:
            self.client = Client(
                settings.twilio_account_sid,
                settings.twilio_auth_token
            )
            self.whatsapp_number = settings.twilio_whatsapp_number
            self.enabled = True
            print("✓ WhatsApp integration enabled")
        else:
            self.client = None
            self.whatsapp_number = None
            self.enabled = False
            print("⚠️  WhatsApp integration disabled - Twilio credentials not configured")
    
    async def get_processed_message_sids(self) -> List[str]:
        """Get list of already processed message SIDs from database"""
        try:
            # Get all WhatsApp tickets and extract message SIDs from metadata
            whatsapp_tickets = await db_manager.get_tickets_by_channel("whatsapp")
            processed_sids = set()
            
            for ticket in whatsapp_tickets:
                if ticket.conversation:
                    for msg in ticket.conversation:
                        if msg.metadata and "message_sid" in msg.metadata:
                            processed_sids.add(msg.metadata["message_sid"])
            
            return list(processed_sids)
        except Exception as e:
            print(f"✗ Error getting processed message SIDs: {e}")
            return []
    
    async def check_new_whatsapp_messages(self, since_minutes: int = 5):
        """Check for new unread WhatsApp messages only"""
        if not self.enabled:
            return []
        
        try:
            print(f"\n{'=' * 80}")
            print(f"  CHECKING UNREAD WHATSAPP MESSAGES FROM TWILIO")
            print(f"{'=' * 80}")
            print(f"Listening on: {self.whatsapp_number}")
            print()
            
            # Get list of already processed message SIDs
            processed_sids = await self.get_processed_message_sids()
            print(f"   ℹ️  Found {len(processed_sids)} already processed message(s)")
            
            # Get messages sent TO your WhatsApp number (incoming messages)
            messages = self.client.messages.list(
                to=self.whatsapp_number,
                limit=50
            )
            
            unread_messages = []
            message_count = 0
            skipped_count = 0
            
            if not messages:
                print("   ℹ️  No messages found for your WhatsApp number")
            else:
                print(f"   ✓ Found {len(messages)} message(s) for {self.whatsapp_number}\n")
                
                for msg in messages:
                    message_count += 1
                    
                    # Skip if already processed
                    if msg.sid in processed_sids:
                        skipped_count += 1
                        print(f"   Message #{message_count}: SID {msg.sid[:20]}... (already processed, skipping)")
                        continue
                    
                    print(f"   Message #{message_count}: NEW")
                    print(f"      From: {msg.from_}")
                    print(f"      To: {msg.to}")
                    print(f"      Date: {msg.date_sent}")
                    print(f"      Status: {msg.status}")
                    print(f"      SID: {msg.sid}")
                    
                    # Only process messages with body content for ticket creation
                    if msg.body:
                        print(f"      📝 Message Body: {msg.body[:100]}...")
                        unread_messages.append({
                            "from_phone": msg.from_,
                            "message": msg.body,
                            "message_sid": msg.sid,
                            "date_sent": msg.date_sent,
                            "num_media": msg.num_media if hasattr(msg, 'num_media') else 0,
                            "direction": msg.direction if hasattr(msg, 'direction') else "inbound",
                            "status": msg.status if hasattr(msg, 'status') else "received"
                        })
                        print(f"      ✓ Message added to processing queue")
                    else:
                        print(f"      ⚠️  Message has no body content (media only?)")
                    
                    print()
            
            print(f"\n   ✓ Total messages: {message_count}")
            print(f"   ✓ Unread messages: {len(unread_messages)}")
            print(f"   ✓ Skipped (already processed): {skipped_count}\n")
            
            return unread_messages
        
        except Exception as e:
            print(f"✗ Error checking WhatsApp messages: {e}")
            import traceback
            traceback.print_exc()
            return []
    
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
    
    async def get_recent_context_messages(self, customer_identifier: str, limit: int = 3) -> List[str]:
        """Get last N messages from customer to check conversation context"""
        try:
            # Get recent tickets from this customer
            tickets = await db_manager.get_tickets_by_customer(customer_identifier)
            
            recent_messages = []
            for ticket in tickets:
                if ticket.conversation:
                    for msg in ticket.conversation:
                        if msg.role == "user":  # Only customer messages
                            recent_messages.append(msg.content)
                            if len(recent_messages) >= limit:
                                break
                
                if len(recent_messages) >= limit:
                    break
            
            return recent_messages[:limit]
        except Exception as e:
            print(f"✗ Error getting recent context messages: {e}")
            return []
    
    async def check_message_related_to_context(self, new_message: str, context_messages: List[str]) -> bool:
        """Check if new message is related to conversation context"""
        if not context_messages:
            return False
        
        # Simple check: if new message contains keywords from context or is very short (likely continuation)
        new_message_lower = new_message.lower()
        
        # Check for common continuation keywords
        continuation_keywords = ["yes", "no", "ok", "thanks", "thank you", "okay", "sure", "ok", "yep", "nope", "correct", "right", "wrong"]
        if new_message_lower.strip() in continuation_keywords:
            return True
        
        # If message is very short (likely a follow-up)
        if len(new_message.split()) <= 3:
            return True
        
        # Check for shared keywords with recent messages
        new_words = set(new_message_lower.split())
        for context_msg in context_messages:
            context_words = set(context_msg.lower().split())
            # If message shares significant words with context, likely related
            if len(new_words & context_words) >= 2:
                return True
        
        return False
    
    async def process_incoming_whatsapp(
        self,
        from_phone: str,
        message: str,
        message_sid: str,
        media_url: Optional[str] = None
    ):
        """Process incoming WhatsApp message with context-aware threading"""
        try:
            # Remove whatsapp: prefix for storage
            customer_identifier = from_phone.replace("whatsapp:", "")
            
            print(f"\n📱 Processing WhatsApp message from {customer_identifier}")
            print(f"   Message: {message[:100]}...")
            
            # Get last 3 messages from this customer for context
            recent_messages = await self.get_recent_context_messages(customer_identifier, limit=3)
            
            if recent_messages:
                print(f"   Found {len(recent_messages)} recent message(s) from this customer")
                print(f"   Checking if message is related to context...")
                
                is_related = await self.check_message_related_to_context(message, recent_messages)
                
                if is_related:
                    print(f"   ✓ Message is related to previous context")
                    # Continue in existing ticket
                    existing_tickets = await db_manager.get_tickets_by_customer(customer_identifier)
                    if existing_tickets:
                        # Find most recent active ticket
                        for ticket in existing_tickets:
                            if ticket.status in ["open", "pending", "in_progress"]:
                                ticket_id = ticket.ticket_id
                                print(f"   → Continuing in existing ticket: {ticket_id}")
                                break
                        else:
                            # No active ticket, create new one
                            ticket_id = f"WHATSAPP-{uuid.uuid4().hex[:8].upper()}"
                            ticket = SupportTicket(
                                ticket_id=ticket_id,
                                channel="whatsapp",
                                customer_identifier=customer_identifier,
                                subject="WhatsApp Support Request (Continued)",
                                status="open"
                            )
                            await db_manager.create_ticket(ticket)
                            print(f"   → Created new ticket for continued conversation: {ticket_id}")
                    else:
                        # No existing tickets, create new one
                        ticket_id = f"WHATSAPP-{uuid.uuid4().hex[:8].upper()}"
                        ticket = SupportTicket(
                            ticket_id=ticket_id,
                            channel="whatsapp",
                            customer_identifier=customer_identifier,
                            subject="WhatsApp Support Request (Continued)",
                            status="open"
                        )
                        await db_manager.create_ticket(ticket)
                        print(f"   → Created new ticket for continued conversation: {ticket_id}")
                else:
                    print(f"   ✗ Message is unrelated to previous context")
                    print(f"   → Creating NEW ticket")
                    # Create new ticket for unrelated message
                    ticket_id = f"WHATSAPP-{uuid.uuid4().hex[:8].upper()}"
                    ticket = SupportTicket(
                        ticket_id=ticket_id,
                        channel="whatsapp",
                        customer_identifier=customer_identifier,
                        subject="WhatsApp Support Request",
                        status="open"
                    )
                    await db_manager.create_ticket(ticket)
                    print(f"   → Created new ticket: {ticket_id}")
            else:
                print(f"   No recent messages from this customer")
                print(f"   → Creating new ticket")
                # No recent messages, create new ticket
                ticket_id = f"WHATSAPP-{uuid.uuid4().hex[:8].upper()}"
                ticket = SupportTicket(
                    ticket_id=ticket_id,
                    channel="whatsapp",
                    customer_identifier=customer_identifier,
                    subject="WhatsApp Support Request",
                    status="open"
                )
                await db_manager.create_ticket(ticket)
                print(f"   → Created new ticket: {ticket_id}")
            
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
            
            # Check if we already sent the "agent will review" message for this ticket
            already_notified = False
            if ticket.conversation:
                for msg in ticket.conversation:
                    if (msg.role == "assistant" and 
                        msg.content and 
                        "support agent will review" in msg.content.lower()):
                        already_notified = True
                        print(f"   ℹ️  Customer already notified about agent review - skipping notification")
                        break
            
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
                    # Low confidence - requires human agent
                    # Send notification only if not already sent
                    if not already_notified:
                        # Get config to customize the message
                        config = await db_manager.get_system_config()
                        agent_message = "A support agent will review your query and respond to you shortly."
                        
                        if config and not config.whatsapp_enabled:
                            agent_message = "Thank you for contacting IT Support. Someone will respond to your query shortly."
                        
                        await self.send_whatsapp_message(from_phone, agent_message)
                        
                        # Add notification message to conversation
                        notification_message = ConversationMessage(
                            role="assistant",
                            content=agent_message,
                            metadata={"auto_notification": True}
                        )
                        await db_manager.add_message_to_ticket(ticket_id, notification_message)
                        print(f"   ✓ Sent agent review notification to customer")
                    
                    # Try to auto-assign to agent
                    from app.auto_assignment import auto_assignment
                    assignment_result = await auto_assignment.auto_assign_ticket(
                        ticket_id=ticket_id,
                        subject=ticket.subject,
                        body=message,
                        channel="whatsapp"
                    )
                    
                    update_data = {
                        "status": "pending",
                        "priority": "high",
                        "metadata": {"requires_human": True}
                    }
                    
                    if assignment_result and assignment_result["assigned"]:
                        update_data["assigned_to"] = assignment_result["agent_email"]
                        update_data["assigned_at"] = datetime.utcnow()
                        print(f"✓ WhatsApp ticket {ticket_id} auto-assigned to {assignment_result['agent_name']}")
                    else:
                        update_data["requires_human"] = True
                        print(f"⚠ WhatsApp from {from_phone} requires human review")
                    
                    await db_manager.update_ticket(ticket_id, update_data)
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

