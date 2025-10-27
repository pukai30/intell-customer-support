# RAG Vector Store Synchronization

## Overview

The RAG system now maintains automatic synchronization between MongoDB knowledge documents and the ChromaDB vector store. When documents are added, updated, or deleted, the vector store is updated accordingly to ensure RAG queries always use the latest information.

## Synchronization Functions

### 1. Add Documents (`add_documents_to_knowledge_base`)

**Purpose**: Adds new documents to both MongoDB and the vector store.

**Process**:
1. Splits content into chunks (1000 chars, 200 char overlap)
2. Creates embeddings and adds chunks to ChromaDB vector store
3. Stores document metadata in MongoDB with chunk IDs
4. Attempts to persist vector store (handles version differences)

**Logging**: 
- `[RAG] Vector store persisted after adding documents`

**Location**: Lines 62-150 in `app/rag_system.py`

---

### 2. Update Documents (`update_document_in_knowledge_base`)

**Purpose**: Updates existing documents in both MongoDB and vector store.

**Process**:
1. Retrieves existing document from MongoDB
2. **If content changes**:
   - Deletes all old chunks from vector store
   - Creates new chunks with updated content
   - Adds new chunks to vector store
   - Updates chunk IDs in MongoDB
3. **If only metadata changes** (title, category, tags):
   - Updates MongoDB only (no vector store changes)
4. Attempts to persist vector store

**Logging**:
- `[RAG] Updating document: {title}`
- `[RAG] Content changed, updating vector store...`
- `[RAG] Deleting old {count} chunks...`
- `[RAG] Created {count} new chunks`
- `[RAG] Added {count} new chunks to vector store`
- `[RAG] Vector store persisted`
- `[RAG] Successfully updated document {doc_id}`

**Location**: Lines 152-235 in `app/rag_system.py`

---

### 3. Delete Documents (`delete_document_from_knowledge_base`)

**Purpose**: Removes documents from both MongoDB and vector store.

**Process**:
1. Retrieves document from MongoDB
2. Deletes all chunks from vector store using chunk IDs
3. Deletes document from MongoDB (soft or hard delete based on parameter)
4. Attempts to persist vector store

**Parameters**:
- `hard_delete`: If `True`, permanently deletes. If `False`, soft deletes (sets `is_active=False`)

**Logging**:
- `[RAG] Deleting document: {title}`
- `[RAG] Deleting {count} chunks from vector store...`
- `[RAG] Deleting from MongoDB ({type} delete)...`
- `[RAG] Deleted {count}/{total} chunks from vector store`
- `[RAG] Vector store persisted`
- `[RAG] Successfully deleted document {doc_id}`

**Location**: Lines 237-282 in `app/rag_system.py`

---

### 4. Helper Function (`_delete_document_chunks`)

**Purpose**: Utility to delete chunks from vector store by chunk IDs.

**Process**:
1. Iterates through chunk IDs
2. Deletes each chunk from ChromaDB using metadata filter
3. Logs progress and errors

**Logging**:
- `[RAG] No chunks to delete`
- `[RAG] Warning: Could not delete chunk {chunk_id}: {error}`
- `[RAG] Deleted {count}/{total} chunks from vector store`
- `[RAG] Error deleting chunks from vector store: {error}`

**Location**: Lines 284-306 in `app/rag_system.py`

---

## Key Features

### 1. Automatic Sync
- Vector store is automatically updated whenever MongoDB documents change
- No manual synchronization required

### 2. Chunk-Level Updates
- Updates individual chunks rather than entire documents
- More efficient for large documents
- Preserves vector store structure

### 3. Version Compatibility
- Handles different ChromaDB versions gracefully
- Checks for `persist()` method before calling
- Modern ChromaDB versions persist automatically

### 4. Error Handling
- Comprehensive try-catch blocks
- Detailed logging for debugging
- Traceback printing on errors
- Continues even if some chunks fail to delete

### 5. Soft Delete Support
- Can mark documents as inactive without deleting
- Option to permanently delete from both stores

---

## Usage Examples

### Adding a Document

```python
from app.rag_system import rag_system

doc_ids = await rag_system.add_documents_to_knowledge_base(
    documents=[{
        "title": "New IT Guide",
        "content": "How to reset password...",
        "tags": ["password", "security"]
    }],
    category="security",
    is_temporary=False,
    created_by="admin"
)
```

### Updating a Document

```python
success = await rag_system.update_document_in_knowledge_base(
    doc_id="document_id_here",
    title="Updated Title",
    content="Updated content...",
    category="hardware",
    tags=["new", "tags"]
)
```

### Deleting a Document

```python
# Soft delete (marks as inactive)
success = await rag_system.delete_document_from_knowledge_base(
    doc_id="document_id_here",
    hard_delete=False
)

# Hard delete (permanently removes)
success = await rag_system.delete_document_from_knowledge_base(
    doc_id="document_id_here",
    hard_delete=True
)
```

---

## Benefits

1. **Always Fresh**: RAG queries always use the latest knowledge
2. **Consistent**: MongoDB and vector store stay in sync
3. **Efficient**: Only updates what changed
4. **Transparent**: Detailed logging shows what's happening
5. **Robust**: Error handling ensures reliability

---

## API Integration

These functions are automatically called by the FastAPI endpoints in `app/api.py`:

- `POST /api/knowledge/add` → `add_documents_to_knowledge_base()`
- `PUT /api/knowledge/{doc_id}` → `update_document_in_knowledge_base()`
- `DELETE /api/knowledge/{doc_id}` → `delete_document_from_knowledge_base()`

No additional work needed - the APIs handle synchronization automatically!

---

## Notes

- ChromaDB persists to `./vector_store/` directory by default
- Vector store must be initialized before using these functions (`await rag_system.initialize()`)
- Chunk size (1000) and overlap (200) can be adjusted in the functions
- All functions return boolean indicating success/failure

