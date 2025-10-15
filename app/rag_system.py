"""
RAG (Retrieval Augmented Generation) System using Langchain
"""
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import os
from pathlib import Path
from app.config import settings
from app.database import db_manager, KnowledgeDocument


class RAGSystem:
    """RAG System for intelligent customer support"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.openai_api_key,
            model=settings.embeddings_model
        )
        self.llm = ChatOpenAI(
            openai_api_key=settings.openai_api_key,
            model=settings.llm_model,
            temperature=0.3
        )
        self.vector_store = None
        self.qa_chain = None
        
        # Create vector store directory if it doesn't exist
        Path(settings.vector_store_path).mkdir(parents=True, exist_ok=True)
        Path(settings.knowledge_base_path).mkdir(parents=True, exist_ok=True)
    
    async def initialize(self):
        """Initialize the RAG system"""
        # Load or create vector store
        if os.path.exists(settings.vector_store_path) and os.listdir(settings.vector_store_path):
            print("Loading existing vector store...")
            self.vector_store = Chroma(
                persist_directory=settings.vector_store_path,
                embedding_function=self.embeddings
            )
        else:
            print("Creating new vector store...")
            self.vector_store = Chroma(
                persist_directory=settings.vector_store_path,
                embedding_function=self.embeddings
            )
        
        # Create QA chain with custom prompt
        self._create_qa_chain()
        
        print("✓ RAG System initialized")
    
    def _create_qa_chain(self):
        """Create the QA chain with custom prompt"""
        template = """You are an intelligent IT support assistant. Your job is to answer the CURRENT customer question using ONLY the provided context.

CRITICAL RULES:
1. ONLY use information from the Context below to answer the question
2. DO NOT use information from previous conversations or questions
3. DO NOT make assumptions or provide information not in the Context
4. If the Context does not contain relevant information for the CURRENT question, say: "I don't have specific information about this issue in my knowledge base. I'll escalate this to a specialized support agent who can help you better."
5. Each question should be treated as a NEW, INDEPENDENT query
6. DO NOT mix answers from different topics

Context (Knowledge Base Information):
{context}

Current Customer Question (treat this as a NEW question):
{question}

Instructions:
- Read the CURRENT question carefully
- Check if the Context above contains relevant information for THIS specific question
- If YES: Provide a clear, step-by-step solution based ONLY on the Context
- If NO: Admit you don't have the information and will escalate
- DO NOT reference previous questions or answers
- Focus ONLY on the current question

