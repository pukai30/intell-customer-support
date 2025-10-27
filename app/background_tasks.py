"""
Background tasks for monitoring email and message channels
"""
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from app.email_integration import email_integration
from app.whatsapp_integration import whatsapp_integration


class BackgroundTaskManager:
    """Manage background tasks for monitoring channels"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
    
    async def check_emails_task(self):
        """Background task to check for new emails"""
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking for new emails...")
            emails = await email_integration.check_new_emails(since_minutes=5)
            
            if emails:
                print(f"✓ Found {len(emails)} new email(s)")
                for email in emails:
                    await email_integration.process_email(email)
            else:
                print("  No new emails")
        
        except Exception as e:
            print(f"✗ Error in email check task: {e}")
    
    async def check_whatsapp_task(self):
        """Background task to check for new WhatsApp messages"""
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking for new WhatsApp messages...")
            
            # Reinitialize to ensure settings are up to date
            whatsapp_integration._init_from_settings()
            
            if not whatsapp_integration.enabled:
                print("  WhatsApp integration disabled - skipping")
                return
            
            messages = await whatsapp_integration.check_new_whatsapp_messages(since_minutes=5)
            
            if messages:
                print(f"✓ Found {len(messages)} new WhatsApp message(s)")
                for msg in messages:
                    await whatsapp_integration.process_incoming_whatsapp(
                        from_phone=msg["from_phone"],
                        message=msg["message"],
                        message_sid=msg["message_sid"],
                        media_url=None
                    )
            else:
                print("  No new WhatsApp messages found")
        
        except Exception as e:
            print(f"✗ Error in WhatsApp check task: {e}")
            import traceback
            traceback.print_exc()
    
    async def cleanup_old_tickets_task(self):
        """Background task to cleanup old resolved tickets (optional)"""
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Running cleanup task...")
            # Add cleanup logic here if needed
            # For example: archive tickets older than 30 days
        except Exception as e:
            print(f"✗ Error in cleanup task: {e}")
    
    async def cleanup_expired_knowledge_task(self):
        """Background task to deactivate expired temporary knowledge"""
        try:
            from app.database import db_manager
            from app.rag_system import rag_system
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking for expired knowledge...")
            
            # Get expired documents
            expired_docs = await db_manager.get_expired_knowledge_documents()
            
            if expired_docs:
                print(f"Found {len(expired_docs)} expired document(s)")
                
                for doc in expired_docs:
                    # Delete from knowledge base
                    await rag_system.delete_document_from_knowledge_base(
                        str(doc.id),
                        hard_delete=False
                    )
                    print(f"  ✓ Deactivated expired document: {doc.title}")
            else:
                print("  No expired documents found")
        
        except Exception as e:
            print(f"✗ Error in expired knowledge cleanup task: {e}")
    
    # SLA monitoring and escalation - Commented out
    # async def sla_monitoring_task(self):
    #     """Background task to monitor SLAs and escalate tickets"""
    #     try:
    #         from app.escalation_system import escalation_system
    #         
    #         print(f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring SLAs...")
    #         
    #         # Check and escalate tickets
    #         escalated_count = await escalation_system.check_and_escalate_tickets()
    #         
    #         if escalated_count == 0:
    #             print("  All tickets within SLA")
    #     
    #     except Exception as e:
    #         print(f"✗ Error in SLA monitoring task: {e}")
    
    def start(self):
        """Start background tasks"""
        if self.is_running:
            print("⚠ Background tasks already running")
            return
        
        # Schedule email checking every 2 minutes
        self.scheduler.add_job(
            self.check_emails_task,
            trigger=IntervalTrigger(minutes=2),
            id="check_emails",
            name="Check for new emails",
            replace_existing=True
        )
        
        # Schedule WhatsApp checking every 2 minutes
        '''self.scheduler.add_job(
            self.check_whatsapp_task,
            trigger=IntervalTrigger(minutes=2),
            id="check_whatsapp",
            name="Check for new WhatsApp messages",
            replace_existing=True
        )'''
        
        # Schedule cleanup every 6 hours
        self.scheduler.add_job(
            self.cleanup_old_tickets_task,
            trigger=IntervalTrigger(hours=6),
            id="cleanup_tickets",
            name="Cleanup old tickets",
            replace_existing=True
        )
        
        # Schedule expired knowledge cleanup every hour
        self.scheduler.add_job(
            self.cleanup_expired_knowledge_task,
            trigger=IntervalTrigger(hours=1),
            id="cleanup_expired_knowledge",
            name="Cleanup expired knowledge",
            replace_existing=True
        )
        
        # SLA monitoring and escalation - Commented out
        # self.scheduler.add_job(
        #     self.sla_monitoring_task,
        #     trigger=IntervalTrigger(minutes=5),
        #     id="sla_monitoring",
        #     name="SLA monitoring and escalation",
        #     replace_existing=True
        # )
        
        self.scheduler.start()
        self.is_running = True
        print("✓ Background tasks started")
        print("  - Email monitoring: Every 2 minutes")
        print("  - WhatsApp monitoring: Every 2 minutes")
        # print("  - SLA monitoring & escalation: Every 5 minutes")  # Commented out
        print("  - Expired knowledge cleanup: Every hour")
        print("  - General cleanup: Every 6 hours")
    
    def stop(self):
        """Stop background tasks"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            self.is_running = False
            print("✓ Background tasks stopped")


# Global background task manager instance
background_tasks = BackgroundTaskManager()

