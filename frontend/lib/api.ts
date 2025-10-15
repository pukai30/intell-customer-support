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

// Booking API (Airline Support) - COMMENTED OUT
/*
export const bookingsAPI = {
  // Create booking
  create: async (data: {
    booking_reference: string
    customer_email: string
    customer_name: string
    customer_phone?: string
    flight_number: string
    origin: string
    destination: string
    departure_date: string
    arrival_date: string
    booking_class?: string
    seat_number?: string
    ticket_price: number
    passengers?: any[]
    special_requests?: string
  }) => {
    const response = await api.post('/api/bookings/create', data)
    return response.data
  },

  // Get booking by reference
  get: async (bookingReference: string) => {
    const response = await api.get(`/api/bookings/${bookingReference}`)
    return response.data
  },

  // Get customer bookings
  getByCustomer: async (customerEmail: string) => {
    const response = await api.get(`/api/bookings/customer/${customerEmail}`)
    return response.data
  },

  // Update booking
  update: async (bookingReference: string, data: any) => {
    const response = await api.put(`/api/bookings/${bookingReference}`, data)
    return response.data
  },
}

// Flight API (Airline Support)
export const flightsAPI = {
  // Create flight route
  create: async (data: {
    flight_number: string
    airline: string
    origin: string
    destination: string
    departure_time: string
    arrival_time: string
    duration_minutes: number
    aircraft_type?: string
    days_of_operation?: string[]
  }) => {
    const response = await api.post('/api/flights/create', data)
    return response.data
  },

  // Get flight by number
  get: async (flightNumber: string) => {
    const response = await api.get(`/api/flights/${flightNumber}`)
    return response.data
  },

  // Search flights
  search: async (params?: { origin?: string; destination?: string }) => {
    const response = await api.get('/api/flights/search', { params })
    return response.data
  },
}
*/

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

