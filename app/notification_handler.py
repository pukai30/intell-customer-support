"""
Notification handler for sending channel-specific notifications to customers
"""
from datetime import datetime
from typing import Dict, Any
from app.database import db_manager, SupportTicket
from app.email_integration import email_integration
from app.sms_integration import sms_integration
from app.whatsapp_integration import whatsapp_integration


class NotificationHandler:
    """Handle sending notifications to customers when their complaint requires human agent"""
    
    async def send_channel_notification(
        self,
        ticket_id: str,
        customer_identifier: str,
        message: str,
        channel: str
    ) -> bool:
        """
        Send notification to customer via the same channel as their complaint
        
        Args:
            ticket_id: Ticket ID
            customer_identifier: Customer email/phone number
            message: Notification message
            channel: Communication channel (email, sms, whatsapp)
        
        Returns:
            True if notification sent successfully
        """
        try:
            if channel == "email":
                return await self._send_email_notification(
                    customer_identifier,
                    message,
                    ticket_id
                )
            elif channel == "sms":
                return await self._send_sms_notification(
                    customer_identifier,
                    message
                )
            elif channel == "whatsapp":
                return await self._send_whatsapp_notification(
                    customer_identifier,
                    message
                )
            else:
                print(f"⚠ Unsupported channel: {channel}")
                return False
        
        except Exception as e:
            print(f"✗ Error sending {channel} notification: {e}")
            return False
    
    async def _send_email_notification(
        self,
        customer_email: str,
        message: str,
        ticket_id: str
    ) -> bool:
        """Send email notification to customer"""
        try:
            subject = f"Support Ticket #{ticket_id} - We Received Your Complaint"
            
            email_body = f"""
            Dear Customer,
            
            We have received your complaint and created support ticket #{ticket_id}.
            
            {message}
            
            One of our support agents will respond to your inquiry shortly. You will receive updates at this email address.
            
            Thank you for contacting us.
            
            Best regards,
            Support Team
            """
            
            # Get config to use proper email settings
            config = await db_manager.get_system_config()
            
            success = await email_integration.send_email(
                to_email=customer_email,
                subject=subject,
                body=email_body
            )
            
            if success:
                print(f"✓ Email notification sent to {customer_email}")
                return True
            else:
                print(f"✗ Failed to send email notification to {customer_email}")
                return False
        
        except Exception as e:
            print(f"✗ Error in email notification: {e}")
            return False
    
    async def _send_sms_notification(
        self,
        customer_phone: str,
        message: str
    ) -> bool:
        """Send SMS notification to customer"""
        try:
            full_message = f"Support: {message}"
            
            success = await sms_integration.send_sms(
                to=customer_phone,
                body=full_message
            )
            
            if success:
                print(f"✓ SMS notification sent to {customer_phone}")
                return True
            else:
                print(f"✗ Failed to send SMS notification to {customer_phone}")
                return False
        
        except Exception as e:
            print(f"✗ Error in SMS notification: {e}")
            return False
    
    async def _send_whatsapp_notification(
        self,
        customer_phone: str,
        message: str
    ) -> bool:
        """Send WhatsApp notification to customer"""
        try:
            full_message = f"Support: {message}"
            
            success = await whatsapp_integration.send_whatsapp(
                to=customer_phone,
                body=full_message
            )
            
            if success:
                print(f"✓ WhatsApp notification sent to {customer_phone}")
                return True
            else:
                print(f"✗ Failed to send WhatsApp notification to {customer_phone}")
                return False
        
        except Exception as e:
            print(f"✗ Error in WhatsApp notification: {e}")
            return False
    
    async def notify_human_agent_required(
        self,
        ticket: SupportTicket,
        reason: str = "Your request requires human agent attention"
    ) -> bool:
        """
        Send notification to customer that their complaint was received and requires human agent
        
        Args:
            ticket: The support ticket
            reason: Optional reason for requiring human agent
        
        Returns:
            True if notification sent successfully
        """
        try:
            # Determine notification message based on ticket status
            if ticket.assigned_to:
                message = f"{reason}. Your complaint has been assigned to our support team and an agent will respond soon."
            else:
                message = f"{reason}. We have received your complaint and our support team will respond shortly."
            
            # Send notification via the same channel as the ticket
            success = await self.send_channel_notification(
                ticket_id=ticket.ticket_id,
                customer_identifier=ticket.customer_identifier,
                message=message,
                channel=ticket.channel
            )
            
            if success:
                # Update ticket metadata to indicate notification was sent
                metadata = ticket.metadata or {}
                metadata["customer_notified"] = True
                metadata["notification_sent_at"] = datetime.utcnow().isoformat()
                
                await db_manager.update_ticket(ticket.ticket_id, {
                    "metadata": metadata,
                    "notification_sent": True,
                    "notification_sent_at": datetime.utcnow()
                })
                
                print(f"✓ Customer notification sent for ticket {ticket.ticket_id}")
            
            return success
        
        except Exception as e:
            print(f"✗ Error notifying customer for ticket {ticket.ticket_id}: {e}")
            return False


# Global notification handler instance
notification_handler = NotificationHandler()

