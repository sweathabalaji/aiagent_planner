import React from 'react'
import { Loader2, MapPin, Users, Camera, Music, Utensils } from 'lucide-react'

const EventLoadingSpinner = () => {
  const loadingSteps = [
    { icon: MapPin, text: "Searching for perfect venues...", delay: 0 },
    { icon: Utensils, text: "Finding catering services...", delay: 1000 },
    { icon: Camera, text: "Locating photographers...", delay: 2000 },
    { icon: Music, text: "Discovering entertainment options...", delay: 3000 },
    { icon: Users, text: "Creating your event plan...", delay: 4000 },
  ]

  return (
    <div className="text-center py-16">
      <div className="card max-w-lg mx-auto">
        <div className="mb-8">
          <div className="flex justify-center mb-4">
            <Loader2 className="h-16 w-16 text-purple-600 animate-spin" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Planning Your Perfect Event
          </h2>
          <p className="text-gray-600">
            Our AI is working hard to find the best vendors and create your ideal event plan...
          </p>
        </div>

        <div className="space-y-4">
          {loadingSteps.map((step, index) => {
            const Icon = step.icon
            return (
              <div 
                key={index}
                className="flex items-center space-x-3 p-3 rounded-lg bg-purple-50 animate-pulse"
                style={{
                  animationDelay: `${step.delay}ms`,
                  animationDuration: '2s'
                }}
              >
                <Icon className="h-5 w-5 text-purple-600" />
                <span className="text-gray-700">{step.text}</span>
              </div>
            )
          })}
        </div>

        <div className="mt-8 text-sm text-gray-500">
          This usually takes 15-45 seconds
        </div>
      </div>
    </div>
  )
}

export default EventLoadingSpinner