import React from 'react'

export function StatusIndicator({ status, className = '' }) {
  const statusStyles = {
    'processing': 'bg-yellow-100 text-yellow-800',
    'completed': 'bg-green-100 text-green-800',
    'failed': 'bg-red-100 text-red-800',
    'idle': 'bg-gray-100 text-gray-800',
  }

  return (
    <span className={`px-2 py-1 rounded-full text-xs ${statusStyles[status] || 'bg-gray-100 text-gray-800'} ${className}`}>
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  )
}

export function ProgressCircle({ progress, size = 24, className = '' }) {
  const circumference = 2 * Math.PI * size / 2
  const strokeDashoffset = circumference - (progress / 100) * circumference

  return (
    <div className={`relative w-${size} h-${size} ${className}`}>
      <svg className="w-full h-full" viewBox="0 0 36 36">
        <path
          className="stroke-gray-200 dark:stroke-gray-700"
          fill="none"
          strokeWidth="3"
          d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
        />
        <path
          className="stroke-primary-500"
          fill="none"
          strokeWidth="3"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          d="M18 2.0845
               a 15.9155 15.9155 0 0 1 0 31.831
               a 15.9155 15.9155 0 0 1 0 -31.831"
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-sm font-medium">{Math.round(progress)}%</span>
      </div>
    </div>
  )
}
