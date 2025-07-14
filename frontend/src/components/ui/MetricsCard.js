import React from 'react'

export function MetricsCard({ title, value, icon, className = '' }) {
  return (
    <div className={`bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">{title}</h3>
        {icon && (
          <div className="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center">
            {icon}
          </div>
        )}
      </div>
      <p className="text-3xl font-bold text-primary-600 dark:text-primary-400">
        {value}
      </p>
    </div>
  )
}
