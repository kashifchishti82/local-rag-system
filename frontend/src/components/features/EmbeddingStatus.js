import React, { useState, useEffect } from 'react'
import { StatusIndicator, ProgressCircle } from '../ui/StatusIndicator'
import { api } from '../../lib/api'
import { toast } from 'react-toastify'

export function EmbeddingStatus() {
  const [status, setStatus] = useState('idle')
  const [progress, setProgress] = useState(0)
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchStatus()
    // Poll for updates every 5 seconds
    const interval = setInterval(fetchStatus, 5000)
    return () => clearInterval(interval)
  }, [])

  const fetchStatus = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get('/retrieve/stats')
      setStatus(response.data.status)
      setProgress(response.data.progress || 0)
      setDocuments(response.data.documents || [])
    } catch (err) {
      setError(err.message || 'Failed to fetch status')
    } finally {
      setLoading(false)
    }
  }

  const handleReindex = async () => {
    try {
      await api.post('/agents/re-index')
      toast.success('Re-indexing started')
    } catch (err) {
      toast.error(err.message || 'Failed to start re-indexing')
    }
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
      <h2 className="text-2xl font-bold mb-4">Embedding Status</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Overall Status */}
        <div>
          <h3 className="text-lg font-semibold mb-2">System Status</h3>
          <div className="flex items-center gap-2">
            <StatusIndicator status={status} />
            <ProgressCircle progress={progress} />
          </div>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            {status === 'processing' ? 'Generating embeddings...' :
             status === 'completed' ? 'All embeddings generated' :
             status === 'failed' ? 'Error in processing' :
             'Idle'}
          </p>
        </div>

        {/* Document Statuses */}
        <div>
          <h3 className="text-lg font-semibold mb-2">Document Status</h3>
          <div className="space-y-2">
            {documents.map((doc) => (
              <div key={doc.id} className="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-700 rounded">
                <span className="font-medium">{doc.name}</span>
                <StatusIndicator status={doc.status} />
              </div>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="col-span-2">
          <button
            onClick={handleReindex}
            className="w-full px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 dark:bg-primary-500 dark:hover:bg-primary-600"
            disabled={status === 'processing'}
          >
            {status === 'processing' ? 'Re-indexing...' : 'Re-index All'}
          </button>
        </div>
      </div>
    </div>
  )
}
