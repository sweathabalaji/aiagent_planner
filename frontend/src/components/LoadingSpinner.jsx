import React from 'react'
import { Loader2, Plane, MapPin, Calendar, BookOpen, Brain, Search } from 'lucide-react'

const LoadingSpinner = ({ message, submessage, steps, duration }) => {
  // Default travel-related steps
  const defaultSteps = [
    { icon: Plane, text: "Searching for flights...", delay: 0 },
    { icon: MapPin, text: "Finding hotels...", delay: 1000 },
    { icon: Calendar, text: "Creating itinerary...", delay: 2000 },
  ]

  const loadingSteps = steps || defaultSteps
  const mainMessage = message || "Creating Your Perfect Trip"
  const subMessage = submessage || "Our AI is working hard to find the best options for you..."
  const timeDuration = duration || "10-30 seconds"

  return (
    <div className="text-center py-16">
      <div className="card max-w-lg mx-auto">
        <div className="mb-8">
          <div className="flex justify-center mb-4">
            <Loader2 className="h-16 w-16 text-blue-600 animate-spin" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            {mainMessage}
          </h2>
          <p className="text-gray-600">
            {subMessage}
          </p>
        </div>

        {loadingSteps && loadingSteps.length > 0 && (
          <div className="space-y-4">
            {loadingSteps.map((step, index) => {
              const Icon = step.icon
              return (
                <div 
                  key={index}
                  className="flex items-center space-x-3 p-3 rounded-lg bg-gray-50 animate-pulse"
                  style={{
                    animationDelay: `${step.delay}ms`,
                    animationDuration: '2s'
                  }}
                >
                  <Icon className="h-5 w-5 text-blue-600" />
                  <span className="text-gray-700">{step.text}</span>
                </div>
              )
            })}
          </div>
        )}

        <div className="mt-8 text-sm text-gray-500">
          This usually takes {timeDuration}
        </div>
      </div>
    </div>
  )
}

export default LoadingSpinner
