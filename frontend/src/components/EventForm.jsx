import React, { useState, useEffect } from 'react';
import { 
  CalendarDaysIcon, 
  MapPinIcon, 
  UserGroupIcon, 
  CurrencyRupeeIcon,
  SparklesIcon,
  ClockIcon,
  HeartIcon,
  BuildingOfficeIcon,
  CakeIcon,
  AcademicCapIcon,
  BriefcaseIcon
} from '@heroicons/react/24/outline';

const EventForm = ({ onSubmit, error }) => {
  const [formData, setFormData] = useState({
    event_name: '',
    event_type: '',
    location: '',
    event_date: '',
    guest_count: 50,
    budget: 100000,
    duration: '1 day',
    preferences: [],
    special_requirements: [],
    contact_info: ''
  });

  const [templates, setTemplates] = useState({});
  const [selectedTemplate, setSelectedTemplate] = useState(null);

  // Load event templates on component mount
  useEffect(() => {
    const loadTemplates = async () => {
      try {
        const response = await fetch('/api/event/templates');
        const data = await response.json();
        setTemplates(data.templates || {});
      } catch (err) {
        console.error('Failed to load templates:', err);
      }
    };
    
    loadTemplates();
  }, []);

  const eventTypes = [
    { value: 'wedding', label: 'Wedding', icon: HeartIcon, color: 'text-pink-600' },
    { value: 'corporate', label: 'Corporate Event', icon: BuildingOfficeIcon, color: 'text-blue-600' },
    { value: 'birthday', label: 'Birthday Party', icon: CakeIcon, color: 'text-yellow-600' },
    { value: 'conference', label: 'Conference', icon: AcademicCapIcon, color: 'text-indigo-600' },
    { value: 'anniversary', label: 'Anniversary', icon: HeartIcon, color: 'text-red-600' },
    { value: 'other', label: 'Other', icon: SparklesIcon, color: 'text-purple-600' }
  ];

  const preferenceOptions = {
    style: ['traditional', 'modern', 'elegant', 'casual', 'luxury', 'rustic', 'theme-based'],
    venue: ['outdoor', 'indoor', 'garden', 'beach', 'banquet hall', 'home', 'destination'],
    food: ['vegetarian', 'non-vegetarian', 'vegan', 'north indian', 'south indian', 'continental', 'chinese', 'buffet', 'plated'],
    entertainment: ['live music', 'DJ', 'band', 'cultural performance', 'games', 'no entertainment'],
    extras: ['photography', 'videography', 'decoration', 'flowers', 'lighting', 'sound system']
  };

  const specialRequirementOptions = [
    'wheelchair accessible', 'child-friendly', 'parking required', 'live streaming', 
    'air conditioning', 'backup power', 'security', 'valet parking', 'coat check',
    'eco-friendly', 'pet-friendly', 'smoking area', 'wifi required'
  ];

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseInt(value) || 0 : value
    }));
  };

  const handleEventTypeChange = (eventType) => {
    setFormData(prev => ({ ...prev, event_type: eventType }));
    
    // Auto-fill template data if available
    const template = templates[eventType];
    if (template) {
      setSelectedTemplate(template);
      setFormData(prev => ({
        ...prev,
        guest_count: template.typical_guest_count || prev.guest_count,
        duration: template.typical_duration || prev.duration,
        preferences: template.common_preferences || []
      }));
    }
  };

  const handlePreferenceToggle = (preference) => {
    setFormData(prev => ({
      ...prev,
      preferences: prev.preferences.includes(preference)
        ? prev.preferences.filter(p => p !== preference)
        : [...prev.preferences, preference]
    }));
  };

  const handleRequirementToggle = (requirement) => {
    setFormData(prev => ({
      ...prev,
      special_requirements: prev.special_requirements.includes(requirement)
        ? prev.special_requirements.filter(r => r !== requirement)
        : [...prev.special_requirements, requirement]
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validation
    if (!formData.event_name || !formData.event_type || !formData.location || !formData.event_date) {
      alert('Please fill in all required fields');
      return;
    }
    
    if (new Date(formData.event_date) <= new Date()) {
      alert('Event date must be in the future');
      return;
    }
    
    onSubmit(formData);
  };

  const today = new Date().toISOString().split('T')[0];

  return (
    <div className="max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Event Basic Information */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <SparklesIcon className="h-5 w-5 mr-2 text-purple-600" />
            Event Details
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Event Name *
              </label>
              <input
                type="text"
                name="event_name"
                value={formData.event_name}
                onChange={handleInputChange}
                placeholder="e.g., Sarah's Wedding, Tech Conference 2025"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Contact Email
              </label>
              <input
                type="email"
                name="contact_info"
                value={formData.contact_info}
                onChange={handleInputChange}
                placeholder="your.email@example.com"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>
          </div>
        </div>

        {/* Event Type Selection */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Event Type *
          </h3>
          
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {eventTypes.map((type) => {
              const Icon = type.icon;
              return (
                <button
                  key={type.value}
                  type="button"
                  onClick={() => handleEventTypeChange(type.value)}
                  className={`p-4 rounded-lg border-2 transition-all duration-200 ${
                    formData.event_type === type.value
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-purple-300'
                  }`}
                >
                  <Icon className={`h-6 w-6 mx-auto mb-2 ${type.color}`} />
                  <div className="text-sm font-medium text-gray-900">{type.label}</div>
                </button>
              );
            })}
          </div>
          
          {selectedTemplate && (
            <div className="mt-4 p-4 bg-blue-50 rounded-lg">
              <h4 className="font-medium text-blue-900 mb-2">Template Applied: {formData.event_type}</h4>
              <div className="text-sm text-blue-700 space-y-1">
                <p>• Typical Duration: {selectedTemplate.typical_duration}</p>
                <p>• Planning Time: {selectedTemplate.planning_duration}</p>
                <p>• Essential Services: {selectedTemplate.essential_vendors?.join(', ')}</p>
              </div>
            </div>
          )}
        </div>

        {/* Location and Date */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <MapPinIcon className="h-5 w-5 mr-2 text-purple-600" />
            Location & Date
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Location/City *
              </label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleInputChange}
                placeholder="e.g., Mumbai, Delhi, Bangalore"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Event Date *
              </label>
              <input
                type="date"
                name="event_date"
                value={formData.event_date}
                onChange={handleInputChange}
                min={today}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Duration
              </label>
              <select
                name="duration"
                value={formData.duration}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="2 hours">2 hours</option>
                <option value="4 hours">4 hours</option>
                <option value="6 hours">6 hours</option>
                <option value="1 day">1 day</option>
                <option value="2 days">2 days</option>
                <option value="3 days">3 days</option>
              </select>
            </div>
          </div>
        </div>

        {/* Guest Count and Budget */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <UserGroupIcon className="h-5 w-5 mr-2 text-purple-600" />
            Capacity & Budget
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Expected Guests
              </label>
              <input
                type="number"
                name="guest_count"
                value={formData.guest_count}
                onChange={handleInputChange}
                min="1"
                max="1000"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Budget (₹)
              </label>
              <input
                type="number"
                name="budget"
                value={formData.budget}
                onChange={handleInputChange}
                min="10000"
                step="5000"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
              {selectedTemplate?.budget_ranges && (
                <div className="mt-2 text-xs text-gray-500">
                  Typical ranges: Budget {selectedTemplate.budget_ranges.budget}, 
                  Standard {selectedTemplate.budget_ranges.standard}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Preferences */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Preferences & Style
          </h3>
          
          {Object.entries(preferenceOptions).map(([category, options]) => (
            <div key={category} className="mb-4">
              <h4 className="text-sm font-medium text-gray-700 mb-2 capitalize">
                {category}
              </h4>
              <div className="flex flex-wrap gap-2">
                {options.map((preference) => (
                  <button
                    key={preference}
                    type="button"
                    onClick={() => handlePreferenceToggle(preference)}
                    className={`px-3 py-1 rounded-full text-sm transition-all ${
                      formData.preferences.includes(preference)
                        ? 'bg-purple-500 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {preference}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Special Requirements */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Special Requirements
          </h3>
          
          <div className="flex flex-wrap gap-2">
            {specialRequirementOptions.map((requirement) => (
              <button
                key={requirement}
                type="button"
                onClick={() => handleRequirementToggle(requirement)}
                className={`px-3 py-2 rounded-lg text-sm border transition-all ${
                  formData.special_requirements.includes(requirement)
                    ? 'border-purple-500 bg-purple-50 text-purple-700'
                    : 'border-gray-200 text-gray-700 hover:border-purple-300'
                }`}
              >
                {requirement}
              </button>
            ))}
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {/* Submit Button */}
        <div className="text-center">
          <button
            type="submit"
            className="bg-purple-600 hover:bg-purple-700 text-white font-medium py-3 px-8 rounded-lg transition-colors duration-200 flex items-center mx-auto"
          >
            <SparklesIcon className="h-5 w-5 mr-2" />
            Plan My Event
          </button>
        </div>
      </form>
    </div>
  );
};

export default EventForm;