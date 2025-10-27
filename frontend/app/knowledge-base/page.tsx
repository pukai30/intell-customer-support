'use client'

import { useState, useEffect } from 'react'
import { knowledgeAPI } from '@/lib/api'
import { format } from 'date-fns'
import UploadModal from '@/components/UploadModal'
import EditModal from '@/components/EditModal'
import CreateModal from '@/components/CreateModal'

interface KnowledgeDocument {
  id: string
  title: string
  category: string
  tags?: string[]
  file_name?: string
  file_type?: string
  is_active: boolean
  is_temporary: boolean
  expires_at?: string
  created_by?: string
  created_at: string
  updated_at: string
  content_preview: string
  is_embedded?: boolean
  chunk_count?: number
}

export default function KnowledgeBasePage() {
  const [documents, setDocuments] = useState<KnowledgeDocument[]>([])
  const [loading, setLoading] = useState(true)
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false)
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [editingDocument, setEditingDocument] = useState<KnowledgeDocument | null>(null)
  const [filterCategory, setFilterCategory] = useState('')
  const [categories, setCategories] = useState<string[]>([])

  useEffect(() => {
    loadDocuments()
    loadCategories()
  }, [filterCategory])

  const loadDocuments = async () => {
    try {
      setLoading(true)
      const params = filterCategory ? { category: filterCategory } : {}
      const response = await knowledgeAPI.list(params)
      setDocuments(response.documents || [])
    } catch (error) {
      console.error('Error loading documents:', error)
      alert('Failed to load knowledge base')
    } finally {
      setLoading(false)
    }
  }

  const loadCategories = async () => {
    try {
      const response = await knowledgeAPI.categories()
      setCategories(response.categories?.map((c: any) => c.name) || [])
    } catch (error) {
      console.error('Error loading categories:', error)
    }
  }

  const handleDelete = async (id: string, title: string) => {
    if (!confirm(`Are you sure you want to delete "${title}"?`)) return

    try {
      await knowledgeAPI.delete(id, false) // Soft delete
      alert('Document deleted successfully')
      loadDocuments()
    } catch (error) {
      console.error('Error deleting document:', error)
      alert('Failed to delete document')
    }
  }

  const handleReEmbed = async (id: string, title: string) => {
    if (!confirm(`Re-embed "${title}" in vector store?`)) return

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/knowledge/${id}/re-embed`, {
        method: 'POST'
      })
      const result = await response.json()
      
      if (result.status === 'success') {
        alert(`Document re-embedded successfully! ${result.chunks_created} chunks created.`)
        loadDocuments()
      } else {
        alert('Failed to re-embed document')
      }
    } catch (error) {
      console.error('Error re-embedding document:', error)
      alert('Failed to re-embed document')
    }
  }

  const handleBatchReEmbed = async () => {
    if (!confirm('Re-embed all documents in vector store? This may take a while.')) return

    try {
      const docIds = documents.map(doc => doc.id)
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/knowledge/batch-re-embed`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(docIds)
      })
      const result = await response.json()
      
      if (result.status === 'success') {
        alert(`Batch re-embed complete: ${result.success}/${result.total} documents successful`)
        loadDocuments()
      } else {
        alert('Failed to batch re-embed documents')
      }
    } catch (error) {
      console.error('Error batch re-embedding:', error)
      alert('Failed to batch re-embed documents')
    }
  }

  const handleUploadSuccess = () => {
    setIsUploadModalOpen(false)
    loadDocuments()
    loadCategories()
  }

  const handleCreateSuccess = () => {
    setIsCreateModalOpen(false)
    loadDocuments()
    loadCategories()
  }

  const handleEditSuccess = () => {
    setEditingDocument(null)
    loadDocuments()
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Knowledge Base Management</h1>
          <p className="text-gray-600 mt-1">Manage your knowledge documents and files</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-medium transition-colors flex items-center gap-2"
          >
            <span>➕</span> Create Knowledge
          </button>
          <button
            onClick={() => setIsUploadModalOpen(true)}
            className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-2 rounded-lg font-medium transition-colors flex items-center gap-2"
          >
            <span>📤</span> Upload File
          </button>
          <button
            onClick={handleBatchReEmbed}
            className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg font-medium transition-colors flex items-center gap-2"
          >
            <span>🔄</span> Re-embed All
          </button>
        </div>
      </div>

      {/* Filter */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex items-center gap-4">
          <label className="text-sm font-medium text-gray-700">Filter by Category:</label>
          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">All Categories</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
          <button
            onClick={loadDocuments}
            className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-md transition-colors"
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-gray-500">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4">Loading knowledge base...</p>
          </div>
        ) : !documents || documents.length === 0 ? (
          <div className="p-12 text-center text-gray-500">
            <p className="text-lg">No knowledge documents found</p>
            <p className="text-sm mt-2">Upload a file or create new knowledge to get started</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Title
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Category
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Tags
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Created
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Vector Store
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {documents.map((doc) => (
                  <tr key={doc.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-gray-900">{doc.title}</div>
                      <div className="text-sm text-gray-500 truncate max-w-md">{doc.content_preview}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                        {doc.category}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-wrap gap-1">
                        {doc.tags && doc.tags.slice(0, 3).map((tag, idx) => (
                          <span key={idx} className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded">
                            {tag}
                          </span>
                        ))}
                        {doc.tags && doc.tags.length > 3 && (
                          <span className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded">
                            +{doc.tags.length - 3}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {doc.file_type ? (
                        <span className="flex items-center gap-1">
                          📄 {doc.file_type.toUpperCase()}
                        </span>
                      ) : (
                        <span>Manual</span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div>{format(new Date(doc.created_at), 'MMM d, yyyy')}</div>
                      <div className="text-xs text-gray-400">{format(new Date(doc.created_at), 'HH:mm')}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {doc.is_embedded ? (
                        <div className="flex flex-col gap-1">
                          <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                            ✓ Embedded
                          </span>
                          {doc.chunk_count && (
                            <span className="text-xs text-gray-500">{doc.chunk_count} chunks</span>
                          )}
                        </div>
                      ) : (
                        <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                          Not Embedded
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {doc.is_temporary ? (
                        <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                          Temporary
                        </span>
                      ) : doc.is_active ? (
                        <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                          Active
                        </span>
                      ) : (
                        <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                          Inactive
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleReEmbed(doc.id, doc.title)}
                          className="text-purple-600 hover:text-purple-900 bg-purple-50 hover:bg-purple-100 px-3 py-1 rounded-md transition-colors"
                          title="Re-embed in vector store"
                        >
                          🔄 Re-embed
                        </button>
                        <button
                          onClick={() => setEditingDocument(doc)}
                          className="text-primary-600 hover:text-primary-900 bg-blue-50 hover:bg-blue-100 px-3 py-1 rounded-md transition-colors"
                        >
                          ✏️ Edit
                        </button>
                        <button
                          onClick={() => handleDelete(doc.id, doc.title)}
                          className="text-red-600 hover:text-red-900 bg-red-50 hover:bg-red-100 px-3 py-1 rounded-md transition-colors"
                        >
                          🗑️ Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-sm text-gray-500">Total Documents</div>
          <div className="text-2xl font-bold text-gray-900">{documents?.length || 0}</div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-sm text-gray-500">Active</div>
          <div className="text-2xl font-bold text-green-600">
            {documents?.filter(d => d.is_active).length || 0}
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-sm text-gray-500">Temporary</div>
          <div className="text-2xl font-bold text-yellow-600">
            {documents?.filter(d => d.is_temporary).length || 0}
          </div>
        </div>
      </div>

      {/* Modals */}
      <UploadModal
        isOpen={isUploadModalOpen}
        onClose={() => setIsUploadModalOpen(false)}
        onSuccess={handleUploadSuccess}
      />

      <CreateModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSuccess={handleCreateSuccess}
      />

      {editingDocument && (
        <EditModal
          document={editingDocument}
          onClose={() => setEditingDocument(null)}
          onSuccess={handleEditSuccess}
        />
      )}
    </div>
  )
}

