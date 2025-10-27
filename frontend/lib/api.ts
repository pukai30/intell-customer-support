import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Knowledge Base API
export const knowledgeAPI = {
  // Get all knowledge documents
  list: async (params?: { category?: string; limit?: number }) => {
    const response = await api.get('/api/knowledge/list', { params })
    return response.data
  },

  // Get single document
  get: async (id: string) => {
    const response = await api.get(`/api/knowledge/${id}`)
    return response.data
  },

  // Create new knowledge
  create: async (data: {
    title: string
    content: string
    category: string
    tags: string[]
    is_temporary?: boolean
    expires_in_days?: number
    created_by?: string
  }) => {
    const response = await api.post('/api/knowledge/add', data)
    return response.data
  },

  // Upload file
  upload: async (formData: FormData) => {
    const response = await api.post('/api/knowledge/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // Update knowledge
  update: async (id: string, data: {
    title?: string
    content?: string
    category?: string
    tags?: string[]
  }) => {
    const response = await api.put(`/api/knowledge/${id}`, data)
    return response.data
  },

  // Delete knowledge
  delete: async (id: string, hardDelete = false) => {
    const response = await api.delete(`/api/knowledge/${id}`, {
      params: { hard_delete: hardDelete }
    })
    return response.data
  },

  // Get categories
  categories: async () => {
    const response = await api.get('/api/knowledge/categories/list')
    return response.data
  },
}

// Tickets API
export const ticketsAPI = {
  // Get all tickets
  list: async (params?: { status?: string; channel?: string; limit?: number }) => {
    const response = await api.get('/api/tickets', { params })
    return response.data
  },

  // Get single ticket
  get: async (ticketId: string) => {
    const response = await api.get(`/api/tickets/${ticketId}`)
    return response.data
  },

  // Update ticket status
  updateStatus: async (ticketId: string, status: string) => {
    const response = await api.put(`/api/tickets/${ticketId}/status`, null, {
      params: { status }
    })
    return response.data
  },

  // Assign ticket to agent
  assign: async (ticketId: string, assignedTo: string, notes?: string) => {
    const response = await api.post(`/api/tickets/${ticketId}/assign`, {
      ticket_id: ticketId,
      assigned_to: assignedTo,
      notes: notes
    })
    return response.data
  },

  // Get unassigned tickets
  getUnassigned: async (requiresHumanOnly = true) => {
    const response = await api.get('/api/tickets/unassigned', {
      params: { requires_human_only: requiresHumanOnly }
    })
    return response.data
  },

  // Get assigned tickets for an agent
  getAssigned: async (agentEmail: string) => {
    const response = await api.get(`/api/tickets/assigned/${agentEmail}`)
    return response.data
  },

  // Reassign ticket to different agent
  reassign: async (ticketId: string, newAgentId: string, reason?: string) => {
    const response = await api.post(`/api/tickets/${ticketId}/reassign`, {
      ticket_id: ticketId,
      new_agent_id: newAgentId,
      reason: reason
    })
    return response.data
  },

  // Check WhatsApp messages on-demand
  checkWhatsApp: async () => {
    const response = await api.post('/api/whatsapp/check-messages')
    return response.data
  },
}

// Notifications API
export const notificationsAPI = {
  // Get pending notifications
  getPending: async () => {
    const response = await api.get('/api/notifications/pending')
    return response.data
  },

  // Mark notification as sent
  markSent: async (ticketId: string) => {
    const response = await api.post(`/api/notifications/${ticketId}/mark-sent`)
    return response.data
  },
}

// Agents API
export const agentsAPI = {
  // Get all agents
  list: async (activeOnly = true) => {
    const response = await api.get('/api/agents/list', {
      params: { active_only: activeOnly }
    })
    return response.data
  },

  // Get agent details
  get: async (agentId: string) => {
    const response = await api.get(`/api/agents/${agentId}`)
    return response.data
  },

  // Get agent statistics
  getStats: async (agentId: string) => {
    const response = await api.get(`/api/agents/${agentId}/stats`)
    return response.data
  },

  // Get team statistics
  getTeamStats: async () => {
    const response = await api.get('/api/agents/team/stats')
    return response.data
  },

  // Update agent status
  updateStatus: async (agentId: string, isActive: boolean) => {
    const response = await api.put(`/api/agents/${agentId}/status`, null, {
      params: { is_active: isActive }
    })
    return response.data
  },

  // Create agent
  create: async (data: {
    agent_id: string
    name: string
    email: string
    skills: string[]
    skill_levels?: Record<string, string>
    max_concurrent_tickets?: number
    channels?: string[]
    shift_start?: string
    shift_end?: string
    timezone?: string
  }) => {
    const response = await api.post('/api/agents/create', data)
    return response.data
  },
}

// Stats API
export const statsAPI = {
  get: async () => {
    const response = await api.get('/api/stats')
    return response.data
  },
}

// Configuration API
export const configAPI = {
  // Get system configuration
  get: async () => {
    const response = await api.get('/api/config')
    return response.data
  },

  // Update system configuration
  update: async (data: {
    support_email: string
    email_host?: string
    email_port?: number
    email_user?: string
    email_password?: string
    sms_enabled?: boolean
    sms_phone_number?: string
    twilio_account_sid?: string
    twilio_auth_token?: string
    twilio_phone_number?: string
    whatsapp_enabled?: boolean
    whatsapp_number?: string
    chat_enabled?: boolean
  }) => {
    const response = await api.put('/api/config', data)
    return response.data
  },

  // Enhanced Configuration APIs
  getEnhanced: async () => {
    const response = await api.get('/api/config/enhanced')
    return response.data
  },

  getSection: async (section: string) => {
    const response = await api.get(`/api/config/${section}`)
    return response.data
  },

  updateEmail: async (data: any) => {
    const response = await api.put('/api/config/email', data)
    return response.data
  },

  updateWhatsApp: async (data: any) => {
    const response = await api.put('/api/config/whatsapp', data)
    return response.data
  },

  updateSMS: async (data: any) => {
    const response = await api.put('/api/config/sms', data)
    return response.data
  },

  updateModel: async (data: any) => {
    const response = await api.put('/api/config/model', data)
    return response.data
  },

  updateVectorDB: async (data: any) => {
    const response = await api.put('/api/config/vector-db', data)
    return response.data
  },

  updateKnowledgeProvider: async (data: any) => {
    const response = await api.put('/api/config/knowledge-provider', data)
    return response.data
  },
}

// SLA API
export const slaAPI = {
  // Get SLA dashboard
  dashboard: async () => {
    const response = await api.get('/api/sla/dashboard')
    return response.data
  },

  // Get SLA breaches
  breaches: async () => {
    const response = await api.get('/api/sla/breaches')
    return response.data
  },

  // Get escalation history for ticket
  escalationHistory: async (ticketId: string) => {
    const response = await api.get(`/api/tickets/${ticketId}/escalation-history`)
    return response.data
  },

  // Manually escalate ticket
  escalateTicket: async (ticketId: string, reason: string) => {
    const response = await api.post(`/api/escalation/manual/${ticketId}?reason=${encodeURIComponent(reason)}`)
    return response.data
  },
}

export default api

