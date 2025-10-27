"""
FastAPI application and routes
"""
from fastapi import FastAPI, HTTPException, Request, Form, UploadFile, File, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import uuid
import aiofiles
import os
from pathlib import Path

from app.config import settings
from app.database import db_manager, SupportTicket, ConversationMessage, Agent, SystemConfiguration
from app.rag_system import rag_system
from app.email_integration import email_integration
from app.sms_integration import sms_integration
from app.whatsapp_integration import whatsapp_integration
from app.auto_assignment import auto_assignment


# Pydantic models for API
class ChatRequest(BaseModel):
    message: str
    customer_identifier: str
    customer_name: Optional[str] = None
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    confidence: float
    timestamp: datetime


class AddKnowledgeRequest(BaseModel):
    title: str
    content: str
    category: str = "general"
    tags: List[str] = []
    source: Optional[str] = None
    is_temporary: bool = False
    expires_in_days: Optional[int] = None
    created_by: Optional[str] = None


class UpdateKnowledgeRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None


class KnowledgeDocumentResponse(BaseModel):
    id: str
    title: str
    content: str
    category: str
    tags: List[str]
    file_name: Optional[str]
    file_type: Optional[str]
    is_active: bool
    is_temporary: bool
    expires_at: Optional[datetime]
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime


class TicketResponse(BaseModel):
    ticket_id: str
    channel: str
    customer_identifier: str
    status: str
    subject: Optional[str]
    created_at: datetime
    conversation: List[Dict[str, Any]]


# Create FastAPI app
app = FastAPI(
    title="Intelligent Customer Support API",
    description="RAG-based customer support system with multi-channel integration",
    version="1.0.0"
)

# CORS middleware for NextJS frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("🚀 Starting Intelligent Customer Support System...")
    
    # Connect to database
    await db_manager.connect()
    
    # Initialize system configuration if it doesn't exist
    config = await db_manager.get_system_config()
    if not config:
        print("📝 Creating default system configuration...")
        default_config = SystemConfiguration(
            config_id="system_config",
            support_email="r15528850@gmail.com",
            email_host="smtp.gmail.com",
            email_port=587,
            twilio_phone_number="+14155238886",
            whatsapp_number="whatsapp:+14155238886",
            whatsapp_enabled=True,
            sms_enabled=False,
            chat_enabled=True
        )
        await db_manager.update_system_config(default_config)
        print("✓ Default system configuration created")
    else:
        print("✓ System configuration found")
    
    # Initialize RAG system
    await rag_system.initialize()
    
    # Start background tasks (must be after event loop is running)
    from app.background_tasks import background_tasks
    background_tasks.start()
    
    print("✅ System ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    from app.background_tasks import background_tasks
    background_tasks.stop()
    await db_manager.disconnect()
    print("👋 System shutdown complete")


# Health check
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Intelligent Customer Support API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "rag_system": "initialized",
        "timestamp": datetime.utcnow()
    }


