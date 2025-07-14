import React, { useState } from 'react'
import { PrimaryButton, SecondaryButton } from '../ui/Button'
import { api } from '../../lib/api'
import { toast } from 'react-toastify'

export function DocumentUpload() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [chunkStrategy, setChunkStrategy] = useState('default')

  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      setSelectedFile(file)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      toast.error('Please select a file first')
      return
    }

    setIsUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', selectedFile)
      formData.append('strategy', chunkStrategy)

      const response = await api.post('/ingest', formData)
      toast.success('File uploaded successfully')
      // Reset form
      setSelectedFile(null)
      setChunkStrategy('default')
    } catch (error) {
      toast.error(error.message || 'Failed to upload file')
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md">
      <h2 className="text-2xl font-bold mb-4">Upload Document</h2>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">
            Select File
          </label>
          <input
            type="file"
            onChange={handleFileSelect}
            className="block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-primary-50 file:text-primary-700
              hover:file:bg-primary-100"
            accept=".pdf,.docx,.md,.txt"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">
            Chunking Strategy
          </label>
          <select
            value={chunkStrategy}
            onChange={(e) => setChunkStrategy(e.target.value)}
            className="w-full p-2 border rounded-md"
          >
            <option value="default">Default</option>
            <option value="paragraph">By Paragraph</option>
            <option value="sentence">By Sentence</option>
          </select>
        </div>

        <div className="flex justify-end space-x-2">
          <SecondaryButton onClick={() => setSelectedFile(null)}>
            Clear
          </SecondaryButton>
          <PrimaryButton
            onClick={handleUpload}
            disabled={isUploading || !selectedFile}
          >
            {isUploading ? 'Uploading...' : 'Upload'}
          </PrimaryButton>
        </div>
      </div>
    </div>
  )
}
