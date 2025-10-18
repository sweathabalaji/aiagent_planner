import React from 'react'
import { MapPin, Calendar, Plane, Sparkles, ArrowRight } from 'lucide-react'

const Hero = ({ onStartPlanning }) => {
  return (
    <div className="hero-bg text-white py-20">
      <div className="container mx-auto px-4 text-center">
        <div className="max-w-4xl mx-auto">
          <div className="flex justify-center mb-6">
            <div className="animate-pulse-slow">
              <Sparkles className="h-16 w-16 text-yellow-300" />
            </div>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-6 animate-fade-in">
            Plan Your Perfect Trip with 
            <span className="block text-yellow-300">AI Intelligence</span>
          </h1>
          
          <p className="text-xl md:text-2xl mb-8 text-blue-100 animate-slide-up">
            Get personalized travel recommendations for flights, hotels, and activities 
            powered by Tavily AI search technology
          </p>
          
          <div className="flex flex-wrap justify-center gap-6 mb-10 text-blue-100">
            <div className="flex items-center space-x-2">
              <Plane className="h-5 w-5" />
              <span>Flight Booking</span>
            </div>
            <div className="flex items-center space-x-2">
              <MapPin className="h-5 w-5" />
              <span>Hotel Recommendations</span>
            </div>
            <div className="flex items-center space-x-2">
              <Calendar className="h-5 w-5" />
              <span>Itinerary Planning</span>
            </div>
          </div>
          
          <button 
            onClick={onStartPlanning}
            className="bg-yellow-400 hover:bg-yellow-500 text-gray-900 font-bold py-4 px-8 rounded-xl text-lg transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl flex items-center space-x-2 mx-auto"
          >
            <span>Start Planning Your Trip</span>
            <ArrowRight className="h-5 w-5" />
          </button>
          
          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto">
            <div className="bg-white/10 backdrop-blur rounded-xl p-6 text-center">
              <div className="text-3xl font-bold text-yellow-300">3</div>
              <div className="text-sm text-blue-100">Plan Variants</div>
            </div>
            <div className="bg-white/10 backdrop-blur rounded-xl p-6 text-center">
              <div className="text-3xl font-bold text-yellow-300">Tavily</div>
              <div className="text-sm text-blue-100">Powered Search</div>
            </div>
            <div className="bg-white/10 backdrop-blur rounded-xl p-6 text-center">
              <div className="text-3xl font-bold text-yellow-300">AI</div>
              <div className="text-sm text-blue-100">Powered Suggestions</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Hero
