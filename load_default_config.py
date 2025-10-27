"""
Script to load default enhanced configuration into MongoDB
"""
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.database import (
    EnhancedSystemConfiguration,
    EmailConfig,
    WhatsAppConfig,
    SMSConfig,
    ModelConfig,
    VectorDBConfig,
    KnowledgeProviderConfig
)

async def load_default_config():
    """Load default enhanced configuration into database"""
    print("=" * 80)
    print("Loading Default Enhanced Configuration")
    print("=" * 80)
    
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(settings.mongodb_url)
        db = client[settings.mongodb_db_name]
        enhanced_configs = db.enhanced_configurations
        
        # Create default configuration
        default_config = EnhancedSystemConfiguration(
            config_id="enhanced_system_config",
            email=EmailConfig(
                support_email="r15528850@gmail.com",
                email_host="smtp.gmail.com",
                email_port=587,
                email_user=None,
                email_password=None,
                use_tls=True,
                use_ssl=False
            ),
            whatsapp=WhatsAppConfig(
                enabled=False,
                whatsapp_number="whatsapp:+14155238886",
                twilio_account_sid=None,
                twilio_auth_token=None,
                twilio_phone_number=None
            ),
            sms=SMSConfig(
                enabled=False,
                sms_phone_number=None,
                twilio_account_sid=None,
                twilio_auth_token=None,
                twilio_phone_number=None
            ),
            model=ModelConfig(
                llm_provider="openai",
                llm_model="gpt-3.5-turbo",
                llm_api_key=None,
                llm_base_url=None,
                llm_temperature=0.7,
                llm_max_tokens=2000,
                embedding_provider="openai",
                embedding_model="text-embedding-ada-002",
                embedding_api_key=None,
                embedding_base_url=None,
                embedding_dimensions=1536
            ),
            vector_db=VectorDBConfig(
                provider="chroma",
                enabled=True,
                chroma_host="localhost",
                chroma_port=8000,
                chroma_collection_name="knowledge_base",
                chroma_persist_directory=None,
                pinecone_api_key=None,
                pinecone_environment=None,
                pinecone_index_name="knowledge-base",
                pinecone_namespace=None,
                weaviate_url="http://localhost:8080",
                weaviate_api_key=None,
                weaviate_class_name="KnowledgeDocument",
                faiss_index_path="./vector_store/faiss_index",
                faiss_index_type="Flat"
            ),
            knowledge_provider=KnowledgeProviderConfig(
                provider="local",
                enabled=True,
                aws_access_key_id=None,
                aws_secret_access_key=None,
                aws_region="us-east-1",
                aws_bucket_name=None,
                aws_prefix="knowledge-base/",
                azure_account_name=None,
                azure_account_key=None,
                azure_container_name=None,
                azure_connection_string=None,
                google_credentials_file=None,
                google_folder_id=None,
                google_service_account_email=None,
                dropbox_access_token=None,
                dropbox_folder_path="/knowledge-base"
            ),
            chat_enabled=True,
            auto_assignment_enabled=True,
            escalation_enabled=True,
            notification_enabled=True
        )
        
        # Check if config already exists
        existing = await enhanced_configs.find_one({"config_id": "enhanced_system_config"})
        
        if existing:
            print("⚠️  Configuration already exists in database")
            print("✅ Skipping - use update API to modify configuration")
            return
        else:
            # Insert default configuration
            config_dict = default_config.model_dump(by_alias=True, exclude={"id"})
            result = await enhanced_configs.insert_one(config_dict)
            
            print("✅ Default enhanced configuration loaded successfully!")
            print(f"   Configuration ID: {result.inserted_id}")
            print("\n📋 Configuration Summary:")
            print(f"   Email: {default_config.email.support_email}")
            print(f"   WhatsApp: {'Enabled' if default_config.whatsapp.enabled else 'Disabled'}")
            print(f"   SMS: {'Enabled' if default_config.sms.enabled else 'Disabled'}")
            print(f"   LLM Provider: {default_config.model.llm_provider}")
            print(f"   LLM Model: {default_config.model.llm_model}")
            print(f"   Vector DB: {default_config.vector_db.provider}")
            print(f"   Knowledge Provider: {default_config.knowledge_provider.provider}")
        
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        client.close()
        print("\n" + "=" * 80)

if __name__ == "__main__":
    asyncio.run(load_default_config())