# Chat endpoints
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for web interface
    """
    try:
        # Get or create ticket
        if request.conversation_id:
            ticket = await db_manager.get_ticket(request.conversation_id)
            if not ticket:
                raise HTTPException(status_code=404, detail="Conversation not found")
            ticket_id = request.conversation_id
        else:
            # Create new ticket
            ticket_id = f"CHAT-{uuid.uuid4().hex[:8].upper()}"
            ticket = SupportTicket(
                ticket_id=ticket_id,
                channel="chat",
                customer_identifier=request.customer_identifier,
                customer_name=request.customer_name,
                subject="Web Chat Support",
                status="open"
            )
            await db_manager.create_ticket(ticket)
        
        # Add customer message
        customer_message = ConversationMessage(
            role="user",
            content=request.message,
            metadata={"customer_name": request.customer_name}
        )
        await db_manager.add_message_to_ticket(ticket_id, customer_message)
        
        # Get conversation history
        ticket = await db_manager.get_ticket(ticket_id)
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in ticket.conversation[-5:]
        ]
        
        # Query RAG system
        rag_response = await rag_system.query(request.message, conversation_history)
        
        # Add assistant response
        assistant_message = ConversationMessage(
            role="assistant",
            content=rag_response["answer"],
            metadata={
                "confidence": rag_response["confidence"],
                "auto_generated": True
            }
        )
        await db_manager.add_message_to_ticket(ticket_id, assistant_message)
        
        return ChatResponse(
            response=rag_response["answer"],
            conversation_id=ticket_id,
            confidence=rag_response["confidence"],
            timestamp=datetime.utcnow()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Webhook endpoints for Twilio
@app.post("/api/webhooks/sms")
async def sms_webhook(
    From: str = Form(...),
    Body: str = Form(...),
    MessageSid: str = Form(...)
):
    """Webhook for incoming SMS messages"""
    try:
        await sms_integration.process_incoming_sms(From, Body, MessageSid)
        return JSONResponse(content={"status": "received"})
    except Exception as e:
        print(f"Error in SMS webhook: {e}")
        return JSONResponse(content={"status": "error"}, status_code=500)


@app.post("/api/webhooks/whatsapp")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...),
    MessageSid: str = Form(...),
    MediaUrl0: Optional[str] = Form(None)
):
    """Webhook for incoming WhatsApp messages"""
    try:
        await whatsapp_integration.process_incoming_whatsapp(
            From, Body, MessageSid, MediaUrl0
        )
        return JSONResponse(content={"status": "received"})
    except Exception as e:
        print(f"Error in WhatsApp webhook: {e}")
        return JSONResponse(content={"status": "error"}, status_code=500)


@app.post("/api/whatsapp/check-messages")
async def check_whatsapp_messages_on_demand():
    """On-demand endpoint to check for new WhatsApp messages"""
    try:
        messages = await whatsapp_integration.check_new_whatsapp_messages(since_minutes=10)
        
        processed_count = 0
        for msg in messages:
            await whatsapp_integration.process_incoming_whatsapp(
                from_phone=msg["from_phone"],
                message=msg["message"],
                message_sid=msg["message_sid"],
                media_url=None
            )
            processed_count += 1
        
        return {
            "status": "success",
            "messages_found": len(messages),
            "messages_processed": processed_count
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Knowledge base management
@app.post("/api/knowledge/add")
async def add_knowledge(request: AddKnowledgeRequest):
    """Add document to knowledge base"""
    try:
        doc_ids = await rag_system.add_documents_to_knowledge_base(
            documents=[{
                "title": request.title,
                "content": request.content,
                "tags": request.tags,
                "source": request.source
            }],
            category=request.category,
            is_temporary=request.is_temporary,
            expires_in_days=request.expires_in_days,
            created_by=request.created_by
        )
        
        return {
            "status": "success",
            "document_ids": doc_ids,
            "message": "Document added to knowledge base",
            "is_temporary": request.is_temporary,
            "expires_in_days": request.expires_in_days if request.is_temporary else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/knowledge/upload")
async def upload_knowledge_file(
    file: UploadFile = File(...),
    category: str = Form("general"),
    tags: str = Form(""),
    is_temporary: bool = Form(False),
    expires_in_days: Optional[int] = Form(None),
    created_by: Optional[str] = Form(None)
):
    """Upload a file to knowledge base (PDF, DOCX, TXT)"""
    try:
        # Validate file type
        allowed_extensions = {".pdf", ".docx", ".txt"}
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not supported. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Create upload directory if not exists
        upload_dir = Path(settings.knowledge_base_path) / "uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file
        file_path = upload_dir / f"{uuid.uuid4().hex}_{file.filename}"
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Extract content based on file type
        from PyPDF2 import PdfReader
        from docx import Document as DocxDocument
        
        if file_ext == ".pdf":
            reader = PdfReader(str(file_path))
            file_content = "\n".join([page.extract_text() for page in reader.pages])
        elif file_ext == ".docx":
            doc = DocxDocument(str(file_path))
            file_content = "\n".join([para.text for para in doc.paragraphs])
        else:  # .txt
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
        
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
        
        # Add to knowledge base
        doc_ids = await rag_system.add_documents_to_knowledge_base(
            documents=[{
                "title": Path(file.filename).stem,
                "content": file_content,
                "tags": tag_list,
                "source": str(file_path),
                "file_name": file.filename,
                "file_type": file_ext.replace(".", "")
            }],
            category=category,
            is_temporary=is_temporary,
            expires_in_days=expires_in_days,
            created_by=created_by
        )
        
        return {
            "status": "success",
            "document_id": doc_ids[0] if doc_ids else None,
            "file_name": file.filename,
            "file_type": file_ext,
            "category": category,
            "is_temporary": is_temporary,
            "expires_in_days": expires_in_days,
            "message": f"File '{file.filename}' uploaded successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/knowledge/list")
async def list_knowledge_documents(
    category: Optional[str] = Query(None),
    include_inactive: bool = Query(False),
    limit: int = Query(100)
):
    """List all knowledge base documents"""
    try:
        if category:
            docs = await db_manager.get_knowledge_by_category(category)
        else:
            docs = await db_manager.get_all_knowledge_documents(include_inactive=include_inactive)
        
        # Limit results
        docs = docs[:limit]
        
        return {
            "status": "success",
            "count": len(docs),
            "documents": [
                {
                    "id": str(doc.id),
                    "title": doc.title,
                    "category": doc.category,
                    "tags": doc.tags,
                    "file_name": doc.file_name,
                    "file_type": doc.file_type,
                    "is_active": doc.is_active,
                    "is_temporary": doc.is_temporary,
                    "expires_at": doc.expires_at.isoformat() if doc.expires_at else None,
                    "created_by": doc.created_by,
                    "created_at": doc.created_at.isoformat(),
                    "updated_at": doc.updated_at.isoformat(),
                    "content_preview": doc.content[:200] + "..." if len(doc.content) > 200 else doc.content,
                    "is_embedded": len(doc.chunk_ids) > 0 if doc.chunk_ids else False,
                    "chunk_count": len(doc.chunk_ids) if doc.chunk_ids else 0
                }
                for doc in docs
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/knowledge/{doc_id}")
async def get_knowledge_document(doc_id: str):
    """Get a specific knowledge document"""
    try:
        doc = await db_manager.get_knowledge_document(doc_id)
        
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "status": "success",
            "document": {
                "id": str(doc.id),
                "title": doc.title,
                "content": doc.content,
                "category": doc.category,
                "tags": doc.tags,
                "file_name": doc.file_name,
                "file_type": doc.file_type,
                "source": doc.source,
                "is_active": doc.is_active,
                "is_temporary": doc.is_temporary,
                "expires_at": doc.expires_at.isoformat() if doc.expires_at else None,
                "created_by": doc.created_by,
                "created_at": doc.created_at.isoformat(),
                "updated_at": doc.updated_at.isoformat()
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/knowledge/{doc_id}")
async def update_knowledge_document(doc_id: str, request: UpdateKnowledgeRequest):
    """Update a knowledge document"""
    try:
        success = await rag_system.update_document_in_knowledge_base(
            doc_id=doc_id,
            title=request.title,
            content=request.content,
            category=request.category,
            tags=request.tags
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Document not found or update failed")
        
        return {
            "status": "success",
            "message": f"Document {doc_id} updated successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/knowledge/{doc_id}")
async def delete_knowledge_document(
    doc_id: str,
    hard_delete: bool = Query(False, description="Permanently delete (true) or soft delete (false)")
):
    """Delete a knowledge document"""
    try:
        success = await rag_system.delete_document_from_knowledge_base(
            doc_id=doc_id,
            hard_delete=hard_delete
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "status": "success",
            "message": f"Document {doc_id} {'permanently deleted' if hard_delete else 'deactivated'}",
            "hard_delete": hard_delete
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/knowledge/{doc_id}/re-embed")
async def re_embed_knowledge_document(doc_id: str):
    """Re-embed a document in the vector store"""
    try:
        # Get the document
        doc = await db_manager.get_knowledge_document(doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete old chunks from vector store
        if doc.chunk_ids:
            await rag_system._delete_document_chunks(doc.chunk_ids)
        
        # Re-embed the document
        doc_ids = await rag_system.add_documents_to_knowledge_base(
            documents=[{
                "title": doc.title,
                "content": doc.content,
                "tags": doc.tags,
                "source": doc.source,
                "file_name": doc.file_name,
                "file_type": doc.file_type
            }],
            category=doc.category,
            is_temporary=doc.is_temporary,
            expires_in_days=None,
            created_by=doc.created_by
        )
        
        return {
            "status": "success",
            "message": f"Document '{doc.title}' successfully re-embedded in vector store",
            "document_id": doc_id,
            "chunks_created": len(doc_ids)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/knowledge/batch-re-embed")
async def batch_re_embed_documents(doc_ids: List[str] = Body(...)):
    """Re-embed multiple documents in the vector store"""
    try:
        results = []
        for doc_id in doc_ids:
            try:
                # Get the document
                doc = await db_manager.get_knowledge_document(doc_id)
                if not doc:
                    results.append({
                        "document_id": doc_id,
                        "status": "error",
                        "message": "Document not found"
                    })
                    continue
                
                # Delete old chunks from vector store
                if doc.chunk_ids:
                    await rag_system._delete_document_chunks(doc.chunk_ids)
                
                # Re-embed the document
                new_doc_ids = await rag_system.add_documents_to_knowledge_base(
                    documents=[{
                        "title": doc.title,
                        "content": doc.content,
                        "tags": doc.tags,
                        "source": doc.source,
                        "file_name": doc.file_name,
                        "file_type": doc.file_type
                    }],
                    category=doc.category,
                    is_temporary=doc.is_temporary,
                    expires_in_days=None,
                    created_by=doc.created_by
                )
                
                results.append({
                    "document_id": doc_id,
                    "status": "success",
                    "message": f"Document '{doc.title}' re-embedded successfully",
                    "chunks_created": len(new_doc_ids)
                })
                
            except Exception as e:
                results.append({
                    "document_id": doc_id,
                    "status": "error",
                    "message": str(e)
                })
        
        success_count = sum(1 for r in results if r["status"] == "success")
        
        return {
            "status": "success",
            "total": len(doc_ids),
            "success": success_count,
            "failed": len(doc_ids) - success_count,
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/knowledge/categories/list")
async def list_categories():
    """Get list of all categories in knowledge base"""
    try:
        docs = await db_manager.get_all_knowledge_documents()
        categories = list(set(doc.category for doc in docs))
        
        # Count documents per category
        category_counts = {}
        for category in categories:
            category_counts[category] = sum(1 for doc in docs if doc.category == category)
        
        return {
            "status": "success",
            "categories": [
                {
                    "name": category,
                    "count": count
                }
                for category, count in sorted(category_counts.items())
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Ticket management - Specific routes MUST come before parametric routes

@app.get("/api/tickets/unassigned")
async def get_unassigned_tickets(requires_human_only: bool = Query(default=True)):
    """Get all unassigned tickets that require human attention"""
    try:
        all_tickets = await db_manager.get_all_tickets()
        unassigned_tickets = [
            ticket for ticket in all_tickets 
            if not ticket.assigned_to and (not requires_human_only or ticket.requires_human)
        ]
        
        return {
            "count": len(unassigned_tickets),
            "tickets": [
                {
                    "ticket_id": ticket.ticket_id,
                    "channel": ticket.channel,
                    "customer_identifier": ticket.customer_identifier,
                    "subject": ticket.subject,
                    "status": ticket.status,
                    "priority": ticket.priority,
                    "requires_human": ticket.requires_human,
                    "created_at": ticket.created_at.isoformat(),
                    "conversation_count": len(ticket.conversation)
                }
                for ticket in unassigned_tickets
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tickets/assigned/{agent_email}")
async def get_assigned_tickets(agent_email: str):
    """Get all tickets assigned to a specific agent"""
    try:
        all_tickets = await db_manager.get_all_tickets()
        # Normalize email for comparison and filter active tickets only
        normalized_email = agent_email.strip().lower()
        assigned_tickets = [
            ticket for ticket in all_tickets 
            if ticket.assigned_to and ticket.assigned_to.strip().lower() == normalized_email
            and ticket.status in ["open", "in_progress", "pending"]
        ]
        
        return {
            "agent": agent_email,
            "count": len(assigned_tickets),
            "tickets": [
                {
                    "ticket_id": ticket.ticket_id,
                    "channel": ticket.channel,
                    "customer_identifier": ticket.customer_identifier,
                    "subject": ticket.subject,
                    "status": ticket.status,
                    "priority": ticket.priority,
                    "created_at": ticket.created_at.isoformat(),
                    "assigned_at": ticket.assigned_at.isoformat() if ticket.assigned_at else None
                }
                for ticket in assigned_tickets
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tickets/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: str):
    """Get ticket details"""
    ticket = await db_manager.get_ticket(ticket_id)
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return TicketResponse(
        ticket_id=ticket.ticket_id,
        channel=ticket.channel,
        customer_identifier=ticket.customer_identifier,
        status=ticket.status,
        subject=ticket.subject,
        created_at=ticket.created_at,
        conversation=[msg.model_dump() for msg in ticket.conversation]
    )


@app.get("/api/debug/db-status")
async def get_db_status():
    """Diagnostic endpoint to check database status"""
    try:
        # Check if database is connected
        db_connected = db_manager.client is not None
        
        # Count documents in collections
        tickets_count = await db_manager.db.tickets.count_documents({})
        knowledge_count = await db_manager.db.knowledge.count_documents({})
        agents_count = await db_manager.db.agents.count_documents({})
        
        # Get sample ticket if exists
        sample_ticket = await db_manager.db.tickets.find_one({})
        
        return {
            "database_connected": db_connected,
            "collections": {
                "tickets": tickets_count,
                "knowledge": knowledge_count,
                "agents": agents_count
            },
            "mongodb_url": settings.mongodb_url.split("@")[-1] if "@" in settings.mongodb_url else settings.mongodb_url,
            "sample_ticket_exists": sample_ticket is not None,
            "sample_ticket_id": sample_ticket.get("ticket_id") if sample_ticket else None
        }
    except Exception as e:
        return {
            "error": str(e),
            "database_connected": False
        }


@app.get("/api/tickets")
async def list_tickets(
    status: Optional[str] = None,
    channel: Optional[str] = None,
    limit: int = 50
):
    """List tickets with filters"""
    try:
        # FIX: Actually get ALL tickets instead of always calling get_open_tickets()
        if status == "open":
            tickets = await db_manager.get_open_tickets()
        elif status:
            # Filter by status
            all_tickets = await db_manager.get_all_tickets()
            tickets = [t for t in all_tickets if t.status == status]
        else:
            # Get ALL tickets (no filter)
            tickets = await db_manager.get_all_tickets()
        
        # Filter by channel if provided
        if channel:
            tickets = [t for t in tickets if t.channel == channel]
        
        return {
            "tickets": [
                {
                    "ticket_id": t.ticket_id,
                    "channel": t.channel,
                    "customer_identifier": t.customer_identifier,
                    "status": t.status,
                    "subject": t.subject,
                    "created_at": t.created_at,
                    "message_count": len(t.conversation),
                    "requires_human": t.requires_human,
                    "assigned_to": t.assigned_to,
                    "assigned_at": t.assigned_at
                }
                for t in tickets[:limit]
            ],
            "count": len(tickets[:limit]),
            "total": len(tickets)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/tickets/{ticket_id}/status")
async def update_ticket_status(ticket_id: str, status: str):
    """Update ticket status"""
    try:
        ticket = await db_manager.get_ticket(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        update_data = {"status": status}
        if status == "resolved" or status == "closed":
            update_data["resolved_at"] = datetime.utcnow()
        
        await db_manager.update_ticket(ticket_id, update_data)
        
        return {
            "status": "success",
            "message": f"Ticket {ticket_id} updated to {status}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Statistics and monitoring
@app.get("/api/stats")
async def get_statistics():
    """Get system statistics"""
    try:
        open_tickets = await db_manager.get_open_tickets()
        
        # Calculate statistics
        stats = {
            "total_open_tickets": len(open_tickets),
            "by_channel": {},
            "auto_resolved_count": 0,
            "requires_human_count": 0
        }
        
        for ticket in open_tickets:
            # Count by channel
            stats["by_channel"][ticket.channel] = stats["by_channel"].get(ticket.channel, 0) + 1
            
            # Count auto-resolved
            if ticket.auto_resolved:
                stats["auto_resolved_count"] += 1
            
            # Count requires human
            if ticket.requires_human:
                stats["requires_human_count"] += 1
        
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Assignment endpoints
class AssignTicketRequest(BaseModel):
    ticket_id: str
    assigned_to: str  # Email or name of agent
    notes: Optional[str] = None


@app.post("/api/tickets/{ticket_id}/assign")
async def assign_ticket(ticket_id: str, request: AssignTicketRequest):
    """Assign a ticket to an agent"""
    try:
        ticket = await db_manager.get_ticket(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        # Update ticket with assignment
        update_data = {
            "assigned_to": request.assigned_to,
            "assigned_at": datetime.utcnow(),
            "requires_human": False,  # Clear the flag once assigned
            "updated_at": datetime.utcnow()
        }
        
        if request.notes:
            if not ticket.metadata:
                ticket.metadata = {}
            ticket.metadata["assignment_notes"] = request.notes
            update_data["metadata"] = ticket.metadata
        
        await db_manager.update_ticket(ticket_id, update_data)
        
        # Add system message to conversation
        system_message = ConversationMessage(
            role="system",
            content=f"Ticket assigned to {request.assigned_to}" + (f". Notes: {request.notes}" if request.notes else ""),
            metadata={"assigned_to": request.assigned_to, "action": "assignment"}
        )
        await db_manager.add_message_to_ticket(ticket_id, system_message)
        
        return {
            "status": "success",
            "message": f"Ticket assigned to {request.assigned_to}",
            "ticket_id": ticket_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ReassignTicketRequest(BaseModel):
    ticket_id: str
    new_agent_id: str  # Agent ID to reassign to
    reason: Optional[str] = None


@app.post("/api/tickets/{ticket_id}/reassign")
async def reassign_ticket(ticket_id: str, request: ReassignTicketRequest):
    """Reassign a ticket to a different agent"""
    try:
        ticket = await db_manager.get_ticket(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        # Get the new agent
        new_agent = await db_manager.get_agent(request.new_agent_id)
        if not new_agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        if not new_agent.is_active:
            raise HTTPException(status_code=400, detail="Cannot assign to inactive agent")
        
        # Get old agent info for logging
        old_agent_email = ticket.assigned_to
        
        # Update ticket with new assignment
        update_data = {
            "assigned_to": new_agent.email,
            "assigned_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Add reassignment notes to metadata
        if not ticket.metadata:
            ticket.metadata = {}
        ticket.metadata["reassignment_history"] = ticket.metadata.get("reassignment_history", [])
        ticket.metadata["reassignment_history"].append({
            "from_agent": old_agent_email,
            "to_agent": new_agent.email,
            "to_agent_id": request.new_agent_id,
            "reason": request.reason,
            "timestamp": datetime.utcnow().isoformat()
        })
        update_data["metadata"] = ticket.metadata
        
        await db_manager.update_ticket(ticket_id, update_data)
        
        # Add system message to conversation
        reassign_message = f"Ticket reassigned from {old_agent_email} to {new_agent.name} ({new_agent.email})"
        if request.reason:
            reassign_message += f". Reason: {request.reason}"
        
        system_message = ConversationMessage(
            role="system",
            content=reassign_message,
            metadata={
                "from_agent": old_agent_email,
                "to_agent": new_agent.email,
                "to_agent_id": request.new_agent_id,
                "action": "reassignment",
                "reason": request.reason
            }
        )
        await db_manager.add_message_to_ticket(ticket_id, system_message)
        
        return {
            "status": "success",
            "message": f"Ticket reassigned to {new_agent.name}",
            "ticket_id": ticket_id,
            "old_agent": old_agent_email,
            "new_agent": new_agent.email,
            "new_agent_id": request.new_agent_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Notification endpoints
@app.get("/api/notifications/pending")
async def get_pending_notifications():
    """Get tickets that need human attention and haven't been notified"""
    try:
        all_tickets = await db_manager.get_all_tickets()
        
        # Find tickets that require human attention and haven't been notified
        pending_notifications = [
            ticket for ticket in all_tickets
            if ticket.requires_human and not ticket.notification_sent and not ticket.assigned_to
        ]
        
        return {
            "count": len(pending_notifications),
            "notifications": [
                {
                    "ticket_id": ticket.ticket_id,
                    "channel": ticket.channel,
                    "customer_identifier": ticket.customer_identifier,
                    "subject": ticket.subject,
                    "priority": ticket.priority,
                    "created_at": ticket.created_at.isoformat(),
                    "last_message": ticket.conversation[-1].content if ticket.conversation else None,
                    "confidence": ticket.conversation[-1].metadata.get("confidence") if ticket.conversation and ticket.conversation[-1].metadata else None
                }
                for ticket in pending_notifications
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/notifications/{ticket_id}/mark-sent")
async def mark_notification_sent(ticket_id: str):
    """Mark that a notification has been sent for a ticket"""
    try:
        ticket = await db_manager.get_ticket(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        await db_manager.update_ticket(ticket_id, {
            "notification_sent": True,
            "notification_sent_at": datetime.utcnow()
        })
        
        return {
            "status": "success",
            "message": "Notification marked as sent",
            "ticket_id": ticket_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Agent Management Endpoints
class CreateAgentRequest(BaseModel):
    agent_id: str
    name: str
    email: str
    skills: List[str] = []
    skill_levels: Dict[str, str] = {}
    max_concurrent_tickets: int = 10
    channels: List[str] = ["email", "sms", "whatsapp", "chat"]
    shift_start: Optional[str] = None
    shift_end: Optional[str] = None
    timezone: str = "UTC"


@app.post("/api/agents/create")
async def create_agent(request: CreateAgentRequest):
    """Create a new support agent"""
    try:
        # Check if agent already exists
        existing = await db_manager.get_agent(request.agent_id)
        if existing:
            raise HTTPException(status_code=400, detail="Agent ID already exists")
        
        # Create agent
        agent = Agent(
            agent_id=request.agent_id,
            name=request.name,
            email=request.email,
            skills=request.skills,
            skill_levels=request.skill_levels,
            max_concurrent_tickets=request.max_concurrent_tickets,
            channels=request.channels,
            shift_start=request.shift_start,
            shift_end=request.shift_end,
            timezone=request.timezone
        )
        
        agent_id = await db_manager.create_agent(agent)
        
        return {
            "status": "success",
            "message": f"Agent {request.name} created successfully",
            "agent_id": request.agent_id,
            "id": agent_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agents/list")
async def list_agents(active_only: bool = Query(default=True)):
    """Get all agents"""
    try:
        agents = await db_manager.get_all_agents(active_only=active_only)
        
        return {
            "count": len(agents),
            "agents": [
                {
                    "agent_id": agent.agent_id,
                    "name": agent.name,
                    "email": agent.email,
                    "skills": agent.skills,
                    "skill_levels": agent.skill_levels,
                    "is_active": agent.is_active,
                    "current_load": agent.current_load,
                    "max_concurrent_tickets": agent.max_concurrent_tickets,
                    "utilization_percent": (agent.current_load / agent.max_concurrent_tickets * 100) if agent.max_concurrent_tickets > 0 else 0,
                    "total_assigned": agent.total_assigned,
                    "total_resolved": agent.total_resolved,
                    "channels": agent.channels,
                    "created_at": agent.created_at.isoformat()
                }
                for agent in agents
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent details"""
    try:
        agent = await db_manager.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        return {
            "agent_id": agent.agent_id,
            "name": agent.name,
            "email": agent.email,
            "skills": agent.skills,
            "skill_levels": agent.skill_levels,
            "is_active": agent.is_active,
            "current_load": agent.current_load,
            "max_concurrent_tickets": agent.max_concurrent_tickets,
            "total_assigned": agent.total_assigned,
            "total_resolved": agent.total_resolved,
            "avg_resolution_time_minutes": agent.avg_resolution_time_minutes,
            "channels": agent.channels,
            "shift_start": agent.shift_start,
            "shift_end": agent.shift_end,
            "timezone": agent.timezone,
            "created_at": agent.created_at.isoformat(),
            "last_assigned_at": agent.last_assigned_at.isoformat() if agent.last_assigned_at else None
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/agents/{agent_id}/status")
async def update_agent_status(agent_id: str, is_active: bool = Query(...)):
    """Update agent active status"""
    try:
        agent = await db_manager.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        await db_manager.update_agent(agent_id, {"is_active": is_active})
        
        return {
            "status": "success",
            "message": f"Agent {agent.name} is now {'active' if is_active else 'inactive'}",
            "agent_id": agent_id,
            "is_active": is_active
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agents/team/stats")
async def get_team_stats():
    """Get team-wide statistics"""
    try:
        stats = await auto_assignment.get_team_stats()
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agents/{agent_id}/stats")
async def get_agent_stats(agent_id: str):
    """Get detailed agent statistics"""
    try:
        stats = await auto_assignment.get_agent_stats(agent_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        return stats
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# SLA MANAGEMENT APIs - COMMENTED OUT
# ============================================================================

# from app.database import SLAPolicy, SLATemplate, BusinessHours, Holiday, SLAEscalationRule

# class CreateSLAPolicyRequest(BaseModel):
#     """Request model for creating SLA policy"""
#     policy_id: str
#     name: str
#     description: Optional[str] = None
#     domain: str = "IT"
#     categories: List[str] = []
#     priorities: List[str] = []
#     customer_tiers: List[str] = ["standard"]
#     response_time_minutes: int
#     resolution_time_minutes: int
#     use_business_hours: bool = True
#     business_hours: Optional[Dict[str, Any]] = None
#     holidays: List[Dict[str, Any]] = []
#     escalation_rules: List[Dict[str, Any]] = []
#     auto_escalate: bool = True
#     is_default: bool = False
#     priority_order: int = 0
#     created_by: Optional[str] = None


# @app.post("/api/sla/policies/create")
# async def create_sla_policy(request: CreateSLAPolicyRequest):
#     """Create a new SLA policy"""
#     try:
#         # Check if policy_id already exists
#         existing = await db_manager.get_sla_policy(request.policy_id)
#         if existing:
#             raise HTTPException(status_code=400, detail="Policy ID already exists")
#         
#         # Build business hours if provided
#         bh = None
#         if request.business_hours:
#             bh = BusinessHours(**request.business_hours)
#         else:
#             bh = BusinessHours()
#         
#         # Build holidays
#         holidays = [Holiday(**h) for h in request.holidays]
#         
#         # Build escalation rules
#         escalation_rules = [SLAEscalationRule(**er) for er in request.escalation_rules]
#         
#         policy = SLAPolicy(
#             policy_id=request.policy_id,
#             name=request.name,
#             description=request.description,
#             domain=request.domain,
#             categories=request.categories,
#             priorities=request.priorities,
#             customer_tiers=request.customer_tiers,
#             response_time_minutes=request.response_time_minutes,
#             resolution_time_minutes=request.resolution_time_minutes,
#             use_business_hours=request.use_business_hours,
#             business_hours=bh,
#             holidays=holidays,
#             escalation_rules=escalation_rules,
#             auto_escalate=request.auto_escalate,
#             is_default=request.is_default,
#             priority_order=request.priority_order,
#             created_by=request.created_by
#         )
#         
#         policy_id = await db_manager.create_sla_policy(policy)
#         
#         return {
#             "status": "success",
#             "policy_id": request.policy_id,
#             "message": "SLA policy created successfully"
#         }
#     
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/api/sla/policies/list")
# async def list_sla_policies(domain: Optional[str] = None, is_active: Optional[bool] = None):
#     """Get all SLA policies"""
#     try:
#         policies = await db_manager.get_all_sla_policies(domain=domain, is_active=is_active)
#         
#         return {
#             "policies": [
#                 {
#                     "policy_id": p.policy_id,
#                     "name": p.name,
#                     "description": p.description,
#                     "domain": p.domain,
#                     "categories": p.categories,
#                     "priorities": p.priorities,
#                     "customer_tiers": p.customer_tiers,
#                     "response_time_minutes": p.response_time_minutes,
#                     "resolution_time_minutes": p.resolution_time_minutes,
#                     "use_business_hours": p.use_business_hours,
#                     "is_active": p.is_active,
#                     "is_default": p.is_default,
#                     "priority_order": p.priority_order,
#                     "created_at": p.created_at.isoformat(),
#                     "updated_at": p.updated_at.isoformat()
#                 }
#                 for p in policies
#             ],
#             "count": len(policies)
#         }
#     
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/api/sla/policies/{policy_id}")
# async def get_sla_policy(policy_id: str):
#     """Get SLA policy details"""
#     try:
#         policy = await db_manager.get_sla_policy(policy_id)
#         if not policy:
#             raise HTTPException(status_code=404, detail="Policy not found")
#         
#         return {
#             "policy_id": policy.policy_id,
#             "name": policy.name,
#             "description": policy.description,
#             "domain": policy.domain,
#             "categories": policy.categories,
#             "priorities": policy.priorities,
#             "customer_tiers": policy.customer_tiers,
#             "response_time_minutes": policy.response_time_minutes,
#             "resolution_time_minutes": policy.resolution_time_minutes,
#             "use_business_hours": policy.use_business_hours,
#             "business_hours": policy.business_hours.model_dump() if policy.business_hours else None,
#             "holidays": [h.model_dump() for h in policy.holidays],
#             "escalation_rules": [er.model_dump() for er in policy.escalation_rules],
#             "auto_escalate": policy.auto_escalate,
#             "is_active": policy.is_active,
#             "is_default": policy.is_default,
#             "priority_order": policy.priority_order,
#             "created_by": policy.created_by,
#             "created_at": policy.created_at.isoformat(),
#             "updated_at": policy.updated_at.isoformat()
#         }
#     
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.put("/api/sla/policies/{policy_id}")
# async def update_sla_policy(policy_id: str, update_data: Dict[str, Any]):
#     """Update SLA policy"""
#     try:
#         policy = await db_manager.get_sla_policy(policy_id)
#         if not policy:
#             raise HTTPException(status_code=404, detail="Policy not found")
#         
#         success = await db_manager.update_sla_policy(policy_id, update_data)
#         
#         if success:
#             return {
#                 "status": "success",
#                 "policy_id": policy_id,
#                 "message": "Policy updated successfully"
#             }
#         else:
#             return {
#                 "status": "error",
#                 "message": "No changes made"
#             }
#     
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.delete("/api/sla/policies/{policy_id}")
# async def delete_sla_policy(policy_id: str):
#     """Delete (deactivate) SLA policy"""
#     try:
#         policy = await db_manager.get_sla_policy(policy_id)
#         if not policy:
#             raise HTTPException(status_code=404, detail="Policy not found")
#         
#         success = await db_manager.delete_sla_policy(policy_id)
#         
#         return {
#             "status": "success" if success else "error",
#             "policy_id": policy_id,
#             "message": "Policy deactivated successfully" if success else "Failed to deactivate"
#         }
#     
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/api/sla/templates/list")
# async def list_sla_templates(category: Optional[str] = None):
#     """Get all SLA templates"""
#     try:
#         templates = await db_manager.get_all_sla_templates(category=category)
#         
#         return {
#             "templates": [
#                 {
#                     "template_id": t.template_id,
#                     "name": t.name,
#                     "description": t.description,
#                     "category": t.category,
#                     "policies_count": len(t.policies),
#                     "created_at": t.created_at.isoformat()
#                 }
#                 for t in templates
#             ],
#             "count": len(templates)
#         }
#     
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/api/sla/templates/{template_id}")
# async def get_sla_template(template_id: str):
#     """Get SLA template details"""
#     try:
#         template = await db_manager.get_sla_template(template_id)
#         if not template:
#             raise HTTPException(status_code=404, detail="Template not found")
#         
#         return {
#             "template_id": template.template_id,
#             "name": template.name,
#             "description": template.description,
#             "category": template.category,
#             "policies": template.policies,
#             "created_at": template.created_at.isoformat()
#         }
#     
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.post("/api/sla/templates/{template_id}/apply")
# async def apply_sla_template(template_id: str, domain: str = Query("IT")):
#     """Apply an SLA template to create policies"""
#     try:
#         policy_ids = await db_manager.apply_sla_template(template_id, domain)
#         
#         if not policy_ids:
#             raise HTTPException(status_code=404, detail="Template not found or no policies created")
#         
#         return {
#             "status": "success",
#             "template_id": template_id,
#             "created_policies": policy_ids,
#             "message": f"Created {len(policy_ids)} policies from template"
#         }
#     
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# HOLIDAY CALENDAR MANAGEMENT APIs
# ============================================================================

from app.database import Holiday, AgentHoliday

class CreateHolidayRequest(BaseModel):
    """Request model for creating a holiday"""
    date: str
    name: str
    is_working_day: bool = False
    holiday_type: str = "national"
    region: Optional[str] = None
    is_recurring: bool = False
    recurring_pattern: Optional[str] = None


class CreateAgentHolidayRequest(BaseModel):
    """Request model for creating agent holiday"""
    agent_id: str
    date: str
    name: str
    leave_type: str = "personal"
    is_working_day: bool = False
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    reason: Optional[str] = None
    approved_by: Optional[str] = None


@app.post("/api/holidays/create")
async def create_holiday(request: CreateHolidayRequest):
    """Create a new holiday entry"""
    try:
        holiday = Holiday(**request.model_dump())
        holiday_id = await db_manager.create_holiday(holiday)
        
        return {
            "status": "success",
            "holiday_id": holiday_id,
            "message": "Holiday created successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/holidays/list")
async def list_holidays(year: Optional[int] = None, holiday_type: Optional[str] = None, region: Optional[str] = None):
    """Get holidays with optional filters"""
    try:
        holidays = await db_manager.get_holidays(year=year, holiday_type=holiday_type, region=region)
        
        return {
            "holidays": [
                {
                    "date": h.date,
                    "name": h.name,
                    "holiday_type": h.holiday_type,
                    "region": h.region,
                    "is_working_day": h.is_working_day,
                    "is_recurring": h.is_recurring
                }
                for h in holidays
            ],
            "count": len(holidays)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/holidays/check/{date}")
async def check_holiday(date: str, region: Optional[str] = None):
    """Check if a date is a holiday"""
    try:
        is_holiday = await db_manager.is_holiday(date, region=region)
        
        return {
            "date": date,
            "is_holiday": is_holiday,
            "region": region
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Agent Holiday Management
@app.post("/api/agents/{agent_id}/holidays/create")
async def create_agent_holiday(agent_id: str, request: CreateAgentHolidayRequest):
    """Create agent holiday/leave entry"""
    try:
        # Verify agent exists
        agent = await db_manager.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Set agent_id from URL
        request.agent_id = agent_id
        
        agent_holiday = AgentHoliday(**request.model_dump())
        holiday_id = await db_manager.create_agent_holiday(agent_holiday)
        
        return {
            "status": "success",
            "holiday_id": holiday_id,
            "message": "Agent holiday created successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agents/{agent_id}/holidays")
async def get_agent_holidays(agent_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    """Get agent holidays within date range"""
    try:
        # Verify agent exists
        agent = await db_manager.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        holidays = await db_manager.get_agent_holidays(agent_id, start_date, end_date)
        
        return {
            "agent_id": agent_id,
            "agent_name": agent.name,
            "holidays": [
                {
                    "id": str(h.id),
                    "date": h.date,
                    "name": h.name,
                    "leave_type": h.leave_type,
                    "is_working_day": h.is_working_day,
                    "start_time": h.start_time,
                    "end_time": h.end_time,
                    "reason": h.reason,
                    "approved_by": h.approved_by,
                    "created_at": h.created_at.isoformat()
                }
                for h in holidays
            ],
            "count": len(holidays)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agents/{agent_id}/holidays/check/{date}")
async def check_agent_holiday(agent_id: str, date: str, time: Optional[str] = None):
    """Check if agent is on holiday on a specific date and time"""
    try:
        # Verify agent exists
        agent = await db_manager.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        is_on_holiday = await db_manager.is_agent_on_holiday(agent_id, date, time)
        
        return {
            "agent_id": agent_id,
            "agent_name": agent.name,
            "date": date,
            "time": time,
            "is_on_holiday": is_on_holiday
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/agents/{agent_id}/holidays/{holiday_id}")
async def update_agent_holiday(agent_id: str, holiday_id: str, update_data: Dict[str, Any]):
    """Update agent holiday entry"""
    try:
        # Verify agent exists
        agent = await db_manager.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        success = await db_manager.update_agent_holiday(holiday_id, update_data)
        
        if success:
            return {
                "status": "success",
                "holiday_id": holiday_id,
                "message": "Agent holiday updated successfully"
            }
        else:
            return {
                "status": "error",
                "message": "Holiday not found or no changes made"
            }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/agents/{agent_id}/holidays/{holiday_id}")
async def delete_agent_holiday(agent_id: str, holiday_id: str):
    """Delete agent holiday entry"""
    try:
        # Verify agent exists
        agent = await db_manager.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        success = await db_manager.delete_agent_holiday(holiday_id)
        
        return {
            "status": "success" if success else "error",
            "holiday_id": holiday_id,
            "message": "Agent holiday deleted successfully" if success else "Holiday not found"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agents/available")
async def get_available_agents(date: str, time: Optional[str] = None, skills: Optional[str] = None, domain: str = "IT"):
    """Get agents available on a specific date and time (considering holidays)"""
    try:
        skills_list = skills.split(",") if skills else None
        available_agents = await db_manager.get_available_agents(date, time, skills_list, domain)
        
        return {
            "date": date,
            "time": time,
            "skills": skills_list,
            "domain": domain,
            "available_agents": [
                {
                    "agent_id": agent.agent_id,
                    "name": agent.name,
                    "email": agent.email,
                    "skills": agent.skills,
                    "tier": agent.tier,
                    "current_load": agent.current_load,
                    "max_concurrent_tickets": agent.max_concurrent_tickets
                }
                for agent in available_agents
            ],
            "count": len(available_agents)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# SYSTEM CONFIGURATION APIs
# ============================================================================

class SystemConfigRequest(BaseModel):
    """Request model for updating system configuration"""
    support_email: str
    email_host: Optional[str] = "smtp.gmail.com"
    email_port: Optional[int] = 587
    email_user: Optional[str] = None
    email_password: Optional[str] = None
    sms_enabled: Optional[bool] = False
    sms_phone_number: Optional[str] = None
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_phone_number: Optional[str] = "+14155238886"
    whatsapp_enabled: Optional[bool] = True
    whatsapp_number: Optional[str] = "whatsapp:+14155238886"
    chat_enabled: Optional[bool] = True


@app.get("/api/config")
async def get_system_config():
    """Get current system configuration"""
    try:
        config = await db_manager.get_system_config()
        if not config:
            # Return default configuration
            return SystemConfiguration(
                config_id="system_config",
                support_email="r15528850@gmail.com",
                twilio_phone_number="+14155238886",
                whatsapp_number="whatsapp:+14155238886",
                whatsapp_enabled=True
            ).model_dump()
        return config.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/config")
async def update_system_config(request: SystemConfigRequest):
    """Update system configuration and reload integrations"""
    try:
        config = SystemConfiguration(
            config_id="system_config",
            support_email=request.support_email,
            email_host=request.email_host,
            email_port=request.email_port,
            email_user=request.email_user,
            email_password=request.email_password,
            sms_enabled=request.sms_enabled,
            sms_phone_number=request.sms_phone_number,
            twilio_account_sid=request.twilio_account_sid,
            twilio_auth_token=request.twilio_auth_token,
            twilio_phone_number=request.twilio_phone_number,
            whatsapp_enabled=request.whatsapp_enabled,
            whatsapp_number=request.whatsapp_number,
            twilio_whatsapp_number=request.whatsapp_number,
            chat_enabled=request.chat_enabled
        )
        
        success = await db_manager.update_system_config(config)
        
        if success:
            # Reload integrations with new configuration
            try:
                # Reload WhatsApp integration with new settings
                from app.whatsapp_integration import whatsapp_integration
                whatsapp_integration._init_from_settings()
                
                # Update email integration settings
                from app.email_integration import email_integration
                email_integration.smtp_host = config.email_host
                email_integration.smtp_port = config.email_port
                email_integration.email_user = config.email_user
                email_integration.email_password = config.email_password
                
                print("✓ Integrations reloaded with new configuration")
            except Exception as reload_error:
                print(f"⚠️  Warning: Could not reload integrations: {reload_error}")
            
            return {
                "status": "success",
                "message": "Configuration updated and integrations reloaded",
                "config": config.model_dump()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to update configuration")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENHANCED CONFIGURATION APIs
# ============================================================================

from app.database import (
    EnhancedSystemConfiguration, 
    EmailConfig, 
    WhatsAppConfig, 
    SMSConfig, 
    ModelConfig, 
    VectorDBConfig, 
    KnowledgeProviderConfig
)

class EmailConfigRequest(BaseModel):
    """Request model for email configuration"""
    support_email: str
    email_host: str = "smtp.gmail.com"
    email_port: int = 587
    email_user: Optional[str] = None
    email_password: Optional[str] = None
    use_tls: bool = True
    use_ssl: bool = False

class WhatsAppConfigRequest(BaseModel):
    """Request model for WhatsApp configuration"""
    enabled: bool = False
    whatsapp_number: str = "whatsapp:+14155238886"
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_phone_number: Optional[str] = None

class SMSConfigRequest(BaseModel):
    """Request model for SMS configuration"""
    enabled: bool = False
    sms_phone_number: Optional[str] = None
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_phone_number: Optional[str] = None

class ModelConfigRequest(BaseModel):
    """Request model for AI model configuration"""
    llm_provider: str = "openai"
    llm_model: str = "gpt-3.5-turbo"
    llm_api_key: Optional[str] = None
    llm_base_url: Optional[str] = None
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2000
    embedding_provider: str = "openai"
    embedding_model: str = "text-embedding-ada-002"
    embedding_api_key: Optional[str] = None
    embedding_base_url: Optional[str] = None
    embedding_dimensions: int = 1536

class VectorDBConfigRequest(BaseModel):
    """Request model for vector database configuration"""
    provider: str = "chroma"
    enabled: bool = True
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    chroma_collection_name: str = "knowledge_base"
    chroma_persist_directory: Optional[str] = None
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    pinecone_index_name: str = "knowledge-base"
    pinecone_namespace: Optional[str] = None
    weaviate_url: str = "http://localhost:8080"
    weaviate_api_key: Optional[str] = None
    weaviate_class_name: str = "KnowledgeDocument"
    faiss_index_path: str = "./vector_store/faiss_index"
    faiss_index_type: str = "Flat"

class KnowledgeProviderConfigRequest(BaseModel):
    """Request model for knowledge provider configuration"""
    provider: str = "local"
    enabled: bool = True
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    aws_bucket_name: Optional[str] = None
    aws_prefix: str = "knowledge-base/"
    azure_account_name: Optional[str] = None
    azure_account_key: Optional[str] = None
    azure_container_name: Optional[str] = None
    azure_connection_string: Optional[str] = None
    google_credentials_file: Optional[str] = None
    google_folder_id: Optional[str] = None
    google_service_account_email: Optional[str] = None
    dropbox_access_token: Optional[str] = None
    dropbox_folder_path: str = "/knowledge-base"


@app.get("/api/config/enhanced")
async def get_enhanced_config():
    """Get enhanced system configuration"""
    try:
        config = await db_manager.get_enhanced_config()
        
        # If config doesn't exist or is None, create default
        if config is None:
            config = EnhancedSystemConfiguration()
            # Ensure each section is properly initialized
            if config.email is None:
                config.email = EmailConfig()
            if config.whatsapp is None:
                config.whatsapp = WhatsAppConfig()
            if config.sms is None:
                config.sms = SMSConfig()
            if config.model is None:
                config.model = ModelConfig()
            if config.vector_db is None:
                config.vector_db = VectorDBConfig()
            if config.knowledge_provider is None:
                config.knowledge_provider = KnowledgeProviderConfig()
            
            # Save to database
            await db_manager.update_enhanced_config(config)
        
        # Return the configuration
        return config.model_dump()
        
    except Exception as e:
        import traceback
        print(f"Error in get_enhanced_config: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/config/{section}")
async def get_config_section(section: str):
    """Get specific configuration section"""
    try:
        if section not in ["email", "whatsapp", "sms", "model", "vector_db", "knowledge_provider"]:
            raise HTTPException(status_code=400, detail="Invalid configuration section")
        
        section_config = await db_manager.get_config_section(section)
        if not section_config:
            # Return default configuration for the section
            if section == "email":
                section_config = EmailConfig(support_email="r15528850@gmail.com").model_dump()
            elif section == "whatsapp":
                section_config = WhatsAppConfig().model_dump()
            elif section == "sms":
                section_config = SMSConfig().model_dump()
            elif section == "model":
                section_config = ModelConfig().model_dump()
            elif section == "vector_db":
                section_config = VectorDBConfig().model_dump()
            elif section == "knowledge_provider":
                section_config = KnowledgeProviderConfig().model_dump()
        
        return section_config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/config/email")
async def update_email_config(request: EmailConfigRequest):
    """Update email configuration"""
    try:
        success = await db_manager.update_config_section("email", request.model_dump())
        if success:
            return {"status": "success", "message": "Email configuration updated"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update email configuration")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/config/whatsapp")
async def update_whatsapp_config(request: WhatsAppConfigRequest):
    """Update WhatsApp configuration"""
    try:
        success = await db_manager.update_config_section("whatsapp", request.model_dump())
        if success:
            return {"status": "success", "message": "WhatsApp configuration updated"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update WhatsApp configuration")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/config/sms")
async def update_sms_config(request: SMSConfigRequest):
    """Update SMS configuration"""
    try:
        success = await db_manager.update_config_section("sms", request.model_dump())
        if success:
            return {"status": "success", "message": "SMS configuration updated"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update SMS configuration")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/config/model")
async def update_model_config(request: ModelConfigRequest):
    """Update AI model configuration"""
    try:
        success = await db_manager.update_config_section("model", request.model_dump())
        if success:
            return {"status": "success", "message": "Model configuration updated"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update model configuration")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/config/vector-db")
async def update_vector_db_config(request: VectorDBConfigRequest):
    """Update vector database configuration"""
    try:
        success = await db_manager.update_config_section("vector_db", request.model_dump())
        if success:
            return {"status": "success", "message": "Vector database configuration updated"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update vector database configuration")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/config/knowledge-provider")
async def update_knowledge_provider_config(request: KnowledgeProviderConfigRequest):
    """Update knowledge provider configuration"""
    try:
        success = await db_manager.update_config_section("knowledge_provider", request.model_dump())
        if success:
            return {"status": "success", "message": "Knowledge provider configuration updated"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update knowledge provider configuration")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.api:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug
    )

