import React, { useState, useEffect } from 'react'
import { api } from '../../lib/api'
import { toast } from 'react-toastify'

export function SearchResults() {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [searchParams, setSearchParams] = useState({
    query: '',
    top_k: 5,
    score_threshold: 0.5,
  })

  const handleSearch = async (query) => {
    setSearchParams(prev => ({ ...prev, query }))
  }

  useEffect(() => {
    if (!searchParams.query) return

    const fetchResults = async () => {
      setLoading(true)
      setError(null)
      try {
        const response = await api.post('/retrieve/search', searchParams)
        setResults(response.data.results)
      } catch (err) {
        setError(err.message || 'Failed to fetch results')
        toast.error(error)
      } finally {
        setLoading(false)
      }
    }

    fetchResults()
  }, [searchParams])

  const formatScore = (score) => {
    return (score * 100).toFixed(1) + '%'
  }

  if (loading) {
    return (
      <div className="p-4 text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
        <p className="mt-2 text-sm">Searching...</p>
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

  if (!results.length) {
    return (
      <div className="p-4 text-gray-500">
        {searchParams.query ? "No results found" : "Enter a search query to get started"}
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <SearchInput onSearch={handleSearch} />
      
      <div className="space-y-4">
        {results.map((result, index) => (
          <div
            key={index}
            className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm"
          >
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-lg font-semibold mb-1">
                  {result.metadata.title || 'Untitled Document'}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {result.metadata.source || 'Unknown source'}
                </p>
              </div>
              <span className="text-sm font-medium text-primary-600 dark:text-primary-400">
                {formatScore(result.score)}
              </span>
            </div>
            
            <div className="mt-2">
              <p className="text-gray-700 dark:text-gray-300">
                {result.text}
              </p>
            </div>
            
            <div className="mt-2 flex space-x-2 text-sm">
              <span className="text-gray-500 dark:text-gray-400">
                {result.metadata.date}
              </span>
              <span className="text-gray-500 dark:text-gray-400">
                {result.metadata.tags?.join(', ') || 'No tags'}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
