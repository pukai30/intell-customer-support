'use client'

import { useState } from 'react'
import { knowledgeAPI } from '@/lib/api'

interface CreateModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
}

export default function CreateModal({ isOpen, onClose, onSuccess }: CreateModalProps) {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [category, setCategory] = useState('general')
  const [tags, setTags] = useState('')
  const [isTemporary, setIsTemporary] = useState(false)
  const [expiresInDays, setExpiresInDays] = useState(30)
  const [createdBy, setCreatedBy] = useState('')
  const [creating, setCreating] = useState(false)

  if (!isOpen) return null

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      setCreating(true)
      const tagArray = tags.split(',').map(t => t.trim()).filter(t => t)
      
      await knowledgeAPI.create({
        title,
        content,
        category,
        tags: tagArray,
        is_temporary: isTemporary,
        expires_in_days: isTemporary ? expiresInDays : undefined,
        created_by: createdBy || undefined,
      })

      alert('Knowledge created successfully!')
      onSuccess()
      resetForm()
    } catch (error) {
      console.error('Error creating knowledge:', error)
      alert('Failed to create knowledge')
    } finally {
      setCreating(false)
    }
  }

  const resetForm = () => {
    setTitle('')
    setContent('')
    setCategory('general')
    setTags('')
    setIsTemporary(false)
    setExpiresInDays(30)
    setCreatedBy('')
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Create Knowledge Document</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Title *
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="e.g., How to Reset Password"
              required
            />
          </div>

          {/* Content */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Content *
            </label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={12}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Enter the knowledge content here..."
              required
            />
            <p className="mt-1 text-sm text-gray-500">
              {content.length} characters
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            {/* Category */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Category *
              </label>
              <input
                type="text"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="e.g., security, hardware"
                required
              />
            </div>

            {/* Tags */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tags (comma-separated)
              </label>
              <input
                type="text"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="e.g., password, reset, account"
              />
            </div>
          </div>

          {/* Temporary Knowledge */}
          <div className="flex items-center">
            <input
              type="checkbox"
              id="createIsTemporary"
              checked={isTemporary}
              onChange={(e) => setIsTemporary(e.target.checked)}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <label htmlFor="createIsTemporary" className="ml-2 block text-sm text-gray-900">
              Temporary knowledge (auto-expires)
            </label>
          </div>

          {isTemporary && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Expires in (days)
              </label>
              <input
                type="number"
                value={expiresInDays}
                onChange={(e) => setExpiresInDays(parseInt(e.target.value))}
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                min="1"
                max="365"
              />
            </div>
          )}

          {/* Created By */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Created By (optional)
            </label>
            <input
              type="text"
              value={createdBy}
              onChange={(e) => setCreatedBy(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="e.g., admin@company.com"
            />
          </div>

          {/* Buttons */}
          <div className="flex justify-end gap-3 mt-6">
            <button
              type="button"
              onClick={() => { resetForm(); onClose(); }}
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              disabled={creating}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
              disabled={creating}
            >
              {creating ? 'Creating...' : 'Create Knowledge'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

