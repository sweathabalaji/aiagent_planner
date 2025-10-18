import React, { useState } from 'react';
import EventForm from './EventForm';
import EventResults from './EventResults';
import EventLoadingSpinner from './EventLoadingSpinner';
import toast from 'react-hot-toast';

const EventPlanner = () => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(true);
  const [error, setError] = useState(null);

  const handlePlanEvent = async (formData) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('Sending event plan request:', formData);
      const response = await fetch('/api/event/plan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('API error response:', errorText);
        throw new Error(`Failed to plan event: ${response.status} - ${errorText}`);
      }
      
      const data = await response.json();
      console.log('Received event plan data:', data);
      console.log('🔬 DETAILED ANALYSIS CHECK:', {
        'data.agent_analysis': data.agent_analysis,
        'data.agent_analysis?.full_analysis': data.agent_analysis?.full_analysis,
        'data.planning_insights': data.planning_insights,
        'data.contextual_recommendations': data.contextual_recommendations,
        'all_keys': Object.keys(data)
      });
      setResults(data);
      toast.success('Event plan generated successfully!');
    } catch (err) {
      console.error('Error planning event:', err);
      setError(`Failed to plan your event: ${err.message}`);
      toast.error('Failed to plan your event. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleBackToForm = () => {
    setResults(null);
    setError(null);
    setShowForm(true);
  };

  const handlePlanAnother = () => {
    setResults(null);
    setError(null);
    setShowForm(true);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Event Planner Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              AI Event Planner
            </h1>
            <p className="text-lg text-gray-600">
              Plan your perfect event with intelligent vendor recommendations and AI assistance
            </p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      {showForm && !results && !loading && (
        <div className="container mx-auto px-4 py-8">
          <EventForm onSubmit={handlePlanEvent} error={error} />
        </div>
      )}
      
      {loading && (
        <div className="container mx-auto px-4 py-16">
          <EventLoadingSpinner />
        </div>
      )}
      
      {results && !loading && (
        <div className="container mx-auto px-4 py-8">
          <EventResults 
            results={results} 
            onBack={handleBackToForm}
            onPlanAnother={handlePlanAnother}
          />
        </div>
      )}
    </div>
  );
};

export default EventPlanner;