"""
RAG (Retrieval Augmented Generation) System using Langchain
"""
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
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
        
        # Create vector store directory if it doesn't exist
        Path(settings.vector_store_path).mkdir(parents=True, exist_ok=True)
        Path(settings.knowledge_base_path).mkdir(parents=True, exist_ok=True)
    
    async def initialize(self):
        """Initialize the RAG system"""
        # Load or create vector store
        try:
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
            print("Vector store initialized")
        except Exception as e:
            print(f"WARNING: Error initializing vector store: {e}")
            print("Creating fresh vector store...")
            self.vector_store = Chroma(
                persist_directory=settings.vector_store_path,
                embedding_function=self.embeddings
            )
        
        print("RAG System initialized")
    
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
        
        # Try to persist (some versions don't have this method)
        try:
            if hasattr(self.vector_store, 'persist'):
                self.vector_store.persist()
                print(f"[RAG] Vector store persisted after adding documents")
        except:
            pass  # Vector store persists automatically in newer versions
        
        return doc_ids
    
    async def update_document_in_knowledge_base(
        self,
        doc_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """Update a document in the knowledge base and sync vector store"""
        try:
            # Get existing document
            doc = await db_manager.get_knowledge_document(doc_id)
            if not doc:
                print(f"[RAG] Document {doc_id} not found")
                return False
            
            print(f"[RAG] Updating document: {doc.title}")
            
            # If content is updated, we need to update vector store
            if content and content != doc.content:
                print(f"[RAG] Content changed, updating vector store...")
                
                # Delete old chunks from vector store
                print(f"[RAG] Deleting old {len(doc.chunk_ids)} chunks...")
                await self._delete_document_chunks(doc.chunk_ids)
                
                # Add new chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )
                chunks = text_splitter.split_text(content)
                print(f"[RAG] Created {len(chunks)} new chunks")
                
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
                
                # Add new chunks to vector store
                self.vector_store.add_documents(langchain_docs)
                print(f"[RAG] Added {len(langchain_docs)} new chunks to vector store")
                
                # Try to persist (some versions don't have this method)
                try:
                    if hasattr(self.vector_store, 'persist'):
                        self.vector_store.persist()
                        print(f"[RAG] Vector store persisted")
                except:
                    pass  # Vector store persists automatically in newer versions
            else:
                chunk_ids = doc.chunk_ids
                print(f"[RAG] Content unchanged, keeping existing {len(chunk_ids)} chunks")
            
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
            print(f"[RAG] Successfully updated document {doc_id}")
            
            return True
        
        except Exception as e:
            print(f"[RAG] Error updating document: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def delete_document_from_knowledge_base(
        self,
        doc_id: str,
        hard_delete: bool = False
    ) -> bool:
        """Delete a document from the knowledge base and sync vector store"""
        try:
            # Get document
            doc = await db_manager.get_knowledge_document(doc_id)
            if not doc:
                print(f"[RAG] Document {doc_id} not found")
                return False
            
            print(f"[RAG] Deleting document: {doc.title}")
            
            # Delete chunks from vector store
            print(f"[RAG] Deleting {len(doc.chunk_ids)} chunks from vector store...")
            await self._delete_document_chunks(doc.chunk_ids)
            
            # Delete from MongoDB (soft or hard)
            delete_type = "soft" if not hard_delete else "hard"
            print(f"[RAG] Deleting from MongoDB ({delete_type} delete)...")
            await db_manager.delete_knowledge_document(doc_id, soft_delete=not hard_delete)
            
            # Try to persist (some versions don't have this method)
            try:
                if hasattr(self.vector_store, 'persist'):
                    self.vector_store.persist()
                    print(f"[RAG] Vector store persisted")
            except:
                pass  # Vector store persists automatically in newer versions
            
            print(f"[RAG] Successfully deleted document {doc_id}")
            
            return True
        
        except Exception as e:
            print(f"[RAG] Error deleting document: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def _delete_document_chunks(self, chunk_ids: List[str]):
        """Delete document chunks from vector store"""
        if not chunk_ids:
            print(f"[RAG] No chunks to delete")
            return
        
        try:
            deleted_count = 0
            # ChromaDB delete by metadata
            for chunk_id in chunk_ids:
                try:
                    self.vector_store.delete(
                        where={"chunk_id": chunk_id}
                    )
                    deleted_count += 1
                except Exception as del_error:
                    print(f"[RAG] Warning: Could not delete chunk {chunk_id}: {del_error}")
            
            print(f"[RAG] Deleted {deleted_count}/{len(chunk_ids)} chunks from vector store")
        except Exception as e:
            print(f"[RAG] Error deleting chunks from vector store: {e}")
            import traceback
            traceback.print_exc()
    
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
       # domain: str = "IT"
    ) -> Dict[str, Any]:
        """
        ROBUST RAG Query - Uses text search and cosine similarity for matching
        Only auto-responds if similarity score is good enough (distance < 1.0)
        
        Args:
            question: The customer's question
            conversation_history: Optional conversation history (NOT USED)
           
        
        Returns:
            Dict with 'answer', 'source_documents', 'confidence', and 'can_auto_respond'
        """
        print(f"\n{'='*80}")
        print(f"  RAG QUERY STARTED")
        print(f"{'='*80}")
        print(f"Question: {question}")
       # print(f"Domain: {domain}")
        
        # Get all active knowledge documents
        from app.database import db_manager
        
        # Query without domain filter since existing documents don't have domain field
        # Or add domain="IT" as fallback if not present
        kb_docs = await db_manager.db.knowledge.find({
            "is_active": True
        }).to_list(length=None)
        
        print(f"\n[INFO] Found {len(kb_docs)} active knowledge documents")
        
        # Step 1: Vector similarity search
        print(f"\n[Step 1] Vector similarity search...")
        similar_docs = self.vector_store.similarity_search_with_score(question, k=15)
        print(f"   Found {len(similar_docs)} similar documents")
        
        # Step 2: Text search in full documents
        print(f"\n[Step 2] Text search in knowledge base...")
        question_words = set(question.lower().split())
        matching_docs = []
        
        for doc_data in kb_docs:
            # Search in title
            title_words = set(doc_data.get("title", "").lower().split())
            title_match = len(question_words & title_words)
            
            # Search in content
            content_words = set(doc_data.get("content", "").lower().split())
            content_match = len(question_words & content_words)
            
            # Search in tags
            tags_words = set()
            for tag in doc_data.get("tags", []):
                tags_words.update(tag.lower().split())
            tags_match = len(question_words & tags_words)
            
            match_score = title_match * 3 + content_match + tags_match * 2
            
            if match_score > 0:
                matching_docs.append({
                    "title": doc_data.get("title"),
                    "content": doc_data.get("content"),
                    "match_score": match_score,
                    "category": doc_data.get("category")
                })
        
        print(f"   Found {len(matching_docs)} documents with text matches")
        
        # Step 3: Combine results
        print(f"\n[Step 3] Combining search results...")
        
        # Get content from vector search results
        vector_content = []
        for doc, score in similar_docs:
            vector_content.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "similarity_score": float(score)
            })
        
        # Combine with text search results
        all_sources = vector_content + matching_docs
        
        # Step 4: Generate answer using top results
        if all_sources:
            print(f"   [OK] Found {len(all_sources)} potential sources")
            
            # Use top 5 sources for context
            top_sources = sorted(all_sources, key=lambda x: x.get('similarity_score', x.get('match_score', 0)), reverse=True)[:5]
            
            # Check if we have actual vector search results with similarity scores
            has_good_vector_match = False
            max_similarity_score = 0.0
            vector_sources = [s for s in top_sources if 'similarity_score' in s]
            
            if vector_sources:
                max_similarity_score = max(s.get('similarity_score', 0) for s in vector_sources)
                # ChromaDB uses distance scores (lower = more similar)
                # Convert to similarity: if score < 1.5, it's a decent match
                # Threshold: similarity_score < 1.0 is good, < 0.7 is excellent
                has_good_vector_match = max_similarity_score < 1.0
                print(f"   [INFO] Best similarity score (distance): {max_similarity_score:.3f}")
                print(f"   [INFO] Has good match: {has_good_vector_match} (threshold: < 1.0)")
            
            # Calculate text match quality - require STRONG match (multiple keywords)
            # match_score is calculated as: title_match * 3 + content_match + tags_match * 2
            # We want at least 2-3 keyword matches for a meaningful match
            text_sources = [s for s in top_sources if 'match_score' in s]
            strong_text_match = any(s.get('match_score', 0) >= 3 for s in text_sources)
            
            print(f"   [INFO] Text match quality check:")
            print(f"      - Sources with match scores: {len(text_sources)}")
            if text_sources:
                max_match_score = max(s.get('match_score', 0) for s in text_sources)
                print(f"      - Best match score: {max_match_score}")
                print(f"      - Has strong text match (>= 3): {strong_text_match}")
            else:
                print(f"      - No text match sources found")
            
            # Only auto-respond if we have GOOD matches (strict threshold)
            if has_good_vector_match or strong_text_match:
                context = "\n\n---\n\n".join([
                    f"Source {i+1}:\n{x.get('content', x.get('title', ''))}"
                    for i, x in enumerate(top_sources)
                ])
                
                print(f"   [OK] Generated context from top {len(top_sources)} sources")
                
                # Generate answer using LLM with context
                prompt = f"""You are a helpful IT support assistant. Answer the customer's question using ONLY the provided context.

Context:
{context}

Customer Question: {question}

Instructions:
- Use ONLY information from the context above
- Provide clear, step-by-step instructions
- If the context doesn't have relevant information, say so
- Be professional and helpful

Answer:"""

                response = self.llm.invoke(prompt)
                answer = response.content if hasattr(response, 'content') else str(response)
                
                print(f"   [OK] Generated answer (length: {len(answer)} chars)")
                
                # Calculate confidence based on actual match quality
                if has_good_vector_match:
                    # Use actual similarity score (invert distance to get similarity)
                    similarity = 1.0 / (1.0 + max_similarity_score)  # Convert distance to similarity
                    confidence = min(similarity, 0.95)  # Cap at 0.95
                    print(f"   [INFO] Using vector similarity for confidence: {confidence:.3f}")
                elif strong_text_match:
                    # Strong text match gets moderate confidence only if match_score is high
                    max_match_score = max(s.get('match_score', 0) for s in top_sources if 'match_score' in s)
                    # match_score >= 5 is very strong (5+ keywords), score it higher
                    if max_match_score >= 5:
                        confidence = 0.7
                    else:
                        confidence = 0.6  # Moderate strength
                    print(f"   [INFO] Using strong text match (score {max_match_score}) - confidence: {confidence}")
                else:
                    confidence = 0.4
                    print(f"   [INFO] Low quality match (low confidence): {confidence}")
                
                # Only auto-respond if confidence is high enough
                can_auto_respond = confidence >= 0.5
                
                print(f"\n[OK] RESULT: Found match, sending response")
                print(f"   Confidence: {confidence:.3f}")
                print(f"   Will auto-respond: {can_auto_respond}")
                
                return {
                    "answer": answer,
                    "source_documents": [
                        {
                            "content": x.get('content', str(x)),
                            "metadata": x.get('metadata', {})
                        }
                        for x in top_sources
                    ],
                    "confidence": confidence,
                    "can_auto_respond": can_auto_respond
                }
            else:
                # Found sources but they're not relevant enough
                print(f"\n[WARNING] Found sources but similarity too low for auto-response")
                if vector_sources:
                    print(f"   Best vector similarity: {max_similarity_score:.3f}")
                    print(f"   Vector threshold: < 1.0")
                if text_sources:
                    max_text_score = max(s.get('match_score', 0) for s in text_sources)
                    print(f"   Best text match score: {max_text_score}")
                    print(f"   Text threshold: >= 3")
                print(f"   → Will assign to human agent")
                return {
                    "answer": "I don't have specific information about this issue in my knowledge base. I'll escalate this to a specialized support agent who can help you better.",
                    "source_documents": [],
                    "confidence": 0.0,
                    "can_auto_respond": False
                }
        
        else:
            print(f"\n[ERROR] RESULT: No matches found")
            print(f"   Confidence: 0.0")
            print(f"   Will auto-respond: False")
            
            return {
                "answer": "I don't have specific information about this issue in my knowledge base. I'll escalate this to a specialized support agent who can help you better.",
                "source_documents": [],
                "confidence": 0.0,
                "can_auto_respond": False
            }
    
    def _calculate_confidence(self, source_documents: List) -> float:
        """Calculate confidence score based on retrieved documents"""
        if not source_documents:
            print("   [INFO] No documents retrieved - confidence: 0.0")
            return 0.0
        
        print(f"   [INFO] Calculating confidence from {len(source_documents)} documents")
        
        # IMPROVED: Use similarity scores if available, fallback to count-based
        # ChromaDB returns documents with scores in metadata
        total_score = 0.0
        scored_docs = 0
        
        for i, doc in enumerate(source_documents):
            # Check if document has similarity score in metadata
            if hasattr(doc, 'metadata') and doc.metadata:
                # ChromaDB may store score differently depending on version
                score = doc.metadata.get('score', None) or doc.metadata.get('similarity', None)
                if score is not None:
                    total_score += float(score)
                    scored_docs += 1
                    print(f"      Doc {i+1} has score: {score}")
                else:
                    print(f"      Doc {i+1} has no score in metadata")
        
        # If we have similarity scores, use average score
        if scored_docs > 0:
            avg_score = total_score / scored_docs
            # Normalize to 0-1 range (assuming scores are between 0-1)
            # Higher score = better match
            confidence = min(avg_score, 1.0)
            print(f"   [OK] Using similarity scores - avg: {avg_score:.3f}, confidence: {confidence:.3f}")
        else:
            # Fallback to count-based with improved threshold
            # Base confidence starts at 0.5 for even a single document
            # This ensures we respond even with minimal context
            base_confidence = 0.5 + (len(source_documents) - 1) * 0.1
            confidence = min(base_confidence, 0.85)
            print(f"   [OK] Using count-based - docs: {len(source_documents)}, base: {base_confidence:.3f}, final: {confidence:.3f}")
        
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

