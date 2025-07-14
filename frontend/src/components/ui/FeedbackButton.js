'use client'

import React, { useState } from 'react'
import { toast } from 'react-toastify'
import { FaBug } from 'react-icons/fa'

export function FeedbackButton() {
  const [isOpen, setIsOpen] = useState(false)
  const [feedback, setFeedback] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!feedback.trim()) {
      toast.error('Please enter your feedback')
      return
    }

    try {
      setLoading(true)
      // TODO: Implement actual feedback submission
      toast.success('Feedback submitted successfully')
      setFeedback('')
      setIsOpen(false)
    } catch (error) {
      toast.error('Failed to submit feedback')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-full transition-colors"
      >
        <FaBug className="w-5 h-5" />
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-96">
            <h2 className="text-xl font-bold mb-4">Send Feedback</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <textarea
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                placeholder="Please share your feedback..."
                className="w-full p-2 border rounded"
                rows={4}
              />
              <div className="flex justify-end space-x-2">
                <button
                  onClick={() => setIsOpen(false)}
                  className="bg-gray-200 hover:bg-gray-300 px-4 py-2 rounded"
                  type="button"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
                  disabled={loading}
                >
                  {loading ? 'Submitting...' : 'Submit'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
