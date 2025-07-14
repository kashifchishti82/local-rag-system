import React, { useState, useEffect } from 'react'
import { api } from '../../lib/api'
import { toast } from 'react-toastify'
import { MetricsCard } from '../ui/MetricsCard'
import { FaDatabase, FaFileAlt, FaUser, FaClock } from 'react-icons/fa'

export function SystemMetrics() {
  const [metrics, setMetrics] = useState({
    totalDocuments: 0,
    totalChunks: 0,
    totalUsers: 0,
    vectorStoreSize: 0,
    lastUpdated: null
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchMetrics()
    // Poll for updates every 30 seconds
    const interval = setInterval(fetchMetrics, 30000)
    return () => clearInterval(interval)
  }, [])

  const fetchMetrics = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get('/admin/metrics')
      setMetrics(response.data)
    } catch (err) {
      setError(err.message || 'Failed to fetch metrics')
    } finally {
      setLoading(false)
    }
  }

  const formatBytes = (bytes) => {
    if (!bytes) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
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
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <MetricsCard
        title="Total Documents"
        value={metrics.totalDocuments}
        icon={<FaFileAlt className="w-5 h-5 text-primary-600" />}
      />
      
      <MetricsCard
        title="Total Chunks"
        value={metrics.totalChunks}
        icon={<FaDatabase className="w-5 h-5 text-primary-600" />}
      />
      
      <MetricsCard
        title="Total Users"
        value={metrics.totalUsers}
        icon={<FaUser className="w-5 h-5 text-primary-600" />}
      />
      
      <MetricsCard
        title="Vector Store Size"
        value={formatBytes(metrics.vectorStoreSize)}
        icon={<FaDatabase className="w-5 h-5 text-primary-600" />}
      />
      
      <MetricsCard
        title="Last Update"
        value={metrics.lastUpdated ? new Date(metrics.lastUpdated).toLocaleString() : 'N/A'}
        icon={<FaClock className="w-5 h-5 text-primary-600" />}
      />
    </div>
  )
}
