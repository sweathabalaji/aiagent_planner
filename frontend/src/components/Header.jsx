import React from 'react'
import { Plane, Globe, Sparkles } from 'lucide-react'

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-blue-600 rounded-lg">
              <Plane className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">PlanAI</h1>
              <p className="text-sm text-gray-500">AI-Powered Travel Planning</p>
            </div>
          </div>
          
          <div className="hidden md:flex items-center space-x-6">
            <div className="flex items-center space-x-2 text-gray-600">
              <Globe className="h-4 w-4" />
              <span className="text-sm">Global Coverage</span>
            </div>
            <div className="flex items-center space-x-2 text-gray-600">
              <Sparkles className="h-4 w-4" />
              <span className="text-sm">AI-Powered</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
