# Automatic Embedding Feature

## What's New?

### 🎉 Automatic Embedding
All knowledge documents are now **automatically embedded** in the vector store when created or uploaded!

### 📊 Embedding Status in UI
- Visual indicators show which documents are embedded
- Displays chunk count for each document
- Easy to see which documents are query-ready

### 🔄 Manual Re-embedding
- Click "Re-embed" on any document to update embeddings
- "Re-embed All" button to process entire knowledge base
- Useful for updating embeddings after configuration changes

## How It Works

### When You Create/Upload Knowledge:
1. ✅ Content is **automatically split into chunks**
2. ✅ **Automatically embedded** in configured vector store
3. ✅ **Automatically indexed** for RAG queries
4. ✅ Status shows "✓ Embedded" with chunk count

### Vector Store Configuration:
- Configure in: Settings → Vector DB Tab
- Choose: Chroma, Pinecone, Weaviate, or FAISS
- Embeddings respect these settings

## Usage

### To View Embedding Status:
1. Go to **Knowledge Base** page
2. Look at **"Vector Store"** column
3. **Green badge** = Embedded ✓
4. **Red badge** = Not Embedded

### To Re-embed a Document:
1. Click **🔄 Re-embed** button next to document
2. Confirms and processes
3. Updates status automatically

### To Re-embed All Documents:
1. Click **🔄 Re-embed All** in header
2. Processes all documents
3. Shows success/failure summary

## Benefits

✅ **Fully Automatic** - No manual steps required
✅ **Immediate Availability** - Documents ready for queries instantly
✅ **Transparent Status** - Always know what's embedded
✅ **Easy Recovery** - Re-embed anytime if needed
✅ **Batch Processing** - Handle large knowledge bases efficiently

## API Endpoints

**Single Re-embed:**
```bash
POST /api/knowledge/{doc_id}/re-embed
```

**Batch Re-embed:**
```bash
POST /api/knowledge/batch-re-embed
Body: ["doc_id1", "doc_id2", ...]
```

## Technical Details

- **Chunk Size**: 1000 characters
- **Overlap**: 200 characters
- **Embedding Model**: Configured in Settings
- **Vector Store**: Configured in Settings
- **Metadata**: Title, category, tags stored with chunks