Professional Answer:"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 5}
            ),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )
    
    async def add_documents_to_knowledge_base(
        self,
        documents: List[Dict[str, Any]],
        category: str = "general",
        is_temporary: bool = False,
        expires_in_days: Optional[int] = None,
        created_by: Optional[str] = None
    ) -> List[str]:
        """
        Add documents to the knowledge base and vector store
        
        Args:
            documents: List of dicts with 'title', 'content', and optional 'tags'
            category: Category for the documents
            is_temporary: Whether this is temporary knowledge
            expires_in_days: Number of days until expiry (for temporary knowledge)
            created_by: User who created this document
        
        Returns:
            List of created document IDs
        """
        doc_ids = []
        
        # Text splitter for chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        for doc_data in documents:
            # Calculate expiry date if temporary
            expires_at = None
            if is_temporary and expires_in_days:
                expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
            
            # Split and add to vector store first to get chunk IDs
            chunks = text_splitter.split_text(doc_data["content"])
            
            # Create Langchain documents with unique IDs
            chunk_ids = []
            langchain_docs = []
            
            for idx, chunk in enumerate(chunks):
                chunk_id = f"{doc_data['title'][:20]}_{idx}_{datetime.utcnow().timestamp()}"
                chunk_ids.append(chunk_id)
                
                langchain_docs.append(Document(
                    page_content=chunk,
                    metadata={
                        "title": doc_data["title"],
                        "category": category,
                        "chunk_id": chunk_id,
                        "source": doc_data.get("source", "manual"),
                        "file_name": doc_data.get("file_name"),
                        "file_type": doc_data.get("file_type")
                    }
                )
            )
            
            # Add to vector store
            vector_ids = self.vector_store.add_documents(langchain_docs)
            
            # Create knowledge document in MongoDB
            knowledge_doc = KnowledgeDocument(
                title=doc_data["title"],
                content=doc_data["content"],
                category=category,
                tags=doc_data.get("tags", []),
                source=doc_data.get("source"),
                file_name=doc_data.get("file_name"),
                file_type=doc_data.get("file_type"),
                chunk_ids=chunk_ids,
                is_temporary=is_temporary,
                expires_at=expires_at,
                created_by=created_by
            )
            
            doc_id = await db_manager.create_knowledge_document(knowledge_doc)
            doc_ids.append(doc_id)
        
        # Persist vector store
        self.vector_store.persist()
        
        return doc_ids
    
    async def update_document_in_knowledge_base(
        self,
        doc_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """Update a document in the knowledge base"""
        try:
            # Get existing document
            doc = await db_manager.get_knowledge_document(doc_id)
            if not doc:
                return False
            
            # If content is updated, we need to update vector store
            if content and content != doc.content:
                # Delete old chunks from vector store
                await self._delete_document_chunks(doc.chunk_ids)
                
                # Add new chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )
                chunks = text_splitter.split_text(content)
                
                chunk_ids = []
                langchain_docs = []
                
                for idx, chunk in enumerate(chunks):
                    chunk_id = f"{(title or doc.title)[:20]}_{idx}_{datetime.utcnow().timestamp()}"
                    chunk_ids.append(chunk_id)
                    
                    langchain_docs.append(Document(
                        page_content=chunk,
                        metadata={
                            "title": title or doc.title,
                            "category": category or doc.category,
                            "chunk_id": chunk_id,
                            "doc_id": doc_id,
                            "source": doc.source
                        }
                    ))
                
                self.vector_store.add_documents(langchain_docs)
                self.vector_store.persist()
            else:
                chunk_ids = doc.chunk_ids
            
            # Update MongoDB document
            update_data = {}
            if title:
                update_data["title"] = title
            if content:
                update_data["content"] = content
                update_data["chunk_ids"] = chunk_ids
            if category:
                update_data["category"] = category
            if tags is not None:
                update_data["tags"] = tags
            
            await db_manager.update_knowledge_document(doc_id, update_data)
            
            return True
        
        except Exception as e:
            print(f"Error updating document: {e}")
            return False
    
    async def delete_document_from_knowledge_base(
        self,
        doc_id: str,
        hard_delete: bool = False
    ) -> bool:
        """Delete a document from the knowledge base"""
        try:
            # Get document
            doc = await db_manager.get_knowledge_document(doc_id)
            if not doc:
                return False
            
            # Delete chunks from vector store
            await self._delete_document_chunks(doc.chunk_ids)
            
            # Delete from MongoDB (soft or hard)
            await db_manager.delete_knowledge_document(doc_id, soft_delete=not hard_delete)
            
            # Persist vector store
            self.vector_store.persist()
            
            return True
        
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    async def _delete_document_chunks(self, chunk_ids: List[str]):
        """Delete document chunks from vector store"""
        try:
            # ChromaDB delete by metadata
            for chunk_id in chunk_ids:
                try:
                    self.vector_store.delete(
                        where={"chunk_id": chunk_id}
                    )
                except:
                    pass  # Chunk might not exist
        except Exception as e:
            print(f"Warning: Error deleting chunks from vector store: {e}")
    
    async def load_documents_from_files(self, file_paths: List[str]) -> List[str]:
        """Load documents from files (PDF, DOCX, TXT)"""
        from PyPDF2 import PdfReader
        from docx import Document as DocxDocument
        
        documents = []
        
        for file_path in file_paths:
            path = Path(file_path)
            
            if not path.exists():
                print(f"File not found: {file_path}")
                continue
            
            content = ""
            
            if path.suffix.lower() == ".pdf":
                reader = PdfReader(file_path)
                content = "\n".join([page.extract_text() for page in reader.pages])
            
            elif path.suffix.lower() == ".docx":
                doc = DocxDocument(file_path)
                content = "\n".join([para.text for para in doc.paragraphs])
            
            elif path.suffix.lower() == ".txt":
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            
            else:
                print(f"Unsupported file type: {path.suffix}")
                continue
            
            documents.append({
                "title": path.stem,
                "content": content,
                "source": str(file_path),
                "tags": []
            })
        
        return await self.add_documents_to_knowledge_base(documents)
    
    async def query(
        self,
        question: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        domain: str = "IT"
    ) -> Dict[str, Any]:
        """
        Query the knowledge base with domain filtering and priority-based retrieval
        
        Args:
            question: The customer's question
            conversation_history: Optional conversation history (NOT USED to prevent context bleeding)
            domain: Support domain ("IT" or "AIRLINE") for filtering knowledge base
        
        Returns:
            Dict with 'answer', 'source_documents', and 'confidence'
        """
        # IMPORTANT: Each question is treated as INDEPENDENT to prevent hallucination
        # We do NOT add conversation history to avoid context bleeding between different topics
        # The prompt explicitly instructs the model to focus only on the current question
        
        # Get domain-specific and priority-filtered documents
        # Higher priority documents will be retrieved first
        from app.database import db_manager
        
        # Get active knowledge documents for this domain, sorted by priority (desc)
        kb_docs = await db_manager.db.knowledge.find({
            "is_active": True,
            "domain": domain
        }).sort("priority", -1).to_list(length=None)
        
        # Filter chunk IDs by domain and priority for better retrieval
        # This ensures high-priority, domain-specific knowledge is preferred
        domain_chunk_ids = []
        for doc in kb_docs:
            if doc.get("chunk_ids"):
                domain_chunk_ids.extend(doc["chunk_ids"])
        
        # Query the chain with ONLY the current question
        # The retriever will prioritize chunks from high-priority documents
        result = self.qa_chain({"query": question})
        
        # Determine confidence based on source documents similarity
        confidence = self._calculate_confidence(result.get("source_documents", []))
        
        # Get the answer
        answer = result["result"]
        
        # CRITICAL FIX: Check if the answer indicates lack of knowledge
        # If the LLM says it doesn't know, force low confidence to trigger auto-assignment
        low_confidence_phrases = [
            "i don't have",
            "i do not have",
            "not in my knowledge base",
            "cannot find",
            "unable to find",
            "i'll escalate",
            "i will escalate",
            "specialized support agent",
            "escalate this",
            "contact a specialist",
            "no information about"
        ]
        
        answer_lower = answer.lower()
        has_low_confidence_phrase = any(phrase in answer_lower for phrase in low_confidence_phrases)
        
        # Override confidence if answer indicates lack of knowledge
        if has_low_confidence_phrase:
            confidence = min(confidence, 0.3)  # Force low confidence for escalation responses
        
        return {
            "answer": answer,
            "source_documents": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in result.get("source_documents", [])
            ],
            "confidence": confidence,
            "can_auto_respond": confidence > 0.7  # Auto-respond if confidence > 70%
        }
    
    def _calculate_confidence(self, source_documents: List) -> float:
        """Calculate confidence score based on retrieved documents"""
        if not source_documents:
            return 0.0
        
        # IMPROVED: Use similarity scores if available, fallback to count-based
        # ChromaDB returns documents with scores in metadata
        total_score = 0.0
        scored_docs = 0
        
        for doc in source_documents:
            # Check if document has similarity score in metadata
            if hasattr(doc, 'metadata') and doc.metadata:
                # ChromaDB may store score differently depending on version
                score = doc.metadata.get('score', None) or doc.metadata.get('similarity', None)
                if score is not None:
                    total_score += float(score)
                    scored_docs += 1
        
        # If we have similarity scores, use average score
        if scored_docs > 0:
            avg_score = total_score / scored_docs
            # Normalize to 0-1 range (assuming scores are between 0-1)
            # Higher score = better match
            confidence = min(avg_score, 1.0)
        else:
            # Fallback to count-based (conservative - requires more docs for high confidence)
            # Reduced from 5.0 to 8.0 to make it harder to get high confidence
            confidence = min(len(source_documents) / 8.0, 0.8)  # Max 0.8 for count-based
        
        return confidence
    
    async def get_similar_documents(
        self,
        query: str,
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """Get similar documents from the knowledge base"""
        results = self.vector_store.similarity_search_with_score(query, k=k)
        
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "similarity_score": float(score)
            }
            for doc, score in results
        ]


# Global RAG system instance
rag_system = RAGSystem()

