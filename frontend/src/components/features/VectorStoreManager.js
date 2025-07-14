import React, { useState, useEffect } from 'react'
import { api } from '../../lib/api'
import { toast } from 'react-toastify'

export function VectorStoreManager() {
  const [stats, setStats] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get('/retrieve/stats')
      setStats(response.data)
    } catch (err) {
      setError(err.message || 'Failed to fetch statistics')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = async () => {
    if (!window.confirm('Are you sure you want to clear the vector store? This action cannot be undone.')) {
      return
    }

    try {
      await api.delete('/retrieve/clear')
      toast.success('Vector store cleared successfully')
      fetchStats()
    } catch (err) {
      toast.error(err.message || 'Failed to clear vector store')
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
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md">
      <h2 className="text-2xl font-bold mb-4">Vector Store Management</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-2">Total Documents</h3>
          <p className="text-3xl font-bold text-primary-600 dark:text-primary-400">
            {stats.totalDocuments || 0}
          </p>
        </div>
        
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-2">Total Chunks</h3>
          <p className="text-3xl font-bold text-primary-600 dark:text-primary-400">
            {stats.totalChunks || 0}
          </p>
        </div>
        
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-2">Storage Size</h3>
          <p className="text-3xl font-bold text-primary-600 dark:text-primary-400">
            {formatBytes(stats.storageSize || 0)}
          </p>
        </div>
        
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-2">Last Updated</h3>
          <p className="text-3xl font-bold text-primary-600 dark:text-primary-400">
            {stats.lastUpdated ? new Date(stats.lastUpdated).toLocaleString() : 'N/A'}
          </p>
        </div>
      </div>

      <div className="flex justify-end">
        <button
          onClick={handleClear}
          className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600"
        >
          Clear Vector Store
        </button>
      </div>
    </div>
  )
}
