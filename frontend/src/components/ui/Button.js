import React from 'react'

export function Button({ children, onClick, className = '', ...props }) {
  return (
    <button
      className={`px-4 py-2 rounded-md font-medium transition-colors ${className}`}
      onClick={onClick}
      {...props}
    >
      {children}
    </button>
  )
}

export function PrimaryButton({ children, ...props }) {
  return (
    <Button
      className="bg-primary-600 text-white hover:bg-primary-700 dark:bg-primary-500 dark:hover:bg-primary-600"
      {...props}
    >
      {children}
    </Button>
  )
}

export function SecondaryButton({ children, ...props }) {
  return (
    <Button
      className="bg-gray-200 text-gray-800 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600"
      {...props}
    >
      {children}
    </Button>
  )
}
