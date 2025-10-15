'use client'

import { useState, useEffect } from 'react'
import { flightsAPI } from '@/lib/api'

interface Flight {
  flight_number: string
  airline: string
  origin: string
  destination: string
  departure_time: string
  arrival_time: string
  duration_minutes: number
}

export default function FlightsPage() {
  const [flights, setFlights] = useState<Flight[]>([])
  const [loading, setLoading] = useState(false)
  const [origin, setOrigin] = useState('')
  const [destination, setDestination] = useState('')

  const searchFlights = async () => {
    try {
      setLoading(true)
      const params: any = {}
      if (origin) params.origin = origin.toUpperCase()
      if (destination) params.destination = destination.toUpperCase()
      
      const data = await flightsAPI.search(params)
      setFlights(data.flights || [])
    } catch (error) {
      console.error('Error searching flights:', error)
      setFlights([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    searchFlights()
  }, [])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    searchFlights()
  }

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    return `${hours}h ${mins}m`
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="container mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">✈️ Flight Routes</h1>
          <p className="text-gray-600 mt-2">Search available flight routes</p>
        </div>

        {/* Search Form */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <form onSubmit={handleSearch} className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Origin Airport
              </label>
              <input
                type="text"
                placeholder="JFK, LAX, ORD..."
                value={origin}
                onChange={(e) => setOrigin(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent uppercase"
                maxLength={3}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Destination Airport
              </label>
              <input
                type="text"
                placeholder="JFK, LAX, ORD..."
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent uppercase"
                maxLength={3}
              />
            </div>
            <div className="flex items-end">
              <button
                type="submit"
                className="w-full px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                🔍 Search Flights
              </button>
            </div>
          </form>
        </div>

        {/* Results */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="p-6 border-b">
            <h2 className="text-xl font-bold text-gray-900">
              Available Flights {flights.length > 0 && `(${flights.length})`}
            </h2>
          </div>

          {loading ? (
            <div className="p-8 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Searching flights...</p>
            </div>
          ) : flights.length === 0 ? (
            <div className="p-8 text-center">
              <p className="text-gray-500">No flights found. Try different airports.</p>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {flights.map((flight) => (
                <div key={flight.flight_number} className="p-6 hover:bg-gray-50">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-8">
                      {/* Flight Number */}
                      <div>
                        <p className="text-xs text-gray-500">{flight.airline}</p>
                        <p className="text-lg font-bold text-blue-600">{flight.flight_number}</p>
                      </div>

                      {/* Route */}
                      <div className="flex items-center space-x-4">
                        <div className="text-right">
                          <p className="text-2xl font-bold text-gray-900">{flight.origin}</p>
                          <p className="text-sm text-gray-500">{flight.departure_time}</p>
                        </div>
                        <div className="text-center">
                          <p className="text-gray-400">✈️</p>
                          <p className="text-xs text-gray-500">{formatDuration(flight.duration_minutes)}</p>
                        </div>
                        <div className="text-left">
                          <p className="text-2xl font-bold text-gray-900">{flight.destination}</p>
                          <p className="text-sm text-gray-500">{flight.arrival_time}</p>
                        </div>
                      </div>
                    </div>

                    {/* Duration Badge */}
                    <div className="text-right">
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                        {formatDuration(flight.duration_minutes)}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

