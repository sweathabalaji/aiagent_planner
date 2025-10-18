import React, { useState } from 'react'
import TravelForm from './TravelForm'
import TravelResults from './TravelResults'
import LoadingSpinner from './LoadingSpinner'
import toast from 'react-hot-toast'

const TravelPlanner = () => {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [showForm, setShowForm] = useState(true)
  const [error, setError] = useState(null)

  const handlePlanTrip = async (formData) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('Sending travel plan request:', formData);
      const response = await fetch('/api/plan_trip', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('API error response:', errorText);
        throw new Error(`Failed to plan trip: ${response.status} - ${errorText}`);
      }
      
      const data = await response.json();
      console.log('Received travel plan data:', data);
      setResults(data);
      toast.success('Travel plan generated successfully!');
    } catch (err) {
      console.error('Error planning trip:', err);
      setError(`Failed to plan your trip: ${err.message}`);
      toast.error('Failed to plan your trip. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleBackToForm = () => {
    setResults(null)
    setError(null)
    setShowForm(true)
  }

  const handlePlanAnother = () => {
    setResults(null)
    setError(null)
    setShowForm(true)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Travel Planner Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              AI Travel Planner
            </h1>
            <p className="text-lg text-gray-600">
              Plan your perfect trip with our intelligent travel assistant
            </p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      {showForm && !results && !loading && (
        <div className="container mx-auto px-4 py-8">
          <TravelForm onSubmit={handlePlanTrip} error={error} />
        </div>
      )}
      
      {loading && (
        <div className="container mx-auto px-4 py-16">
          <LoadingSpinner />
        </div>
      )}
      
      {results && !loading && (
        <div className="container mx-auto px-4 py-8">
          <TravelResults 
            results={results} 
            onBack={handleBackToForm}
            onPlanAnother={handlePlanAnother}
          />
        </div>
      )}
    </div>
  )
}

export default TravelPlanner
