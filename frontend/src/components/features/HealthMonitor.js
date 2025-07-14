import React, { useState, useEffect } from 'react'
import { api } from '../../lib/api'
import { toast } from 'react-toastify'
import { FaCheckCircle, FaTimesCircle } from 'react-icons/fa'

export function HealthMonitor() {
  const [health, setHealth] = useState({
    api: { status: 'unknown', message: '' },
    database: { status: 'unknown', message: '' },
    vectorStore: { status: 'unknown', message: '' },
    model: { status: 'unknown', message: '' }
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    checkHealth()
    // Poll for updates every 30 seconds
    const interval = setInterval(checkHealth, 30000)
    return () => clearInterval(interval)
  }, [])

  const checkHealth = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get('/admin/health')
      setHealth(response.data)
    } catch (err) {
      setError(err.message || 'Failed to check health')
    } finally {
      setLoading(false)
    }
  }

  const getStatusIcon = (status) => {
    return status === 'healthy' ? (
      <FaCheckCircle className="w-5 h-5 text-green-500" />
    ) : (
      <FaTimesCircle className="w-5 h-5 text-red-500" />
    )
  }

  if (loading) {
    return (
      <div className="p-4 text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-4 text-red-500">
        Error: {error}
      </div>
    )
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md">
      <h2 className="text-2xl font-bold mb-4">System Health</h2>
      
      <div className="space-y-4">
        {Object.entries(health).map(([service, { status, message }]) => (
          <div key={service} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div>
              <h3 className="font-medium">{service.replace(/([A-Z])/g, ' $1').trim()}</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">{message || 'No additional information'}</p>
            </div>
            {getStatusIcon(status)}
          </div>
        ))}
      </div>

      <div className="mt-4">
        <button
          onClick={checkHealth}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 dark:bg-primary-500 dark:hover:bg-primary-600"
        >
          Check Health Now
        </button>
      </div>
    </div>
  )
}
