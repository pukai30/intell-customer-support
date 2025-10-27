"""
MongoDB database connection and models
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from app.config import settings


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic v2"""
    
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema
        
        def validate(value):
            if isinstance(value, ObjectId):
                return value
            if isinstance(value, str):
                if not ObjectId.is_valid(value):
                    raise ValueError(f"Invalid ObjectId: {value}")
                return ObjectId(value)
            raise ValueError(f"Invalid ObjectId type: {type(value)}")
        
        return core_schema.no_info_plain_validator_function(
            validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            )
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler):
        return {"type": "string"}


class ConversationMessage(BaseModel):
    """Individual message in a conversation"""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None


class SupportTicket(BaseModel):
    """Support ticket model with SLA and escalation tracking"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    ticket_id: str
    channel: str  # 'email', 'sms', 'whatsapp', 'chat'
    customer_identifier: str  # email, phone number, etc.
    customer_name: Optional[str] = None
    subject: Optional[str] = None
    status: str = "open"  # 'open', 'pending', 'resolved', 'closed', 'escalated'
    priority: str = "medium"  # 'low', 'medium', 'high', 'urgent'
    conversation: List[ConversationMessage] = []
    auto_resolved: bool = False
    requires_human: bool = False  # Flag for low-confidence tickets
    assigned_to: Optional[str] = None  # Email/ID of assigned agent
    assigned_at: Optional[datetime] = None  # When ticket was assigned
    notification_sent: bool = False  # Track if notification was sent
    notification_sent_at: Optional[datetime] = None  # When notification was sent
    
    # SLA (Service Level Agreement) fields
    sla_response_time_minutes: int = 60  # Expected first response time (default 60 min)
    sla_resolution_time_minutes: int = 240  # Expected resolution time (default 4 hours)
    first_response_at: Optional[datetime] = None  # When first response was sent
    sla_response_breached: bool = False  # Response SLA breached
    sla_resolution_breached: bool = False  # Resolution SLA breached
    sla_response_deadline: Optional[datetime] = None  # Calculated response deadline
    sla_resolution_deadline: Optional[datetime] = None  # Calculated resolution deadline
    
    # Escalation fields
    escalation_level: int = 0  # 0=no escalation, 1=L1, 2=L2, 3=L3
    escalation_history: List[Dict[str, Any]] = []  # Track escalation history
    escalated_at: Optional[datetime] = None  # When last escalated
    escalated_to: Optional[str] = None  # Agent email ticket was escalated to
    
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    tags: List[str] = []
    metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class KnowledgeDocument(BaseModel):
    """Knowledge base document model with priority support"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    content: str
    category: str
    tags: List[str] = []
    source: Optional[str] = None  # file path or URL
    file_name: Optional[str] = None  # original file name if uploaded
    file_type: Optional[str] = None  # pdf, docx, txt, etc.
    embedding_id: Optional[str] = None  # Reference to vector store
    chunk_ids: List[str] = []  # IDs of chunks in vector store
    is_active: bool = True  # Soft delete flag
    is_temporary: bool = False  # Temporary knowledge flag
    expires_at: Optional[datetime] = None  # Expiry date for temporary knowledge
    created_by: Optional[str] = None  # User who created this
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Priority for knowledge retrieval (higher number = higher priority)
    priority: int = 1  # 1=normal, 2=high, 3=critical (temporary high-priority KB)
    
    metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class Agent(BaseModel):
    """Support agent model with skills, tiers, and workload tracking"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    agent_id: str  # Unique agent identifier
    name: str
    email: str
    skills: List[str] = []  # List of skill categories (e.g., "password", "vpn", "hardware")
    skill_levels: Dict[str, str] = {}  # skill -> level mapping (beginner, intermediate, expert)
    is_active: bool = True  # Currently available for assignments
    max_concurrent_tickets: int = 10  # Maximum tickets agent can handle
    current_load: int = 0  # Current number of open assigned tickets
    total_assigned: int = 0  # Total tickets ever assigned
    total_resolved: int = 0  # Total tickets resolved
    avg_resolution_time_minutes: Optional[float] = None  # Average time to resolve
    channels: List[str] = ["email", "sms", "whatsapp", "chat"]  # Supported channels
    shift_start: Optional[str] = None  # e.g., "09:00"
    shift_end: Optional[str] = None  # e.g., "17:00"
    timezone: str = "UTC"
    
    # Escalation tier/level (0=L1/junior, 1=L2/senior, 2=L3/expert, 3=L4/manager)
    tier: int = 0  # Agent tier for escalation matrix
    handles_escalations: bool = False  # Can handle escalated tickets
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_assigned_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


# ============================================================================
# SLA MANAGEMENT MODELS
# ============================================================================

class BusinessHours(BaseModel):
    """Business hours configuration"""
    timezone: str = "UTC"
    working_days: List[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    start_time: str = "09:00"  # 24-hour format
    end_time: str = "17:00"  # 24-hour format
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class Holiday(BaseModel):
    """Holiday calendar entry"""
    date: str  # YYYY-MM-DD format
    name: str
    is_working_day: bool = False  # Can tickets be worked on this day?
    holiday_type: str = "national"  # national, regional, personal, company
    region: Optional[str] = None  # For regional holidays (e.g., "Maharashtra", "Karnataka")
    is_recurring: bool = False  # Recurring holiday (like Diwali)
    recurring_pattern: Optional[str] = None  # "yearly", "monthly", etc.
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class AgentHoliday(BaseModel):
    """Individual agent holiday/leave entry"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    agent_id: str  # Reference to agent
    date: str  # YYYY-MM-DD format
    name: str  # Holiday/leave name
    leave_type: str  # "personal", "sick", "vacation", "emergency"
    is_working_day: bool = False  # Can agent work on this day?
    start_time: Optional[str] = None  # For partial day leaves (e.g., "09:00")
    end_time: Optional[str] = None  # For partial day leaves (e.g., "13:00")
    reason: Optional[str] = None  # Reason for leave
    approved_by: Optional[str] = None  # Manager who approved
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class SystemConfiguration(BaseModel):
    """System configuration for support channels"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    config_id: str = "system_config"  # Single configuration instance
    
    # Email Configuration
    support_email: str = "r15528850@gmail.com"  # Default email
    email_host: str = "smtp.gmail.com"
    email_port: int = 587
    email_user: Optional[str] = None
    email_password: Optional[str] = None
    imap_host: str = "imap.gmail.com"
    imap_port: int = 993
    
    # SMS Configuration (Twilio)
    sms_enabled: bool = False
    sms_phone_number: Optional[str] = None
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_phone_number: Optional[str] = None
    
    # WhatsApp Configuration
    whatsapp_enabled: bool = True
    whatsapp_number: str = "whatsapp:+14155238886"
    twilio_whatsapp_number: str = "whatsapp:+14155238886"
    
    # Chat Configuration
    chat_enabled: bool = True
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


# ========================================================================
# ENHANCED CONFIGURATION MODELS
# ========================================================================

class EmailConfig(BaseModel):
    """Email configuration settings"""
    support_email: str = "r15528850@gmail.com"
    email_host: str = "smtp.gmail.com"
    email_port: int = 587
    email_user: Optional[str] = None
    email_password: Optional[str] = None
    use_tls: bool = True
    use_ssl: bool = False


class WhatsAppConfig(BaseModel):
    """WhatsApp configuration settings"""
    enabled: bool = False
    whatsapp_number: str = "whatsapp:+14155238886"
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_phone_number: Optional[str] = None


class SMSConfig(BaseModel):
    """SMS configuration settings"""
    enabled: bool = False
    sms_phone_number: Optional[str] = None
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_phone_number: Optional[str] = None


class ModelConfig(BaseModel):
    """AI Model configuration settings"""
    # LLM Configuration
    llm_provider: str = "openai"  # openai, anthropic, google, azure_openai, local
    llm_model: str = "gpt-3.5-turbo"  # gpt-3.5-turbo, gpt-4, claude-3-sonnet, etc.
    llm_api_key: Optional[str] = None
    llm_base_url: Optional[str] = None  # For local models or custom endpoints
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2000
    
    # Embedding Configuration
    embedding_provider: str = "openai"  # openai, huggingface, sentence_transformers, local
    embedding_model: str = "text-embedding-ada-002"  # text-embedding-ada-002, all-MiniLM-L6-v2, etc.
    embedding_api_key: Optional[str] = None
    embedding_base_url: Optional[str] = None
    embedding_dimensions: int = 1536


class VectorDBConfig(BaseModel):
    """Vector Database configuration settings"""
    provider: str = "chroma"  # chroma, pinecone, weaviate, faiss
    enabled: bool = True
    
    # Chroma Configuration
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    chroma_collection_name: str = "knowledge_base"
    chroma_persist_directory: Optional[str] = None
    
    # Pinecone Configuration
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    pinecone_index_name: str = "knowledge-base"
    pinecone_namespace: Optional[str] = None
    
    # Weaviate Configuration
    weaviate_url: str = "http://localhost:8080"
    weaviate_api_key: Optional[str] = None
    weaviate_class_name: str = "KnowledgeDocument"
    
    # FAISS Configuration
    faiss_index_path: str = "./vector_store/faiss_index"
    faiss_index_type: str = "Flat"  # Flat, IVF, HNSW


class KnowledgeProviderConfig(BaseModel):
    """Knowledge Provider configuration settings"""
    provider: str = "local"  # local, aws_s3, azure_blob, google_drive, dropbox
    enabled: bool = True
    
    # AWS S3 Configuration
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    aws_bucket_name: Optional[str] = None
    aws_prefix: str = "knowledge-base/"
    
    # Azure Blob Storage Configuration
    azure_account_name: Optional[str] = None
    azure_account_key: Optional[str] = None
    azure_container_name: Optional[str] = None
    azure_connection_string: Optional[str] = None
    
    # Google Drive Configuration
    google_credentials_file: Optional[str] = None
    google_folder_id: Optional[str] = None
    google_service_account_email: Optional[str] = None
    
    # Dropbox Configuration
    dropbox_access_token: Optional[str] = None
    dropbox_folder_path: str = "/knowledge-base"


class EnhancedSystemConfiguration(BaseModel):
    """Enhanced system configuration with tabs"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    config_id: str = "enhanced_system_config"
    
    # Channel Configurations
    email: Optional[EmailConfig] = Field(default_factory=EmailConfig)
    whatsapp: Optional[WhatsAppConfig] = Field(default_factory=WhatsAppConfig)
    sms: Optional[SMSConfig] = Field(default_factory=SMSConfig)
    
    # AI Configuration
    model: Optional[ModelConfig] = Field(default_factory=ModelConfig)
    vector_db: Optional[VectorDBConfig] = Field(default_factory=VectorDBConfig)
    knowledge_provider: Optional[KnowledgeProviderConfig] = Field(default_factory=KnowledgeProviderConfig)
    
    # System Settings
    chat_enabled: bool = True
    auto_assignment_enabled: bool = True
    escalation_enabled: bool = True
    notification_enabled: bool = True
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    version: str = "1.0.0"
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class SLAEscalationRule(BaseModel):
    """Escalation rules for SLA breaches"""
    level: int  # Escalation level (1, 2, 3, etc.)
    trigger_after_minutes: int  # Minutes after SLA breach to trigger
    escalate_to_tier: int  # Agent tier to escalate to
    notify_emails: List[str] = []  # Additional notification emails
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class SLAPolicy(BaseModel):
    """SLA Policy configuration"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    policy_id: str  # Unique policy identifier (e.g., "IT_CRITICAL", "NETWORK_HIGH")
    name: str  # Human-readable name
    description: Optional[str] = None
    
    # Policy applicability
    categories: List[str] = []  # Empty means applies to all categories
    priorities: List[str] = []  # Empty means applies to all priorities
    customer_tiers: List[str] = ["standard"]  # VIP, premium, standard, etc.
    
    # SLA times (in minutes)
    response_time_minutes: int  # First response time
    resolution_time_minutes: int  # Resolution time
    
    # Business hours
    use_business_hours: bool = True  # Count only business hours or 24/7
    business_hours: Optional[BusinessHours] = Field(default_factory=BusinessHours)
    holidays: List[Holiday] = []  # Holiday calendar
    
    # Escalation rules
    escalation_rules: List[SLAEscalationRule] = []
    auto_escalate: bool = True  # Automatically escalate on breach
    
    # Policy status
    is_active: bool = True
    is_default: bool = False  # Is this the default policy?
    priority_order: int = 0  # Higher number = higher priority when matching
    
    # Metadata
    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class SLATemplate(BaseModel):
    """Predefined SLA template for quick setup"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    template_id: str  # Unique template identifier
    name: str  # Template name (e.g., "Standard IT Support", "Enterprise SLA")
    description: str
    
    # Template policies (list of policy configurations)
    policies: List[Dict[str, Any]] = []  # Policy data that can be applied
    
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class DatabaseManager:
    """MongoDB database manager"""
    
    client: Optional[AsyncIOMotorClient] = None
    db = None
    
    async def connect(self):
        """Connect to MongoDB"""
        self.client = AsyncIOMotorClient(settings.mongodb_url)
        self.db = self.client[settings.mongodb_db_name]
        
        # Create indexes
        await self._create_indexes()
        
        print(f"Connected to MongoDB: {settings.mongodb_db_name}")
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")
    
    async def _create_indexes(self):
        """Create database indexes"""
        # Support tickets indexes
        await self.db.tickets.create_index([("ticket_id", ASCENDING)], unique=True)
        await self.db.tickets.create_index([("channel", ASCENDING)])
        await self.db.tickets.create_index([("customer_identifier", ASCENDING)])
        await self.db.tickets.create_index([("status", ASCENDING)])
        await self.db.tickets.create_index([("created_at", DESCENDING)])
        
        # Knowledge documents indexes
        await self.db.knowledge.create_index([("category", ASCENDING)])
        await self.db.knowledge.create_index([("tags", ASCENDING)])
        await self.db.knowledge.create_index([("title", "text"), ("content", "text")])
        await self.db.knowledge.create_index([("is_active", ASCENDING)])
        await self.db.knowledge.create_index([("expires_at", ASCENDING)])
        await self.db.knowledge.create_index([("created_at", DESCENDING)])
    
    # Support Ticket Operations
    async def create_ticket(self, ticket: SupportTicket) -> str:
        """Create a new support ticket with SLA deadlines"""
        # Calculate SLA deadlines
        deadlines = self.calculate_sla_deadlines(ticket)
        ticket.sla_response_deadline = deadlines["response_deadline"]
        ticket.sla_resolution_deadline = deadlines["resolution_deadline"]
        
        ticket_dict = ticket.model_dump(by_alias=True, exclude={"id"})
        result = await self.db.tickets.insert_one(ticket_dict)
        return str(result.inserted_id)
    
    async def get_ticket(self, ticket_id: str) -> Optional[SupportTicket]:
        """Get a support ticket by ticket_id"""
        ticket_data = await self.db.tickets.find_one({"ticket_id": ticket_id})
        if ticket_data:
            return SupportTicket(**ticket_data)
        return None
    
    async def update_ticket(self, ticket_id: str, update_data: dict):
        """Update a support ticket"""
        update_data["updated_at"] = datetime.utcnow()
        await self.db.tickets.update_one(
            {"ticket_id": ticket_id},
            {"$set": update_data}
        )
    
    async def add_message_to_ticket(self, ticket_id: str, message: ConversationMessage):
        """Add a message to a ticket's conversation"""
        await self.db.tickets.update_one(
            {"ticket_id": ticket_id},
            {
                "$push": {"conversation": message.model_dump()},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
    
    async def get_tickets_by_customer(self, customer_identifier: str) -> List[SupportTicket]:
        """Get all tickets for a customer"""
        tickets = []
        cursor = self.db.tickets.find({"customer_identifier": customer_identifier})
        async for ticket_data in cursor:
            tickets.append(SupportTicket(**ticket_data))
        return tickets
    
    async def get_open_tickets(self) -> List[SupportTicket]:
        """Get all open tickets"""
        tickets = []
        cursor = self.db.tickets.find({"status": "open"})
        async for ticket_data in cursor:
            tickets.append(SupportTicket(**ticket_data))
        return tickets
    
    async def get_all_tickets(self) -> List[SupportTicket]:
        """Get all tickets"""
        tickets = []
        cursor = self.db.tickets.find({})
        async for ticket_data in cursor:
            tickets.append(SupportTicket(**ticket_data))
        return tickets
    
    # Knowledge Base Operations
    async def create_knowledge_document(self, doc: KnowledgeDocument) -> str:
        """Create a knowledge document"""
        doc_dict = doc.model_dump(by_alias=True, exclude={"id"})
        result = await self.db.knowledge.insert_one(doc_dict)
        return str(result.inserted_id)
    
    async def get_knowledge_document(self, doc_id: str) -> Optional[KnowledgeDocument]:
        """Get a knowledge document by ID"""
        doc_data = await self.db.knowledge.find_one({"_id": ObjectId(doc_id)})
        if doc_data:
            return KnowledgeDocument(**doc_data)
        return None
    
    async def search_knowledge(self, query: str, limit: int = 10) -> List[KnowledgeDocument]:
        """Full-text search in knowledge base"""
        docs = []
        cursor = self.db.knowledge.find(
            {"$text": {"$search": query}}
        ).limit(limit)
        async for doc_data in cursor:
            docs.append(KnowledgeDocument(**doc_data))
        return docs
    
    async def get_all_knowledge_documents(self, include_inactive: bool = False) -> List[KnowledgeDocument]:
        """Get all knowledge documents"""
        docs = []
        query = {} if include_inactive else {"is_active": True}
        cursor = self.db.knowledge.find(query).sort("created_at", DESCENDING)
        async for doc_data in cursor:
            docs.append(KnowledgeDocument(**doc_data))
        return docs
    
    async def update_knowledge_document(self, doc_id: str, update_data: dict):
        """Update a knowledge document"""
        update_data["updated_at"] = datetime.utcnow()
        await self.db.knowledge.update_one(
            {"_id": ObjectId(doc_id)},
            {"$set": update_data}
        )
    
    async def delete_knowledge_document(self, doc_id: str, soft_delete: bool = True):
        """Delete a knowledge document (soft or hard delete)"""
        if soft_delete:
            await self.db.knowledge.update_one(
                {"_id": ObjectId(doc_id)},
                {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
            )
        else:
            await self.db.knowledge.delete_one({"_id": ObjectId(doc_id)})
    
    async def get_expired_knowledge_documents(self) -> List[KnowledgeDocument]:
        """Get all expired temporary knowledge documents"""
        docs = []
        cursor = self.db.knowledge.find({
            "is_temporary": True,
            "expires_at": {"$lte": datetime.utcnow()},
            "is_active": True
        })
        async for doc_data in cursor:
            docs.append(KnowledgeDocument(**doc_data))
        return docs
    
    async def get_knowledge_by_category(self, category: str) -> List[KnowledgeDocument]:
        """Get knowledge documents by category"""
        docs = []
        cursor = self.db.knowledge.find({
            "category": category,
            "is_active": True
        }).sort("created_at", DESCENDING)
        async for doc_data in cursor:
            docs.append(KnowledgeDocument(**doc_data))
        return docs
    
    # Agent Operations
    async def create_agent(self, agent: Agent) -> str:
        """Create a new agent"""
        agent_dict = agent.model_dump(by_alias=True, exclude={"id"})
        result = await self.db.agents.insert_one(agent_dict)
        return str(result.inserted_id)
    
    async def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get an agent by agent_id"""
        agent_data = await self.db.agents.find_one({"agent_id": agent_id})
        if agent_data:
            return Agent(**agent_data)
        return None
    
    async def get_agent_by_email(self, email: str) -> Optional[Agent]:
        """Get an agent by email"""
        agent_data = await self.db.agents.find_one({"email": email})
        if agent_data:
            return Agent(**agent_data)
        return None
    
    async def get_all_agents(self, active_only: bool = True) -> List[Agent]:
        """Get all agents"""
        agents = []
        query = {"is_active": True} if active_only else {}
        cursor = self.db.agents.find(query).sort("name", ASCENDING)
        async for agent_data in cursor:
            agents.append(Agent(**agent_data))
        return agents
    
    async def update_agent(self, agent_id: str, update_data: dict):
        """Update an agent"""
        update_data["updated_at"] = datetime.utcnow()
        await self.db.agents.update_one(
            {"agent_id": agent_id},
            {"$set": update_data}
        )
    
    async def increment_agent_load(self, agent_id: str):
        """Increment agent's current load"""
        await self.db.agents.update_one(
            {"agent_id": agent_id},
            {
                "$inc": {"current_load": 1, "total_assigned": 1},
                "$set": {"last_assigned_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
            }
        )
    
    async def decrement_agent_load(self, agent_id: str):
        """Decrement agent's current load"""
        await self.db.agents.update_one(
            {"agent_id": agent_id},
            {
                "$inc": {"current_load": -1, "total_resolved": 1},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
    
    async def get_agents_by_skill(self, skill: str, active_only: bool = True) -> List[Agent]:
        """Get agents with a specific skill"""
        agents = []
        query = {"skills": skill}
        if active_only:
            query["is_active"] = True
        cursor = self.db.agents.find(query).sort("current_load", ASCENDING)
        async for agent_data in cursor:
            agents.append(Agent(**agent_data))
        return agents
    
    async def find_best_agent(self, required_skills: List[str], channel: str) -> Optional[Agent]:
        """Find the best available agent based on skills, load, and channel"""
        # Build query for agents with required skills, active, and supporting the channel
        query = {
            "is_active": True,
            "channels": channel,
            "$expr": {"$lt": ["$current_load", "$max_concurrent_tickets"]}
        }
        
        # If skills are required, match them
        if required_skills:
            query["skills"] = {"$in": required_skills}
        
        # Sort by: skill match count (desc), then current load (asc)
        pipeline = [
            {"$match": query},
            {
                "$addFields": {
                    "skill_match_count": {
                        "$size": {
                            "$setIntersection": ["$skills", required_skills] if required_skills else []
                        }
                    }
                }
            },
            {"$sort": {"skill_match_count": -1, "current_load": 1}},
            {"$limit": 1}
        ]
        
        cursor = self.db.agents.aggregate(pipeline)
        async for agent_data in cursor:
            return Agent(**agent_data)
        
        # If no skilled agent found, find any available agent
        fallback_query = {
            "is_active": True,
            "channels": channel,
            "$expr": {"$lt": ["$current_load", "$max_concurrent_tickets"]}
        }
        agent_data = await self.db.agents.find_one(fallback_query, sort=[("current_load", ASCENDING)])
        if agent_data:
            return Agent(**agent_data)
        
        return None
    
    # SLA and Escalation Helpers
    def calculate_sla_deadlines(self, ticket: SupportTicket) -> Dict[str, datetime]:
        """Calculate SLA deadlines based on priority"""
        now = ticket.created_at
        
        # SLA times based on priority (in minutes)
        sla_matrix = {
            "urgent": {"response": 15, "resolution": 60},
            "high": {"response": 30, "resolution": 120},
            "medium": {"response": 60, "resolution": 240},
            "low": {"response": 120, "resolution": 480}
        }
        
        sla_times = sla_matrix.get(ticket.priority, sla_matrix["medium"])
        
        return {
            "response_deadline": now + timedelta(minutes=sla_times["response"]),
            "resolution_deadline": now + timedelta(minutes=sla_times["resolution"])
        }
    
    async def check_sla_breaches(self) -> List[SupportTicket]:
        """Find tickets with SLA breaches"""
        now = datetime.utcnow()
        
        # Find tickets where deadlines have passed
        query = {
            "status": {"$in": ["open", "pending"]},
            "$or": [
                {"sla_response_deadline": {"$lt": now}, "first_response_at": None},
                {"sla_resolution_deadline": {"$lt": now}, "resolved_at": None}
            ]
        }
        
        tickets = []
        cursor = self.db.tickets.find(query)
        async for ticket_data in cursor:
            tickets.append(SupportTicket(**ticket_data))
        return tickets
    
    async def get_escalation_agent(self, current_tier: int, skills: List[str], domain: str = "IT") -> Optional[Agent]:
        """Find agent for escalation (higher tier)"""
        query = {
            "is_active": True,
            "tier": {"$gt": current_tier},  # Higher tier
            "handles_escalations": True,
            "domain": domain,
            "$expr": {"$lt": ["$current_load", "$max_concurrent_tickets"]}
        }
        
        if skills:
            query["skills"] = {"$in": skills}
        
        # Sort by tier (ascending), then load (ascending)
        agent_data = await self.db.agents.find_one(
            query,
            sort=[("tier", ASCENDING), ("current_load", ASCENDING)]
        )
        
        if agent_data:
            return Agent(**agent_data)
        return None
    
    # ========================================================================
    # SLA POLICY MANAGEMENT
    # ========================================================================
    
    async def create_sla_policy(self, policy: SLAPolicy) -> str:
        """Create a new SLA policy"""
        policy_dict = policy.model_dump(by_alias=True, exclude={"id"})
        result = await self.db.sla_policies.insert_one(policy_dict)
        return str(result.inserted_id)
    
    async def get_sla_policy(self, policy_id: str) -> Optional[SLAPolicy]:
        """Get SLA policy by policy_id"""
        policy_data = await self.db.sla_policies.find_one({"policy_id": policy_id})
        if policy_data:
            return SLAPolicy(**policy_data)
        return None
    
    async def get_all_sla_policies(self, domain: str = None, is_active: bool = None) -> List[SLAPolicy]:
        """Get all SLA policies with optional filters"""
        query = {}
        if domain:
            query["domain"] = domain
        if is_active is not None:
            query["is_active"] = is_active
        
        policies = []
        cursor = self.db.sla_policies.find(query).sort("priority_order", DESCENDING)
        async for policy_data in cursor:
            policies.append(SLAPolicy(**policy_data))
        return policies
    
    async def update_sla_policy(self, policy_id: str, update_data: Dict[str, Any]) -> bool:
        """Update SLA policy"""
        update_data["updated_at"] = datetime.utcnow()
        result = await self.db.sla_policies.update_one(
            {"policy_id": policy_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    async def delete_sla_policy(self, policy_id: str) -> bool:
        """Delete SLA policy (soft delete by deactivating)"""
        result = await self.db.sla_policies.update_one(
            {"policy_id": policy_id},
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    async def find_matching_sla_policy(
        self,
        domain: str,
        category: str = None,
        priority: str = None,
        customer_tier: str = "standard"
    ) -> Optional[SLAPolicy]:
        """
        Find the best matching SLA policy for a ticket
        Returns the most specific policy that matches the criteria
        """
        query = {
            "is_active": True,
            "domain": domain
        }
        
        # Get all active policies for the domain, sorted by priority_order
        all_policies = await self.get_all_sla_policies(domain=domain, is_active=True)
        
        # Score each policy based on specificity
        best_policy = None
        best_score = -1
        
        for policy in all_policies:
            score = 0
            
            # Check if policy applies to this category
            if category and policy.categories:
                if category not in policy.categories:
                    continue
                score += 10  # Category match is highly specific
            
            # Check if policy applies to this priority
            if priority and policy.priorities:
                if priority not in policy.priorities:
                    continue
                score += 5  # Priority match is somewhat specific
            
            # Check customer tier
            if customer_tier in policy.customer_tiers:
                score += 3
            
            # Add policy priority order
            score += policy.priority_order
            
            # If this policy is more specific, use it
            if score > best_score:
                best_score = score
                best_policy = policy
            
            # Use default policy if no better match
            if policy.is_default and best_policy is None:
                best_policy = policy
        
        return best_policy
    
    # SLA Template Management
    async def create_sla_template(self, template: SLATemplate) -> str:
        """Create a new SLA template"""
        template_dict = template.model_dump(by_alias=True, exclude={"id"})
        result = await self.db.sla_templates.insert_one(template_dict)
        return str(result.inserted_id)
    
    async def get_sla_template(self, template_id: str) -> Optional[SLATemplate]:
        """Get SLA template by template_id"""
        template_data = await self.db.sla_templates.find_one({"template_id": template_id})
        if template_data:
            return SLATemplate(**template_data)
        return None
    
    async def get_all_sla_templates(self, category: str = None) -> List[SLATemplate]:
        """Get all SLA templates"""
        query = {"is_active": True}
        if category:
            query["category"] = category
        
        templates = []
        cursor = self.db.sla_templates.find(query)
        async for template_data in cursor:
            templates.append(SLATemplate(**template_data))
        return templates
    
    async def apply_sla_template(self, template_id: str, domain: str = "IT") -> List[str]:
        """Apply an SLA template to create multiple policies"""
        template = await self.get_sla_template(template_id)
        if not template:
            return []
        
        created_policy_ids = []
        for policy_data in template.policies:
            # Override domain if specified
            policy_data["domain"] = domain
            policy = SLAPolicy(**policy_data)
            policy_id = await self.create_sla_policy(policy)
            created_policy_ids.append(policy_id)
        
        return created_policy_ids
    
    # ========================================================================
    # HOLIDAY CALENDAR MANAGEMENT
    # ========================================================================
    
    async def create_holiday(self, holiday: Holiday) -> str:
        """Create a new holiday entry"""
        holiday_dict = holiday.model_dump(by_alias=True, exclude={"id"})
        result = await self.db.holidays.insert_one(holiday_dict)
        return str(result.inserted_id)
    
    async def get_holidays(self, year: int = None, holiday_type: str = None, region: str = None) -> List[Holiday]:
        """Get holidays with optional filters"""
        query = {}
        if year:
            query["date"] = {"$regex": f"^{year}-"}
        if holiday_type:
            query["holiday_type"] = holiday_type
        if region:
            query["region"] = region
        
        holidays = []
        cursor = self.db.holidays.find(query).sort("date", ASCENDING)
        async for holiday_data in cursor:
            holidays.append(Holiday(**holiday_data))
        return holidays
    
    async def is_holiday(self, date: str, region: str = None) -> bool:
        """Check if a date is a holiday"""
        query = {"date": date, "is_working_day": False}
        if region:
            query["$or"] = [
                {"region": region},
                {"region": None},  # National holidays
                {"holiday_type": "national"}
            ]
        else:
            query["holiday_type"] = "national"
        
        holiday = await self.db.holidays.find_one(query)
        return holiday is not None
    
    # Agent Holiday Management
    async def create_agent_holiday(self, agent_holiday: AgentHoliday) -> str:
        """Create agent holiday/leave entry"""
        holiday_dict = agent_holiday.model_dump(by_alias=True, exclude={"id"})
        result = await self.db.agent_holidays.insert_one(holiday_dict)
        return str(result.inserted_id)
    
    async def get_agent_holidays(self, agent_id: str, start_date: str = None, end_date: str = None) -> List[AgentHoliday]:
        """Get agent holidays within date range"""
        query = {"agent_id": agent_id}
        if start_date and end_date:
            query["date"] = {"$gte": start_date, "$lte": end_date}
        elif start_date:
            query["date"] = {"$gte": start_date}
        elif end_date:
            query["date"] = {"$lte": end_date}
        
        holidays = []
        cursor = self.db.agent_holidays.find(query).sort("date", ASCENDING)
        async for holiday_data in cursor:
            holidays.append(AgentHoliday(**holiday_data))
        return holidays
    
    async def is_agent_on_holiday(self, agent_id: str, date: str, time: str = None) -> bool:
        """Check if agent is on holiday/leave on a specific date and time"""
        query = {
            "agent_id": agent_id,
            "date": date,
            "is_working_day": False
        }
        
        # If time is provided, check for partial day leaves
        if time:
            query["$or"] = [
                {"start_time": None, "end_time": None},  # Full day leave
                {"start_time": {"$lte": time}, "end_time": {"$gte": time}}  # Partial day leave
            ]
        
        holiday = await self.db.agent_holidays.find_one(query)
        return holiday is not None
    
    async def get_available_agents(self, date: str = None, time: str = None, skills: List[str] = None, domain: str = "IT") -> List[Agent]:
        """Get agents available (considering skills and workload only, holidays ignored)"""
        # First get all active agents with required skills
        query = {
            "is_active": True,
            "$expr": {"$lt": ["$current_load", "$max_concurrent_tickets"]}
        }
        
        if skills:
            query["skills"] = {"$in": skills}
        
        print(f"   [DEBUG] Query for available agents:")
        print(f"      - Skills filter: {skills}")
        print(f"      - Query: {query}")
        
        available_agents = []
        total_agents = 0
        
        # Debug: Count total agents first
        async for _ in self.db.agents.find({"is_active": True}):
            total_agents += 1
        
        print(f"   [DEBUG] Total active agents in DB: {total_agents}")
        
        # Debug: Check domain distribution
        domain_counts = {}
        async for agent_data in self.db.agents.find({"is_active": True}):
            domain_counts[agent_data.get("domain", "unknown")] = domain_counts.get(agent_data.get("domain", "unknown"), 0) + 1
        print(f"   [DEBUG] Agents by domain: {domain_counts}")
        
        # Debug: Check agents with matching skills
        if skills:
            async for agent_data in self.db.agents.find({"is_active": True, "skills": {"$in": skills}}):
                agent_domain = agent_data.get("domain", "unknown")
                agent_skills = agent_data.get("skills", [])
                print(f"   [DEBUG] Found agent with matching skills: {agent_data.get('name')} (domain={agent_domain}, skills={agent_skills}, load={agent_data.get('current_load')}/{agent_data.get('max_concurrent_tickets')})")
        
        cursor = self.db.agents.find(query)
        async for agent_data in cursor:
            agent = Agent(**agent_data)
            available_agents.append(agent)
            print(f"   [DEBUG] Added agent: {agent.name} (load: {agent.current_load}/{agent.max_concurrent_tickets})")
        
        print(f"   [DEBUG] Found {len(available_agents)} available agents")
        return available_agents
    
    async def update_agent_holiday(self, holiday_id: str, update_data: Dict[str, Any]) -> bool:
        """Update agent holiday entry"""
        update_data["updated_at"] = datetime.utcnow()
        result = await self.db.agent_holidays.update_one(
            {"_id": ObjectId(holiday_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    async def delete_agent_holiday(self, holiday_id: str) -> bool:
        """Delete agent holiday entry"""
        result = await self.db.agent_holidays.delete_one({"_id": ObjectId(holiday_id)})
        return result.deleted_count > 0
    
    # ========================================================================
    # SYSTEM CONFIGURATION MANAGEMENT
    # ========================================================================
    
    async def get_system_config(self) -> Optional[SystemConfiguration]:
        """Get system configuration"""
        config_data = await self.db.configurations.find_one({"config_id": "system_config"})
        if config_data:
            return SystemConfiguration(**config_data)
        return None
    
    async def update_system_config(self, config: SystemConfiguration) -> bool:
        """Update or create system configuration"""
        config_dict = config.model_dump(by_alias=True, exclude={"id"})
        config_dict["updated_at"] = datetime.utcnow()
        
        result = await self.db.configurations.update_one(
            {"config_id": "system_config"},
            {"$set": config_dict},
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None

    # ========================================================================
    # ENHANCED CONFIGURATION MANAGEMENT
    # ========================================================================
    
    async def get_enhanced_config(self) -> Optional[EnhancedSystemConfiguration]:
        """Get enhanced system configuration"""
        config_data = await self.db.enhanced_configurations.find_one({"config_id": "enhanced_system_config"})
        if config_data:
            return EnhancedSystemConfiguration(**config_data)
        return None
    
    async def update_enhanced_config(self, config: EnhancedSystemConfiguration) -> bool:
        """Update or create enhanced system configuration"""
        config_dict = config.model_dump(by_alias=True, exclude={"id"})
        config_dict["updated_at"] = datetime.utcnow()
        config_dict["config_id"] = "enhanced_system_config"
        
        result = await self.db.enhanced_configurations.update_one(
            {"config_id": "enhanced_system_config"},
            {"$set": config_dict},
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None
    
    async def get_config_section(self, section: str) -> Optional[Dict[str, Any]]:
        """Get specific configuration section (email, whatsapp, sms, model, vector_db, knowledge_provider)"""
        config = await self.get_enhanced_config()
        if not config:
            return None
        
        section_map = {
            "email": config.email.model_dump(),
            "whatsapp": config.whatsapp.model_dump(),
            "sms": config.sms.model_dump(),
            "model": config.model.model_dump(),
            "vector_db": config.vector_db.model_dump(),
            "knowledge_provider": config.knowledge_provider.model_dump()
        }
        
        return section_map.get(section)
    
    async def update_config_section(self, section: str, section_config: Dict[str, Any]) -> bool:
        """Update specific configuration section"""
        config = await self.get_enhanced_config()
        if not config:
            config = EnhancedSystemConfiguration()
        
        # Update the specific section
        if section == "email":
            config.email = EmailConfig(**section_config)
        elif section == "whatsapp":
            config.whatsapp = WhatsAppConfig(**section_config)
        elif section == "sms":
            config.sms = SMSConfig(**section_config)
        elif section == "model":
            config.model = ModelConfig(**section_config)
        elif section == "vector_db":
            config.vector_db = VectorDBConfig(**section_config)
        elif section == "knowledge_provider":
            config.knowledge_provider = KnowledgeProviderConfig(**section_config)
        else:
            return False
        
        config.updated_at = datetime.utcnow()
        return await self.update_enhanced_config(config)


# Global database manager instance
db_manager = DatabaseManager()

