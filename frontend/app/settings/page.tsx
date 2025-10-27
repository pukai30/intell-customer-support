'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Configuration interfaces
interface EmailConfig {
  support_email: string
  email_host: string
  email_port: number
  email_user: string | null
  email_password: string | null
  use_tls: boolean
  use_ssl: boolean
}

interface WhatsAppConfig {
  enabled: boolean
  whatsapp_number: string
  twilio_account_sid: string | null
  twilio_auth_token: string | null
  twilio_phone_number: string | null
}

interface SMSConfig {
  enabled: boolean
  sms_phone_number: string | null
  twilio_account_sid: string | null
  twilio_auth_token: string | null
  twilio_phone_number: string | null
}

interface ModelConfig {
  llm_provider: string
  llm_model: string
  llm_api_key: string | null
  llm_base_url: string | null
  llm_temperature: number
  llm_max_tokens: number
  embedding_provider: string
  embedding_model: string
  embedding_api_key: string | null
  embedding_base_url: string | null
  embedding_dimensions: number
}

interface VectorDBConfig {
  provider: string
  enabled: boolean
  chroma_host: string
  chroma_port: number
  chroma_collection_name: string
  chroma_persist_directory: string | null
  pinecone_api_key: string | null
  pinecone_environment: string | null
  pinecone_index_name: string
  pinecone_namespace: string | null
  weaviate_url: string
  weaviate_api_key: string | null
  weaviate_class_name: string
  faiss_index_path: string
  faiss_index_type: string
}

interface KnowledgeProviderConfig {
  provider: string
  enabled: boolean
  aws_access_key_id: string | null
  aws_secret_access_key: string | null
  aws_region: string
  aws_bucket_name: string | null
  aws_prefix: string
  azure_account_name: string | null
  azure_account_key: string | null
  azure_container_name: string | null
  azure_connection_string: string | null
  google_credentials_file: string | null
  google_folder_id: string | null
  google_service_account_email: string | null
  dropbox_access_token: string | null
  dropbox_folder_path: string
}

interface EnhancedConfig {
  email: EmailConfig
  whatsapp: WhatsAppConfig
  sms: SMSConfig
  model: ModelConfig
  vector_db: VectorDBConfig
  knowledge_provider: KnowledgeProviderConfig
  chat_enabled: boolean
  auto_assignment_enabled: boolean
  escalation_enabled: boolean
  notification_enabled: boolean
}

