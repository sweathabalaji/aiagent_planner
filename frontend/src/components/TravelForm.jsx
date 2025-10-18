import React, { useState } from 'react'
import { MapPin, Calendar, DollarSign, Users, Heart, Send, ArrowLeft } from 'lucide-react'

const TravelForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    origin: '',
    destination: '',
    start_date: '',
    end_date: '',
    budget: '',
    travellers: 1,
    interests: []
  })

  const interestOptions = [
    'sightseeing', 'food', 'culture', 'adventure', 'relaxation', 
    'nightlife', 'shopping', 'nature', 'history', 'art', 'sports', 'beach'
  ]

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleInterestToggle = (interest) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    // Convert budget to number
    const submitData = {
      ...formData,
      budget: parseFloat(formData.budget),
      travellers: parseInt(formData.travellers)
    }
    onSubmit(submitData)
  }

  // Get tomorrow's date for min date
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  const minDate = tomorrow.toISOString().split('T')[0]

  return (
    <div className="max-w-4xl mx-auto">
      <div className="card animate-slide-up">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Plan Your Dream Trip</h2>
          <p className="text-gray-600">Fill in the details below and let AI create the perfect itinerary for you</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Origin and Destination */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <MapPin className="inline h-4 w-4 mr-1" />
                From (Origin)
              </label>
              <input
                type="text"
                name="origin"
                value={formData.origin}
                onChange={handleChange}
                placeholder="e.g., BOM, Mumbai, New York"
                className="input-field"
                required
              />
              <p className="text-xs text-gray-500 mt-1">City name or airport code</p>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <MapPin className="inline h-4 w-4 mr-1" />
                To (Destination)
              </label>
              <input
                type="text"
                name="destination"
                value={formData.destination}
                onChange={handleChange}
                placeholder="e.g., DEL, Delhi, Paris"
                className="input-field"
                required
              />
              <p className="text-xs text-gray-500 mt-1">City name or airport code</p>
            </div>
          </div>

          {/* Dates */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Calendar className="inline h-4 w-4 mr-1" />
                Start Date
              </label>
              <input
                type="date"
                name="start_date"
                value={formData.start_date}
                onChange={handleChange}
                min={minDate}
                className="input-field"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Calendar className="inline h-4 w-4 mr-1" />
                End Date
              </label>
              <input
                type="date"
                name="end_date"
                value={formData.end_date}
                onChange={handleChange}
                min={formData.start_date || minDate}
                className="input-field"
                required
              />
            </div>
          </div>

          {/* Budget and Travelers */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <DollarSign className="inline h-4 w-4 mr-1" />
                Budget (₹ INR)
              </label>
              <input
                type="number"
                name="budget"
                value={formData.budget}
                onChange={handleChange}
                placeholder="e.g., 1500"
                min="100"
                step="50"
                className="input-field"
                required
              />
              <p className="text-xs text-gray-500 mt-1">Total budget for the entire trip in Indian Rupees</p>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Users className="inline h-4 w-4 mr-1" />
                Number of Travelers
              </label>
              <select
                name="travellers"
                value={formData.travellers}
                onChange={handleChange}
                className="input-field"
                required
              >
                {[1,2,3,4,5,6,7,8].map(num => (
                  <option key={num} value={num}>{num} {num === 1 ? 'Person' : 'People'}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Interests */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              <Heart className="inline h-4 w-4 mr-1" />
              Interests (Select all that apply)
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {interestOptions.map(interest => (
                <button
                  key={interest}
                  type="button"
                  onClick={() => handleInterestToggle(interest)}
                  className={`p-3 rounded-lg border-2 transition-all duration-200 capitalize text-sm font-medium ${
                    formData.interests.includes(interest)
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 bg-white text-gray-700 hover:border-blue-300 hover:bg-blue-25'
                  }`}
                >
                  {interest}
                </button>
              ))}
            </div>
          </div>

          {/* Submit Button */}
          <div className="pt-6 border-t border-gray-200">
            <button
              type="submit"
              className="w-full btn-primary py-4 text-lg font-semibold flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl transform transition-all duration-200 hover:scale-[1.02]"
            >
              <Send className="h-5 w-5" />
              <span>Create My Travel Plan</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default TravelForm
