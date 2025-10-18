import React, { useState } from 'react'
import { ArrowLeft, Plane, Building, MapPin, Calendar, RefreshCw, ChevronDown, ChevronUp } from 'lucide-react'

const TravelResults = ({ results, onBack, onPlanAnother }) => {
  const [selectedVariant, setSelectedVariant] = useState(0)
  const [expandedSections, setExpandedSections] = useState({
    flights: true,
    hotels: true,
    itinerary: true
  })

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }))
  }

  const variant = results?.variants[selectedVariant]

  if (!results || !variant) {
    return (
      <div className="text-center py-16">
        <p className="text-gray-500">No results available</p>
        <button onClick={onBack} className="btn-primary mt-4">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Form
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      {/* Header */}
      <div className="card mb-8">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Your Travel Plan is Ready!</h1>
            <p className="text-gray-600">Choose from our AI-generated variants below</p>
          </div>
          <div className="flex space-x-3">
            <button onClick={onBack} className="btn-secondary flex items-center">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </button>
            <button onClick={onPlanAnother} className="btn-primary flex items-center">
              <RefreshCw className="h-4 w-4 mr-2" />
              Plan Another Trip
            </button>
          </div>
        </div>
      </div>

      {/* Variant Selector */}
      <div className="card mb-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Choose Your Plan Variant</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {results.variants.map((v, index) => (
            <button
              key={index}
              onClick={() => setSelectedVariant(index)}
              className={`p-4 rounded-lg border-2 transition-all duration-200 text-left ${
                selectedVariant === index
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-blue-300 bg-white'
              }`}
            >
              <div className="flex justify-between items-start mb-3">
                <h4 className="font-semibold text-gray-900 capitalize flex items-center">
                  {v.variant === 'budget' && <span className="text-green-600 mr-2">💰</span>}
                  {v.variant === 'standard' && <span className="text-blue-600 mr-2">⭐</span>}
                  {v.variant === 'premium' && <span className="text-purple-600 mr-2">👑</span>}
                  {v.variant}
                </h4>
                <div className="text-right">
                  <div className="text-lg font-bold text-blue-600">
                    ₹{v.estimated_cost.toFixed(0)}
                  </div>
                  <div className="text-xs text-gray-500">Total Cost</div>
                  {v.within_budget && (
                    <div className="text-xs text-green-600 mt-1">
                      ✓ Within Budget
                    </div>
                  )}
                </div>
              </div>
              <div className="text-sm text-gray-600 space-y-1">
                <div>{v.flights.length} flight options</div>
                <div>{v.hotels.length} hotel options</div>
                <div>{v.itinerary.length} day itinerary</div>
                {v.savings > 0 && (
                  <div className="text-green-600 text-xs font-medium">
                    Saves ₹{v.savings.toFixed(0)}
                  </div>
                )}
              </div>
              <div className="mt-3">
                <div className="text-xs text-gray-500 mb-1">Features:</div>
                <div className="text-xs text-gray-600">
                  {v.features?.slice(0, 2).join(', ')}
                  {v.features?.length > 2 && '...'}
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Cost Breakdown Section */}
      {variant.cost_breakdown && (
        <div className="card mb-8 bg-gradient-to-r from-amber-50 to-orange-50 border-orange-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <span className="mr-2">💳</span>
            Cost Breakdown - {variant.variant.charAt(0).toUpperCase() + variant.variant.slice(1)} Plan
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-3 bg-white rounded-lg border border-orange-100">
              <div className="text-lg font-bold text-blue-600">₹{variant.cost_breakdown.flights?.toFixed(0) || '0'}</div>
              <div className="text-xs text-gray-600">Flights (Round Trip)</div>
            </div>
            <div className="text-center p-3 bg-white rounded-lg border border-orange-100">
              <div className="text-lg font-bold text-green-600">₹{variant.cost_breakdown.accommodation?.toFixed(0) || '0'}</div>
              <div className="text-xs text-gray-600">Accommodation</div>
            </div>
            <div className="text-center p-3 bg-white rounded-lg border border-orange-100">
              <div className="text-lg font-bold text-purple-600">₹{variant.cost_breakdown.activities?.toFixed(0) || '0'}</div>
              <div className="text-xs text-gray-600">Activities & Attractions</div>
            </div>
            <div className="text-center p-3 bg-white rounded-lg border border-orange-100">
              <div className="text-lg font-bold text-orange-600">₹{variant.cost_breakdown.daily_expenses?.toFixed(0) || '0'}</div>
              <div className="text-xs text-gray-600">Meals & Transport</div>
            </div>
          </div>
          <div className="mt-4 p-3 bg-white rounded-lg border border-orange-100 text-center">
            <div className="text-xl font-bold text-gray-900">
              Total: ₹{variant.cost_breakdown.total?.toFixed(0) || variant.estimated_cost.toFixed(0)}
            </div>
            <div className="text-sm text-gray-600">
              {variant.within_budget ? '✅ Within your budget' : '⚠️ Exceeds budget'} 
              {variant.savings > 0 && ` • Saves ₹${variant.savings.toFixed(0)}`}
            </div>
          </div>
        </div>
      )}

      {/* Flights Section */}
      <div className="card mb-8">
        <button
          onClick={() => toggleSection('flights')}
          className="w-full flex items-center justify-between text-left mb-4"
        >
          <h3 className="text-xl font-semibold text-gray-900 flex items-center">
            <Plane className="h-5 w-5 mr-2 text-blue-600" />
            Flight Options ({variant.flights.length})
          </h3>
          {expandedSections.flights ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
        </button>
        
        {expandedSections.flights && (
          <div className="space-y-4">
            {variant.flights.length > 0 ? (
              variant.flights.slice(0, 3).map((flight, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-semibold text-gray-900">
                        {flight.airline || `Flight Option ${index + 1}`}
                      </div>
                      <div className="text-sm text-gray-600 mt-1">
                        {flight.route || `${flight.provider} Flight`}
                      </div>
                      {flight.url && (
                        <a href={flight.url} target="_blank" rel="noopener noreferrer" 
                           className="text-blue-500 text-xs hover:underline mt-1 inline-block">
                          View Booking Details →
                        </a>
                      )}
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-blue-600">
                        ₹{flight.price ? flight.price.toFixed(0) : 'N/A'}
                      </div>
                      <div className="text-xs text-gray-500">per person</div>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-4">No flights found for this route</p>
            )}
          </div>
        )}
      </div>

      {/* Hotels Section */}
      <div className="card mb-8">
        <button
          onClick={() => toggleSection('hotels')}
          className="w-full flex items-center justify-between text-left mb-4"
        >
          <h3 className="text-xl font-semibold text-gray-900 flex items-center">
            <Building className="h-5 w-5 mr-2 text-blue-600" />
            Hotel Options ({variant.hotels.length})
          </h3>
          {expandedSections.hotels ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
        </button>
        
        {expandedSections.hotels && (
          <div className="space-y-4">
            {variant.hotels.length > 0 ? (
              variant.hotels.slice(0, 3).map((hotel, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="font-semibold text-gray-900">
                        {hotel.name || `Hotel Option ${index + 1}`}
                      </div>
                      <div className="text-sm text-gray-600 mt-1">
                        {hotel.location || 'City Center'}
                      </div>
                      {hotel.price_per_night && (
                        <div className="text-sm text-gray-500 mt-1">
                          ₹{hotel.price_per_night.toFixed(0)} per night
                        </div>
                      )}
                      {hotel.url && (
                        <a href={hotel.url} target="_blank" rel="noopener noreferrer" 
                           className="text-blue-500 text-xs hover:underline mt-1 inline-block">
                          View Hotel Details →
                        </a>
                      )}
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-blue-600">
                        ₹{hotel.total_price ? hotel.total_price.toFixed(0) : 
                           (hotel.price ? (hotel.price * 3).toFixed(0) : 
                            (hotel.price_per_night ? (hotel.price_per_night * 3).toFixed(0) : 'Call for rates'))}
                      </div>
                      <div className="text-xs text-gray-500">total stay</div>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-4">No hotels found for this destination</p>
            )}
          </div>
        )}
      </div>

      {/* Itinerary Section */}
      <div className="card">
        <button
          onClick={() => toggleSection('itinerary')}
          className="w-full flex items-center justify-between text-left mb-4"
        >
          <h3 className="text-xl font-semibold text-gray-900 flex items-center">
            <Calendar className="h-5 w-5 mr-2 text-blue-600" />
            Daily Itinerary ({variant.itinerary.length} days)
          </h3>
          {expandedSections.itinerary ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
        </button>
        
        {expandedSections.itinerary && (
          <div className="space-y-6">
            {variant.itinerary.length > 0 ? (
              variant.itinerary.map((day, index) => (
                <div key={index} className="border-l-4 border-blue-500 pl-4">
                  <div className="flex items-center space-x-2 mb-3">
                    <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold">
                      {day.day}
                    </div>
                    <h4 className="font-semibold text-gray-900">Day {day.day}</h4>
                    {day.date && (
                      <span className="text-sm text-gray-500">
                        ({day.date})
                      </span>
                    )}
                  </div>
                  
                  <div className="space-y-3">
                    {day.activities && day.activities.length > 0 ? (
                      day.activities.map((activity, actIndex) => (
                        <div key={actIndex} className="bg-gray-50 rounded-lg p-3">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <div className="flex items-center space-x-2 mb-1">
                                <span className="font-medium text-blue-600 text-sm">
                                  {activity.time || `${9 + (actIndex * 3)}:00 AM - ${12 + (actIndex * 3)}:00 PM`}
                                </span>
                                <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                                  {activity.type || 'sightseeing'}
                                </span>
                              </div>
                              <div className="font-medium text-gray-900 text-sm">
                                {activity.activity || activity.name || `Visit Local Attraction`}
                              </div>
                              <div className="flex items-center space-x-1 text-xs text-gray-500 mt-1">
                                <MapPin className="h-3 w-3" />
                                <span>{activity.location || 'City Center'}</span>
                              </div>
                              {(activity.description && activity.description.length > 10) && (
                                <div className="text-xs text-gray-600 mt-1">
                                  {activity.description.slice(0, 120)}
                                  {activity.description.length > 120 ? '...' : ''}
                                </div>
                              )}
                              {activity.cost > 0 && (
                                <div className="text-xs text-green-600 mt-1">
                                  Entry fee: ₹{activity.cost}
                                </div>
                              )}
                              {activity.url && (
                                <a href={activity.url} target="_blank" rel="noopener noreferrer" 
                                   className="text-blue-500 text-xs hover:underline mt-1 inline-block">
                                  More Info →
                                </a>
                              )}
                            </div>
                            {activity.rating && (
                              <div className="text-right">
                                <div className="text-xs text-yellow-600">
                                  ⭐ {activity.rating}
                                </div>
                              </div>
                            )}
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="text-sm text-gray-500 italic">Free day / No specific activities planned</div>
                    )}
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-4">No itinerary generated</p>
            )}
          </div>
        )}
      </div>

      {/* Summary Card */}
      <div className="card mt-8 bg-gradient-to-r from-blue-50 to-cyan-50">
        <div className="text-center">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Trip Summary</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <div className="text-2xl font-bold text-blue-600">{variant.flights.length}</div>
              <div className="text-sm text-gray-600">Flight Options</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-blue-600">{variant.hotels.length}</div>
              <div className="text-sm text-gray-600">Hotel Options</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-blue-600">{variant.itinerary.length}</div>
              <div className="text-sm text-gray-600">Days Planned</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-blue-600">₹{variant.estimated_cost.toFixed(0)}</div>
              <div className="text-sm text-gray-600">Estimated Cost</div>
            </div>
          </div>
          {results.saved_plan_id && (
            <div className="mt-4 text-sm text-gray-600">
              Plan ID: {results.saved_plan_id}
            </div>
          )}
        </div>
      </div>

      {/* AI Recommendations Section */}
      {results.recommendations && (
        <div className="card mt-8 bg-gradient-to-r from-green-50 to-emerald-50 border-green-200">
          <div className="flex items-center mb-4">
            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-3">
              <span className="text-green-600 text-lg">🤖</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-900">AI Travel Recommendations</h3>
          </div>

          {/* Summary Section */}
          {results.recommendations.summary && (
            <div className="mb-6 p-4 bg-white rounded-lg border border-green-100">
              <h4 className="font-semibold text-gray-900 mb-3">Trip Overview</h4>
              <div className="space-y-2 text-sm text-gray-700">
                <p><strong>Destination:</strong> {results.recommendations.summary.destination_overview}</p>
                <p><strong>Budget Analysis:</strong> {results.recommendations.summary.budget_analysis}</p>
                <p><strong>Best Time:</strong> {results.recommendations.summary.best_time_insight}</p>
                {results.recommendations.summary.trip_highlights && (
                  <div>
                    <strong>Highlights:</strong>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {results.recommendations.summary.trip_highlights.map((highlight, index) => (
                        <span key={index} className="inline-block bg-green-100 text-green-700 px-2 py-1 rounded text-xs">
                          {highlight}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Variant Analysis */}
          {results.recommendations.variant_analysis && (
            <div className="mb-6 p-4 bg-white rounded-lg border border-green-100">
              <h4 className="font-semibold text-gray-900 mb-3">Plan Analysis</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                {results.recommendations.variant_analysis.best_value && (
                  <div className="p-3 bg-yellow-50 rounded border border-yellow-200">
                    <div className="font-medium text-yellow-800">🏆 Best Value</div>
                    <div className="text-yellow-700 capitalize">{results.recommendations.variant_analysis.best_value.variant} Plan</div>
                    <div className="text-xs text-yellow-600 mt-1">{results.recommendations.variant_analysis.best_value.reason}</div>
                  </div>
                )}
                {results.recommendations.variant_analysis.most_comprehensive && (
                  <div className="p-3 bg-purple-50 rounded border border-purple-200">
                    <div className="font-medium text-purple-800">📋 Most Comprehensive</div>
                    <div className="text-purple-700 capitalize">{results.recommendations.variant_analysis.most_comprehensive.variant} Plan</div>
                    <div className="text-xs text-purple-600 mt-1">{results.recommendations.variant_analysis.most_comprehensive.reason}</div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Tips Sections */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Personalized Tips */}
            {results.recommendations.personalized_tips && (
              <div className="p-4 bg-white rounded-lg border border-green-100">
                <h5 className="font-medium text-gray-900 mb-2 flex items-center">
                  <span className="mr-2">💡</span>Personal Tips
                </h5>
                <ul className="text-xs text-gray-600 space-y-1">
                  {results.recommendations.personalized_tips.slice(0, 4).map((tip, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-green-500 mr-1">•</span>
                      <span>{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Smart Savings */}
            {results.recommendations.smart_savings && (
              <div className="p-4 bg-white rounded-lg border border-green-100">
                <h5 className="font-medium text-gray-900 mb-2 flex items-center">
                  <span className="mr-2">💰</span>Smart Savings
                </h5>
                <ul className="text-xs text-gray-600 space-y-1">
                  {results.recommendations.smart_savings.slice(0, 4).map((tip, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-green-500 mr-1">•</span>
                      <span>{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Safety Tips */}
            {results.recommendations.safety_tips && (
              <div className="p-4 bg-white rounded-lg border border-green-100">
                <h5 className="font-medium text-gray-900 mb-2 flex items-center">
                  <span className="mr-2">🛡️</span>Safety Tips
                </h5>
                <ul className="text-xs text-gray-600 space-y-1">
                  {results.recommendations.safety_tips.slice(0, 4).map((tip, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-blue-500 mr-1">•</span>
                      <span>{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default TravelResults
