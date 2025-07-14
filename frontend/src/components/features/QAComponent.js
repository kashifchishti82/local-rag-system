import React, { useState } from 'react'
import { api } from '../../lib/api'
import { toast } from 'react-toastify'

export function QAComponent() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [sources, setSources] = useState([])

  const handleAsk = async () => {
    if (!question.trim()) return

    setLoading(true)
    setError(null)
    setAnswer(null)
    
    try {
      const response = await api.post('/agents/qna', {
        query: question,
        top_k: 5,
        score_threshold: 0.5
      })
      
      setAnswer(response.data.answer)
      setSources(response.data.sources || [])
    } catch (err) {
      setError(err.message || 'Failed to get answer')
      toast.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md">
      <h2 className="text-2xl font-bold mb-4">Ask a Question</h2>
      
      <div className="space-y-4">
        <div>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask your question here..."
            className="w-full p-4 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            rows={4}
          />
        </div>

        <button
          onClick={handleAsk}
          disabled={loading || !question.trim()}
          className="w-full px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 dark:bg-primary-500 dark:hover:bg-primary-600"
        >
          {loading ? 'Getting answer...' : 'Get Answer'}
        </button>

        {error && (
          <div className="text-red-500 text-sm mt-2">
            {error}
          </div>
        )}

        {answer && (
          <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <h3 className="font-semibold mb-2">Answer:</h3>
            <p className="text-gray-700 dark:text-gray-300">
              {answer}
            </p>

            {sources.length > 0 && (
              <div className="mt-4">
                <h3 className="font-semibold mb-2">Sources:</h3>
                <ul className="list-disc list-inside text-sm text-gray-600 dark:text-gray-400">
                  {sources.map((source, index) => (
                    <li key={index}>{source}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