export default function EnhancedSettingsPage() {
  const [activeTab, setActiveTab] = useState('email')
  const [config, setConfig] = useState<EnhancedConfig | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)
  const [editMode, setEditMode] = useState<Record<string, boolean>>({
    email: false,
    whatsapp: false,
    sms: false,
    model: false,
    vector_db: false,
    knowledge_provider: false
  })
  const [originalConfig, setOriginalConfig] = useState<EnhancedConfig | null>(null)

  const tabs = [
    { id: 'email', label: 'Email', icon: '📧' },
    { id: 'whatsapp', label: 'WhatsApp', icon: '📱' },
    { id: 'sms', label: 'SMS', icon: '💬' },
    { id: 'model', label: 'AI Model', icon: '🤖' },
    { id: 'knowledge_provider', label: 'Knowledge Provider', icon: '📚' },
    { id: 'vector_db', label: 'Vector DB', icon: '🗄️' }
  ]

  useEffect(() => {
    loadConfig()
  }, [])

  const loadConfig = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_URL}/api/config/enhanced`)
      setConfig(response.data)
      setOriginalConfig(response.data) // Store original for cancel
    } catch (error: any) {
      console.error('Error loading config:', error)
      setMessage({ 
        type: 'error', 
        text: `Failed to load configuration: ${error.response?.data?.detail || error.message}` 
      })
      // Set default config on error
      const defaultConfig = {
        email: { support_email: 'r15528850@gmail.com', email_host: 'smtp.gmail.com', email_port: 587, email_user: null, email_password: null, use_tls: true, use_ssl: false },
        whatsapp: { enabled: false, whatsapp_number: 'whatsapp:+14155238886', twilio_account_sid: null, twilio_auth_token: null, twilio_phone_number: null },
        sms: { enabled: false, sms_phone_number: null, twilio_account_sid: null, twilio_auth_token: null, twilio_phone_number: null },
        model: { llm_provider: 'openai', llm_model: 'gpt-3.5-turbo', llm_api_key: null, llm_base_url: null, llm_temperature: 0.7, llm_max_tokens: 2000, embedding_provider: 'openai', embedding_model: 'text-embedding-ada-002', embedding_api_key: null, embedding_base_url: null, embedding_dimensions: 1536 },
        vector_db: { provider: 'chroma', enabled: true, chroma_host: 'localhost', chroma_port: 8000, chroma_collection_name: 'knowledge_base', chroma_persist_directory: null, pinecone_api_key: null, pinecone_environment: null, pinecone_index_name: 'knowledge-base', pinecone_namespace: null, weaviate_url: 'http://localhost:8080', weaviate_api_key: null, weaviate_class_name: 'KnowledgeDocument', faiss_index_path: './vector_store/faiss_index', faiss_index_type: 'Flat' },
        knowledge_provider: { provider: 'local', enabled: true, aws_access_key_id: null, aws_secret_access_key: null, aws_region: 'us-east-1', aws_bucket_name: null, aws_prefix: 'knowledge-base/', azure_account_name: null, azure_account_key: null, azure_container_name: null, azure_connection_string: null, google_credentials_file: null, google_folder_id: null, google_service_account_email: null, dropbox_access_token: null, dropbox_folder_path: '/knowledge-base' },
        chat_enabled: true,
        auto_assignment_enabled: true,
        escalation_enabled: true,
        notification_enabled: true
      }
      setConfig(defaultConfig as EnhancedConfig)
      setOriginalConfig(defaultConfig as EnhancedConfig)
    } finally {
      setLoading(false)
    }
  }

  const handleEdit = (section: string) => {
    setEditMode({ ...editMode, [section]: true })
  }

  const handleCancel = (section: string) => {
    if (originalConfig) {
      setConfig(originalConfig)
    }
    setEditMode({ ...editMode, [section]: false })
    setMessage(null)
  }

  const handleSaveComplete = (section: string) => {
    setEditMode({ ...editMode, [section]: false })
    loadConfig() // Reload to get updated config
  }

  const saveConfig = async (section: string, sectionConfig: any) => {
    try {
      setSaving(true)
      setMessage(null)
      
      await axios.put(`${API_URL}/api/config/${section}`, sectionConfig)
      
      setMessage({ type: 'success', text: `${section.charAt(0).toUpperCase() + section.slice(1)} configuration saved successfully!` })
      
      // Reload config to show updated values
      setTimeout(async () => {
        await loadConfig()
        setMessage(null)
      }, 2000)
      
    } catch (error: any) {
      console.error('Error saving config:', error)
      setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to save configuration' })
    } finally {
      setSaving(false)
    }
  }

  const handleEmailSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!config) return
    await saveConfig('email', config.email)
    handleSaveComplete('email')
  }

  const handleWhatsAppSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!config) return
    await saveConfig('whatsapp', config.whatsapp)
    handleSaveComplete('whatsapp')
  }

  const handleSMSSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!config) return
    await saveConfig('sms', config.sms)
    handleSaveComplete('sms')
  }

  const handleModelSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!config) return
    await saveConfig('model', config.model)
    handleSaveComplete('model')
  }

  const handleVectorDBSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!config) return
    await saveConfig('vector-db', config.vector_db)
    handleSaveComplete('vector_db')
  }

  const handleKnowledgeProviderSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!config) return
    await saveConfig('knowledge-provider', config.knowledge_provider)
    handleSaveComplete('knowledge_provider')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading configuration...</p>
        </div>
      </div>
    )
  }

  if (!config) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="text-center py-12">
          <p className="text-gray-600">Failed to load configuration</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 p-4 md:p-8">
      <div className="container mx-auto max-w-7xl">
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-2xl border border-slate-200/50 overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 px-6 py-6">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center shadow-lg">
                <span className="text-3xl">⚙️</span>
              </div>
              <div>
                <h1 className="text-3xl font-extrabold text-white">System Configuration</h1>
                <p className="text-blue-100 mt-1">Configure support channels, AI models, and integrations</p>
              </div>
            </div>
          </div>

          {message && (
            <div className={`mx-6 mt-6 p-4 rounded-xl shadow-lg border-l-4 ${
              message.type === 'success' 
                ? 'bg-gradient-to-r from-green-50 to-emerald-50 text-green-800 border-green-500' 
                : 'bg-gradient-to-r from-red-50 to-rose-50 text-red-800 border-red-500'
            }`}>
              <div className="flex items-center gap-2">
                <span className="text-xl">{message.type === 'success' ? '✅' : '❌'}</span>
                <span className="font-semibold">{message.text}</span>
              </div>
            </div>
          )}

          {/* Tab Navigation */}
          <div className="border-b border-slate-200 bg-slate-50/50">
            <nav className="flex space-x-2 px-6 overflow-x-auto">
              {tabs.map((tab) => {
                const colors = {
                  'email': { active: 'bg-blue-600 text-white', inactive: 'text-slate-600 hover:bg-slate-200' },
                  'whatsapp': { active: 'bg-green-600 text-white', inactive: 'text-slate-600 hover:bg-slate-200' },
                  'sms': { active: 'bg-purple-600 text-white', inactive: 'text-slate-600 hover:bg-slate-200' },
                  'model': { active: 'bg-pink-600 text-white', inactive: 'text-slate-600 hover:bg-slate-200' },
                  'knowledge_provider': { active: 'bg-indigo-600 text-white', inactive: 'text-slate-600 hover:bg-slate-200' },
                  'vector_db': { active: 'bg-orange-600 text-white', inactive: 'text-slate-600 hover:bg-slate-200' }
                }[tab.id] || { active: 'bg-primary-600 text-white', inactive: 'text-slate-600 hover:bg-slate-200' }
                
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-2 py-4 px-4 rounded-t-lg font-semibold text-sm transition-all whitespace-nowrap ${
                      activeTab === tab.id ? colors.active : colors.inactive
                    }`}
                  >
                    <span className="text-lg">{tab.icon}</span>
                    <span>{tab.label}</span>
                  </button>
                )
              })}
            </nav>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {/* Email Tab */}
            {activeTab === 'email' && (
              <form onSubmit={handleEmailSubmit}>
                <div className="space-y-6">
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center text-2xl shadow-lg">
                        📧
                      </div>
                      <h2 className="text-2xl font-bold text-gray-900">Email Configuration</h2>
                    </div>
                    {!editMode.email ? (
                      <button
                        type="button"
                        onClick={() => handleEdit('email')}
                        className="px-6 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all shadow-lg hover:shadow-xl font-semibold flex items-center gap-2"
                      >
                        <span>✏️</span>
                        Edit
                      </button>
                    ) : (
                      <div className="flex gap-2">
                        <button
                          type="button"
                          onClick={() => handleCancel('email')}
                          className="px-6 py-2 bg-slate-600 text-white rounded-xl hover:bg-slate-700 transition-all shadow-lg font-semibold"
                        >
                          Cancel
                        </button>
                      </div>
                    )}
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Support Email *
                      </label>
                      <input
                        type="email"
                        value={config.email.support_email}
                        onChange={(e) => setConfig({
                          ...config,
                          email: { ...config.email, support_email: e.target.value }
                        })}
                        disabled={!editMode.email}
                        className={`w-full px-4 py-3 border-2 rounded-xl shadow-sm transition-all ${
                          editMode.email 
                            ? 'border-slate-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 bg-white' 
                            : 'border-slate-200 bg-slate-50 cursor-not-allowed'
                        }`}
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Email Host
                      </label>
                      <input
                        type="text"
                        value={config.email.email_host}
                        onChange={(e) => setConfig({
                          ...config,
                          email: { ...config.email, email_host: e.target.value }
                        })}
                        disabled={!editMode.email}
                        className={`w-full px-3 py-2 border rounded-lg ${
                          editMode.email ? 'border-gray-300 bg-white' : 'border-slate-200 bg-slate-50 cursor-not-allowed'
                        }`}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Email Port
                      </label>
                      <input
                        type="number"
                        value={config.email.email_port}
                        onChange={(e) => setConfig({
                          ...config,
                          email: { ...config.email, email_port: parseInt(e.target.value) }
                        })}
                        disabled={!editMode.email}
                        className={`w-full px-3 py-2 border rounded-lg ${
                          editMode.email ? 'border-gray-300 bg-white' : 'border-slate-200 bg-slate-50 cursor-not-allowed'
                        }`}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Email User
                      </label>
                      <input
                        type="text"
                        value={config.email.email_user || ''}
                        onChange={(e) => setConfig({
                          ...config,
                          email: { ...config.email, email_user: e.target.value }
                        })}
                        disabled={!editMode.email}
                        className={`w-full px-3 py-2 border rounded-lg ${
                          editMode.email ? 'border-gray-300 bg-white' : 'border-slate-200 bg-slate-50 cursor-not-allowed'
                        }`}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Email Password
                      </label>
                      <input
                        type="password"
                        value={config.email.email_password || ''}
                        onChange={(e) => setConfig({
                          ...config,
                          email: { ...config.email, email_password: e.target.value }
                        })}
                        disabled={!editMode.email}
                        className={`w-full px-3 py-2 border rounded-lg ${
                          editMode.email ? 'border-gray-300 bg-white' : 'border-slate-200 bg-slate-50 cursor-not-allowed'
                        }`}
                      />
                    </div>
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        checked={config.email.use_tls}
                        onChange={(e) => setConfig({
                          ...config,
                          email: { ...config.email, use_tls: e.target.checked }
                        })}
                        disabled={!editMode.email}
                        className={`mr-2 ${!editMode.email ? 'cursor-not-allowed' : ''}`}
                      />
                      <label className="text-sm font-medium text-gray-700">Use TLS</label>
                    </div>
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        checked={config.email.use_ssl}
                        onChange={(e) => setConfig({
                          ...config,
                          email: { ...config.email, use_ssl: e.target.checked }
                        })}
                        disabled={!editMode.email}
                        className={`mr-2 ${!editMode.email ? 'cursor-not-allowed' : ''}`}
                      />
                      <label className="text-sm font-medium text-gray-700">Use SSL</label>
                    </div>
                  </div>
                  {editMode.email && (
                    <div className="flex justify-end pt-4 gap-3">
                      <button
                        type="button"
                        onClick={() => handleCancel('email')}
                        className="px-8 py-3 bg-slate-500 text-white rounded-xl shadow-lg hover:bg-slate-600 transition-all font-semibold text-base"
                      >
                        Cancel
                      </button>
                      <button
                        type="submit"
                        disabled={saving}
                        className="px-8 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl shadow-lg hover:shadow-xl hover:from-blue-700 hover:to-indigo-700 transition-all disabled:opacity-50 font-semibold text-base"
                      >
                        {saving ? '💾 Saving...' : '💾 Save Changes'}
                      </button>
                    </div>
                  )}
                </div>
              </form>
            )}

            {/* WhatsApp Tab */}
            {activeTab === 'whatsapp' && (
              <form onSubmit={handleWhatsAppSubmit}>
                <div className="space-y-6">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center text-2xl shadow-lg">
                      📱
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900">WhatsApp Configuration</h2>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="flex items-center md:col-span-2">
                      <input
                        type="checkbox"
                        checked={config.whatsapp.enabled}
                        onChange={(e) => setConfig({
                          ...config,
                          whatsapp: { ...config.whatsapp, enabled: e.target.checked }
                        })}
                        className="mr-2"
                      />
                      <label className="text-sm font-medium text-gray-700">Enable WhatsApp Support</label>
                    </div>
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        WhatsApp Number
                      </label>
                      <input
                        type="text"
                        value={config.whatsapp.whatsapp_number}
                        onChange={(e) => setConfig({
                          ...config,
                          whatsapp: { ...config.whatsapp, whatsapp_number: e.target.value }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        placeholder="whatsapp:+14155238886"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Twilio Account SID
                      </label>
                      <input
                        type="text"
                        value={config.whatsapp.twilio_account_sid || ''}
                        onChange={(e) => setConfig({
                          ...config,
                          whatsapp: { ...config.whatsapp, twilio_account_sid: e.target.value }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Twilio Auth Token
                      </label>
                      <input
                        type="password"
                        value={config.whatsapp.twilio_auth_token || ''}
                        onChange={(e) => setConfig({
                          ...config,
                          whatsapp: { ...config.whatsapp, twilio_auth_token: e.target.value }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Twilio Phone Number
                      </label>
                      <input
                        type="text"
                        value={config.whatsapp.twilio_phone_number || ''}
                        onChange={(e) => setConfig({
                          ...config,
                          whatsapp: { ...config.whatsapp, twilio_phone_number: e.target.value }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        placeholder="+1234567890"
                      />
                    </div>
                  </div>
                  <div className="flex justify-end pt-4">
                    <button
                      type="submit"
                      disabled={saving}
                      className="px-8 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl shadow-lg hover:shadow-xl hover:from-green-700 hover:to-emerald-700 transition-all disabled:opacity-50 font-semibold text-base"
                    >
                      {saving ? '💾 Saving...' : '💾 Save WhatsApp Config'}
                    </button>
                  </div>
                </div>
              </form>
            )}

            {/* SMS Tab */}
            {activeTab === 'sms' && (
              <form onSubmit={handleSMSSubmit}>
                <div className="space-y-6">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-violet-600 rounded-xl flex items-center justify-center text-2xl shadow-lg">
                      💬
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900">SMS Configuration</h2>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="flex items-center md:col-span-2">
                      <input
                        type="checkbox"
                        checked={config.sms.enabled}
                        onChange={(e) => setConfig({
                          ...config,
                          sms: { ...config.sms, enabled: e.target.checked }
                        })}
                        className="mr-2"
                      />
                      <label className="text-sm font-medium text-gray-700">Enable SMS Support</label>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        SMS Phone Number
                      </label>
                      <input
                        type="text"
                        value={config.sms.sms_phone_number || ''}
                        onChange={(e) => setConfig({
                          ...config,
                          sms: { ...config.sms, sms_phone_number: e.target.value }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        placeholder="+1234567890"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Twilio Account SID
                      </label>
                      <input
                        type="text"
                        value={config.sms.twilio_account_sid || ''}
                        onChange={(e) => setConfig({
                          ...config,
                          sms: { ...config.sms, twilio_account_sid: e.target.value }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Twilio Auth Token
                      </label>
                      <input
                        type="password"
                        value={config.sms.twilio_auth_token || ''}
                        onChange={(e) => setConfig({
                          ...config,
                          sms: { ...config.sms, twilio_auth_token: e.target.value }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Twilio Phone Number
                      </label>
                      <input
                        type="text"
                        value={config.sms.twilio_phone_number || ''}
                        onChange={(e) => setConfig({
                          ...config,
                          sms: { ...config.sms, twilio_phone_number: e.target.value }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        placeholder="+1234567890"
                      />
                    </div>
                  </div>
                  <div className="flex justify-end pt-4">
                    <button
                      type="submit"
                      disabled={saving}
                      className="px-8 py-3 bg-gradient-to-r from-purple-600 to-violet-600 text-white rounded-xl shadow-lg hover:shadow-xl hover:from-purple-700 hover:to-violet-700 transition-all disabled:opacity-50 font-semibold text-base"
                    >
                      {saving ? '💾 Saving...' : '💾 Save SMS Config'}
                    </button>
                  </div>
                </div>
              </form>
            )}

            {/* Model Tab */}
            {activeTab === 'model' && (
              <form onSubmit={handleModelSubmit}>
                <div className="space-y-6">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-12 h-12 bg-gradient-to-br from-pink-500 to-rose-600 rounded-xl flex items-center justify-center text-2xl shadow-lg">
                      🤖
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900">AI Model Configuration</h2>
                  </div>
                  
                  {/* LLM Configuration */}
                  <div className="border rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Large Language Model (LLM)</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          LLM Provider
                        </label>
                        <select
                          value={config.model.llm_provider}
                          onChange={(e) => setConfig({
                            ...config,
                            model: { ...config.model, llm_provider: e.target.value }
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        >
                          <option value="openai">OpenAI</option>
                          <option value="anthropic">Anthropic</option>
                          <option value="google">Google</option>
                          <option value="azure_openai">Azure OpenAI</option>
                          <option value="local">Local Model</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          LLM Model
                        </label>
                        <select
                          value={config.model.llm_model}
                          onChange={(e) => setConfig({
                            ...config,
                            model: { ...config.model, llm_model: e.target.value }
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        >
                          <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                          <option value="gpt-4">GPT-4</option>
                          <option value="gpt-4-turbo">GPT-4 Turbo</option>
                          <option value="claude-3-sonnet">Claude 3 Sonnet</option>
                          <option value="claude-3-haiku">Claude 3 Haiku</option>
                          <option value="gemini-pro">Gemini Pro</option>
                          <option value="llama-2-7b">Llama 2 7B</option>
                          <option value="llama-2-13b">Llama 2 13B</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          API Key
                        </label>
                        <input
                          type="password"
                          value={config.model.llm_api_key || ''}
                          onChange={(e) => setConfig({
                            ...config,
                            model: { ...config.model, llm_api_key: e.target.value }
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Base URL (for local models)
                        </label>
                        <input
                          type="text"
                          value={config.model.llm_base_url || ''}
                          onChange={(e) => setConfig({
                            ...config,
                            model: { ...config.model, llm_base_url: e.target.value }
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          placeholder="http://localhost:8000/v1"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Temperature
                        </label>
                        <input
                          type="number"
                          step="0.1"
                          min="0"
                          max="2"
                          value={config.model.llm_temperature}
                          onChange={(e) => setConfig({
                            ...config,
                            model: { ...config.model, llm_temperature: parseFloat(e.target.value) }
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Max Tokens
                        </label>
                        <input
                          type="number"
                          value={config.model.llm_max_tokens}
                          onChange={(e) => setConfig({
                            ...config,
                            model: { ...config.model, llm_max_tokens: parseInt(e.target.value) }
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Embedding Configuration */}
                  <div className="border rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Embedding Model</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Embedding Provider
                        </label>
                        <select
                          value={config.model.embedding_provider}
                          onChange={(e) => setConfig({
                            ...config,
                            model: { ...config.model, embedding_provider: e.target.value }
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        >
                          <option value="openai">OpenAI</option>
                          <option value="huggingface">Hugging Face</option>
                          <option value="sentence_transformers">Sentence Transformers</option>
                          <option value="local">Local Model</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Embedding Model
                        </label>
                        <select
                          value={config.model.embedding_model}
                          onChange={(e) => setConfig({
                            ...config,
                            model: { ...config.model, embedding_model: e.target.value }
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        >
                          <option value="text-embedding-ada-002">text-embedding-ada-002</option>
                          <option value="text-embedding-3-small">text-embedding-3-small</option>
                          <option value="text-embedding-3-large">text-embedding-3-large</option>
                          <option value="all-MiniLM-L6-v2">all-MiniLM-L6-v2</option>
                          <option value="all-mpnet-base-v2">all-mpnet-base-v2</option>
                          <option value="paraphrase-multilingual-MiniLM-L12-v2">paraphrase-multilingual-MiniLM-L12-v2</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Embedding API Key
                        </label>
                        <input
                          type="password"
                          value={config.model.embedding_api_key || ''}
                          onChange={(e) => setConfig({
                            ...config,
                            model: { ...config.model, embedding_api_key: e.target.value }
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Embedding Base URL
                        </label>
                        <input
                          type="text"
                          value={config.model.embedding_base_url || ''}
                          onChange={(e) => setConfig({
                            ...config,
                            model: { ...config.model, embedding_base_url: e.target.value }
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          placeholder="http://localhost:8000/v1"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Embedding Dimensions
                        </label>
                        <input
                          type="number"
                          value={config.model.embedding_dimensions}
                          onChange={(e) => setConfig({
                            ...config,
                            model: { ...config.model, embedding_dimensions: parseInt(e.target.value) }
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        />
                      </div>
                    </div>
                  </div>

                  <div className="flex justify-end pt-4">
                    <button
                      type="submit"
                      disabled={saving}
                      className="px-8 py-3 bg-gradient-to-r from-pink-600 to-rose-600 text-white rounded-xl shadow-lg hover:shadow-xl hover:from-pink-700 hover:to-rose-700 transition-all disabled:opacity-50 font-semibold text-base"
                    >
                      {saving ? '💾 Saving...' : '💾 Save Model Config'}
                    </button>
                  </div>
                </div>
              </form>
            )}

            {/* Vector DB Tab */}
            {activeTab === 'vector_db' && (
              <form onSubmit={handleVectorDBSubmit}>
                <div className="space-y-6">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-amber-600 rounded-xl flex items-center justify-center text-2xl shadow-lg">
                      🗄️
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900">Vector Database Configuration</h2>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Vector DB Provider
                      </label>
                      <select
                        value={config.vector_db.provider}
                        onChange={(e) => setConfig({
                          ...config,
                          vector_db: { ...config.vector_db, provider: e.target.value }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      >
                        <option value="chroma">Chroma</option>
                        <option value="pinecone">Pinecone</option>
                        <option value="weaviate">Weaviate</option>
                        <option value="faiss">FAISS</option>
                      </select>
                    </div>
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        checked={config.vector_db.enabled}
                        onChange={(e) => setConfig({
                          ...config,
                          vector_db: { ...config.vector_db, enabled: e.target.checked }
                        })}
                        className="mr-2"
                      />
                      <label className="text-sm font-medium text-gray-700">Enable Vector Database</label>
                    </div>
                  </div>

                  {/* Chroma Configuration */}
                  {config.vector_db.provider === 'chroma' && (
                    <div className="border rounded-lg p-4">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Chroma Configuration</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Chroma Host
                          </label>
                          <input
                            type="text"
                            value={config.vector_db.chroma_host}
                            onChange={(e) => setConfig({
                              ...config,
                              vector_db: { ...config.vector_db, chroma_host: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Chroma Port
                          </label>
                          <input
                            type="number"
                            value={config.vector_db.chroma_port}
                            onChange={(e) => setConfig({
                              ...config,
                              vector_db: { ...config.vector_db, chroma_port: parseInt(e.target.value) }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Collection Name
                          </label>
                          <input
                            type="text"
                            value={config.vector_db.chroma_collection_name}
                            onChange={(e) => setConfig({
                              ...config,
                              vector_db: { ...config.vector_db, chroma_collection_name: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Persist Directory
                          </label>
                          <input
                            type="text"
                            value={config.vector_db.chroma_persist_directory || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              vector_db: { ...config.vector_db, chroma_persist_directory: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                            placeholder="./vector_store"
                          />
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Pinecone Configuration */}
                  {config.vector_db.provider === 'pinecone' && (
                    <div className="border rounded-lg p-4">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Pinecone Configuration</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            API Key
                          </label>
                          <input
                            type="password"
                            value={config.vector_db.pinecone_api_key || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              vector_db: { ...config.vector_db, pinecone_api_key: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Environment
                          </label>
                          <input
                            type="text"
                            value={config.vector_db.pinecone_environment || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              vector_db: { ...config.vector_db, pinecone_environment: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                            placeholder="us-west1-gcp"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Index Name
                          </label>
                          <input
                            type="text"
                            value={config.vector_db.pinecone_index_name}
                            onChange={(e) => setConfig({
                              ...config,
                              vector_db: { ...config.vector_db, pinecone_index_name: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Namespace
                          </label>
                          <input
                            type="text"
                            value={config.vector_db.pinecone_namespace || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              vector_db: { ...config.vector_db, pinecone_namespace: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Weaviate Configuration */}
                  {config.vector_db.provider === 'weaviate' && (
                    <div className="border rounded-lg p-4">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Weaviate Configuration</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Weaviate URL
                          </label>
                          <input
                            type="text"
                            value={config.vector_db.weaviate_url}
                            onChange={(e) => setConfig({
                              ...config,
                              vector_db: { ...config.vector_db, weaviate_url: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            API Key
                          </label>
                          <input
                            type="password"
                            value={config.vector_db.weaviate_api_key || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              vector_db: { ...config.vector_db, weaviate_api_key: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Class Name
                          </label>
                          <input
                            type="text"
                            value={config.vector_db.weaviate_class_name}
                            onChange={(e) => setConfig({
                              ...config,
                              vector_db: { ...config.vector_db, weaviate_class_name: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                      </div>
                    </div>
                  )}

                  {/* FAISS Configuration */}
                  {config.vector_db.provider === 'faiss' && (
                    <div className="border rounded-lg p-4">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">FAISS Configuration</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Index Path
                          </label>
                          <input
                            type="text"
                            value={config.vector_db.faiss_index_path}
                            onChange={(e) => setConfig({
                              ...config,
                              vector_db: { ...config.vector_db, faiss_index_path: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Index Type
                          </label>
                          <select
                            value={config.vector_db.faiss_index_type}
                            onChange={(e) => setConfig({
                              ...config,
                              vector_db: { ...config.vector_db, faiss_index_type: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          >
                            <option value="Flat">Flat</option>
                            <option value="IVF">IVF</option>
                            <option value="HNSW">HNSW</option>
                          </select>
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="flex justify-end pt-4">
                    <button
                      type="submit"
                      disabled={saving}
                      className="px-8 py-3 bg-gradient-to-r from-orange-600 to-amber-600 text-white rounded-xl shadow-lg hover:shadow-xl hover:from-orange-700 hover:to-amber-700 transition-all disabled:opacity-50 font-semibold text-base"
                    >
                      {saving ? '💾 Saving...' : '💾 Save Vector DB Config'}
                    </button>
                  </div>
                </div>
              </form>
            )}

            {/* Knowledge Provider Tab */}
            {activeTab === 'knowledge_provider' && (
              <form onSubmit={handleKnowledgeProviderSubmit}>
                <div className="space-y-6">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-blue-600 rounded-xl flex items-center justify-center text-2xl shadow-lg">
                      📚
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900">Knowledge Provider Configuration</h2>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Knowledge Provider
                      </label>
                      <select
                        value={config.knowledge_provider.provider}
                        onChange={(e) => setConfig({
                          ...config,
                          knowledge_provider: { ...config.knowledge_provider, provider: e.target.value }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      >
                        <option value="local">Local Storage</option>
                        <option value="aws_s3">AWS S3</option>
                        <option value="azure_blob">Azure Blob Storage</option>
                        <option value="google_drive">Google Drive</option>
                        <option value="dropbox">Dropbox</option>
                      </select>
                    </div>
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        checked={config.knowledge_provider.enabled}
                        onChange={(e) => setConfig({
                          ...config,
                          knowledge_provider: { ...config.knowledge_provider, enabled: e.target.checked }
                        })}
                        className="mr-2"
                      />
                      <label className="text-sm font-medium text-gray-700">Enable Knowledge Provider</label>
                    </div>
                  </div>

                  {/* AWS S3 Configuration */}
                  {config.knowledge_provider.provider === 'aws_s3' && (
                    <div className="border rounded-lg p-4">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">AWS S3 Configuration</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Access Key ID
                          </label>
                          <input
                            type="text"
                            value={config.knowledge_provider.aws_access_key_id || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              knowledge_provider: { ...config.knowledge_provider, aws_access_key_id: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Secret Access Key
                          </label>
                          <input
                            type="password"
                            value={config.knowledge_provider.aws_secret_access_key || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              knowledge_provider: { ...config.knowledge_provider, aws_secret_access_key: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Region
                          </label>
                          <input
                            type="text"
                            value={config.knowledge_provider.aws_region}
                            onChange={(e) => setConfig({
                              ...config,
                              knowledge_provider: { ...config.knowledge_provider, aws_region: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Bucket Name
                          </label>
                          <input
                            type="text"
                            value={config.knowledge_provider.aws_bucket_name || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              knowledge_provider: { ...config.knowledge_provider, aws_bucket_name: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Prefix
                          </label>
                          <input
                            type="text"
                            value={config.knowledge_provider.aws_prefix}
                            onChange={(e) => setConfig({
                              ...config,
                              knowledge_provider: { ...config.knowledge_provider, aws_prefix: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Azure Blob Storage Configuration */}
                  {config.knowledge_provider.provider === 'azure_blob' && (
                    <div className="border rounded-lg p-4">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Azure Blob Storage Configuration</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Account Name
                          </label>
                          <input
                            type="text"
                            value={config.knowledge_provider.azure_account_name || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              knowledge_provider: { ...config.knowledge_provider, azure_account_name: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Account Key
                          </label>
                          <input
                            type="password"
                            value={config.knowledge_provider.azure_account_key || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              knowledge_provider: { ...config.knowledge_provider, azure_account_key: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Container Name
                          </label>
                          <input
                            type="text"
                            value={config.knowledge_provider.azure_container_name || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              knowledge_provider: { ...config.knowledge_provider, azure_container_name: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Connection String
                          </label>
                          <input
                            type="text"
                            value={config.knowledge_provider.azure_connection_string || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              knowledge_provider: { ...config.knowledge_provider, azure_connection_string: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Google Drive Configuration */}
                  {config.knowledge_provider.provider === 'google_drive' && (
                    <div className="border rounded-lg p-4">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Google Drive Configuration</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Credentials File Path
                          </label>
                          <input
                            type="text"
                            value={config.knowledge_provider.google_credentials_file || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              knowledge_provider: { ...config.knowledge_provider, google_credentials_file: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                            placeholder="./credentials.json"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Folder ID
                          </label>
                          <input
                            type="text"
                            value={config.knowledge_provider.google_folder_id || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              knowledge_provider: { ...config.knowledge_provider, google_folder_id: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Service Account Email
                          </label>
                          <input
                            type="email"
                            value={config.knowledge_provider.google_service_account_email || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              knowledge_provider: { ...config.knowledge_provider, google_service_account_email: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Dropbox Configuration */}
                  {config.knowledge_provider.provider === 'dropbox' && (
                    <div className="border rounded-lg p-4">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Dropbox Configuration</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Access Token
                          </label>
                          <input
                            type="password"
                            value={config.knowledge_provider.dropbox_access_token || ''}
                            onChange={(e) => setConfig({
                              ...config,
                              knowledge_provider: { ...config.knowledge_provider, dropbox_access_token: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Folder Path
                          </label>
                          <input
                            type="text"
                            value={config.knowledge_provider.dropbox_folder_path}
                            onChange={(e) => setConfig({
                              ...config,
                              knowledge_provider: { ...config.knowledge_provider, dropbox_folder_path: e.target.value }
                            })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          />
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="flex justify-end pt-4">
                    <button
                      type="submit"
                      disabled={saving}
                      className="px-8 py-3 bg-gradient-to-r from-indigo-600 to-blue-600 text-white rounded-xl shadow-lg hover:shadow-xl hover:from-indigo-700 hover:to-blue-700 transition-all disabled:opacity-50 font-semibold text-base"
                    >
                      {saving ? '💾 Saving...' : '💾 Save Knowledge Provider Config'}
                    </button>
                  </div>
                </div>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}