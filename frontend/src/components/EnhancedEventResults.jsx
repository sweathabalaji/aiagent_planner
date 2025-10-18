import React, { useState } from 'react';
import { 
  ArrowLeftIcon, 
  MapPinIcon, 
  UserGroupIcon, 
  CurrencyRupeeIcon,
  StarIcon,
  PhoneIcon,
  CalendarDaysIcon,
  ClockIcon,
  CheckCircleIcon,
  LightBulbIcon,
  SparklesIcon,
  BuildingOfficeIcon,
  CameraIcon,
  MusicalNoteIcon,
  GiftIcon,
  GlobeAltIcon,
  ArrowTopRightOnSquareIcon,
  ChartBarIcon,
  CpuChipIcon,
  BoltIcon
} from '@heroicons/react/24/outline';

const EnhancedEventResults = ({ results, onBack, onPlanAnother }) => {
  const [selectedVariant, setSelectedVariant] = useState(0);
  const [activeTab, setActiveTab] = useState('overview');

  if (!results || !results.variants || results.variants.length === 0) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-sm p-8 text-center">
          <div className="text-gray-500 mb-4">
            <SparklesIcon className="h-12 w-12 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Event Plans Generated</h3>
          <p className="text-gray-600 mb-6">We couldn't find suitable options for your event. Please try adjusting your requirements.</p>
          <button
            onClick={onBack}
            className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const { variants, cost_analysis, planning_insights, contextual_recommendations, ai_analysis, metadata } = results;
  const currentVariant = variants[selectedVariant];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-4">
              <button
                onClick={onBack}
                className="flex items-center text-gray-600 hover:text-gray-900"
              >
                <ArrowLeftIcon className="h-5 w-5 mr-2" />
                Back
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Your AI-Generated Event Plan</h1>
                <p className="text-gray-600">
                  {metadata?.planning_approach && (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {metadata.planning_approach}
                    </span>
                  )}
                </p>
              </div>
            </div>
            <button
              onClick={onPlanAnother}
              className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg transition-colors"
            >
              Plan Another Event
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* AI Analysis Dashboard */}
        {(cost_analysis || planning_insights || contextual_recommendations) && (
          <div className="mb-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Cost Analysis Card */}
            {cost_analysis && (
              <div className="bg-gradient-to-br from-blue-50 to-indigo-100 rounded-xl p-6 border border-blue-200">
                <div className="flex items-center mb-4">
                  <ChartBarIcon className="h-6 w-6 text-blue-600 mr-2" />
                  <h3 className="text-lg font-semibold text-blue-900">Dynamic Cost Analysis</h3>
                </div>
                {cost_analysis.dynamic_estimation && (
                  <div className="space-y-3">
                    <div className="grid grid-cols-3 gap-2 text-sm">
                      <div className="text-center">
                        <div className="text-green-600 font-medium">Optimistic</div>
                        <div className="text-lg font-bold text-green-800">
                          ₹{cost_analysis.dynamic_estimation.optimistic_total?.toLocaleString() || 'N/A'}
                        </div>
                      </div>
                      <div className="text-center">
                        <div className="text-blue-600 font-medium">Realistic</div>
                        <div className="text-lg font-bold text-blue-800">
                          ₹{cost_analysis.dynamic_estimation.realistic_total?.toLocaleString() || 'N/A'}
                        </div>
                      </div>
                      <div className="text-center">
                        <div className="text-orange-600 font-medium">Conservative</div>
                        <div className="text-lg font-bold text-orange-800">
                          ₹{cost_analysis.dynamic_estimation.pessimistic_total?.toLocaleString() || 'N/A'}
                        </div>
                      </div>
                    </div>
                    {cost_analysis.dynamic_estimation.confidence_level && (
                      <div className="flex items-center justify-center">
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                          cost_analysis.dynamic_estimation.confidence_level === 'high' ? 'bg-green-100 text-green-800' :
                          cost_analysis.dynamic_estimation.confidence_level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-orange-100 text-orange-800'
                        }`}>
                          {cost_analysis.dynamic_estimation.confidence_level.toUpperCase()} Confidence
                        </span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* AI Insights Card */}
            {planning_insights && planning_insights.length > 0 && (
              <div className="bg-gradient-to-br from-green-50 to-emerald-100 rounded-xl p-6 border border-green-200">
                <div className="flex items-center mb-4">
                  <CpuChipIcon className="h-6 w-6 text-green-600 mr-2" />
                  <h3 className="text-lg font-semibold text-green-900">AI Planning Insights</h3>
                </div>
                <ul className="space-y-2">
                  {planning_insights.slice(0, 3).map((insight, index) => (
                    <li key={index} className="flex items-start text-sm text-green-800">
                      <CheckCircleIcon className="h-4 w-4 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                      <span>{insight}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Smart Recommendations Card */}
            {contextual_recommendations && contextual_recommendations.length > 0 && (
              <div className="bg-gradient-to-br from-purple-50 to-violet-100 rounded-xl p-6 border border-purple-200">
                <div className="flex items-center mb-4">
                  <BoltIcon className="h-6 w-6 text-purple-600 mr-2" />
                  <h3 className="text-lg font-semibold text-purple-900">Smart Recommendations</h3>
                </div>
                <ul className="space-y-2">
                  {contextual_recommendations.slice(0, 3).map((recommendation, index) => (
                    <li key={index} className="flex items-start text-sm text-purple-800">
                      <LightBulbIcon className="h-4 w-4 text-purple-600 mr-2 mt-0.5 flex-shrink-0" />
                      <span>{recommendation}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Budget Optimization Tips */}
        {cost_analysis?.cost_optimization && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6 mb-8">
            <h3 className="text-lg font-semibold text-yellow-900 mb-4">💰 Budget Optimization Tips</h3>
            <div className="grid md:grid-cols-2 gap-4">
              {cost_analysis.cost_optimization.slice(0, 4).map((tip, index) => (
                <div key={index} className="flex items-start">
                  <CheckCircleIcon className="h-5 w-5 text-yellow-600 mr-2 mt-0.5 flex-shrink-0" />
                  <span className="text-sm text-yellow-800">{tip}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Variant Selector */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Event Plan Options</h2>
            <p className="text-gray-600 mt-1">Choose the option that best fits your needs and budget</p>
          </div>

          <div className="p-6">
            {/* Variant Tabs */}
            <div className="flex space-x-1 bg-gray-100 rounded-lg p-1 mb-6">
              {variants.map((variant, index) => (
                <button
                  key={index}
                  onClick={() => setSelectedVariant(index)}
                  className={`flex-1 py-3 px-4 rounded-md text-sm font-medium transition-colors ${
                    selectedVariant === index
                      ? 'bg-white text-purple-700 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <div className="flex items-center justify-center space-x-2">
                    <span>{getVariantIcon(variant.variant)}</span>
                    <span className="capitalize">{variant.variant || 'Standard'}</span>
                    {variant.strategy && (
                      <span className="text-xs text-gray-500">({variant.strategy.replace('_', ' ')})</span>
                    )}
                  </div>
                  <div className="text-lg font-bold mt-1">
                    ₹{variant.estimated_cost?.toLocaleString() || 'N/A'}
                  </div>
                </button>
              ))}
            </div>

            {/* Selected Variant Details */}
            <VariantDetails variant={currentVariant} costAnalysis={cost_analysis} />
          </div>
        </div>
      </div>
    </div>
  );
};

const getVariantIcon = (variant) => {
  switch(variant?.toLowerCase()) {
    case 'budget': return '💰';
    case 'standard':
    case 'balanced': return '⚖️';
    case 'premium': return '⭐';
    default: return '📋';
  }
};

const VariantDetails = ({ variant, costAnalysis }) => {
  const { venues = [], vendors = [], cost_breakdown, selection_rationale, timeline } = variant;

  // Group vendors by service type
  const groupedVendors = vendors.reduce((acc, vendor) => {
    const serviceType = vendor.service_type || 'Other';
    if (!acc[serviceType]) acc[serviceType] = [];
    acc[serviceType].push(vendor);
    return acc;
  }, {});

  return (
    <div className="space-y-6">
      {/* Selection Rationale */}
      {selection_rationale && (
        <div className="bg-blue-50 rounded-lg p-4">
          <h4 className="font-semibold text-blue-900 mb-2">Why This Option?</h4>
          <p className="text-sm text-blue-800">{selection_rationale.venue_reason}</p>
          <p className="text-sm text-blue-800 mt-1">{selection_rationale.vendor_reason}</p>
        </div>
      )}

      {/* Cost Breakdown */}
      {cost_breakdown && (
        <div>
          <h4 className="font-semibold text-gray-900 mb-3">Cost Breakdown</h4>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
            {Object.entries(cost_breakdown).map(([category, amount]) => (
              <div key={category} className="bg-gray-50 rounded-lg p-3">
                <div className="text-xs text-gray-600 capitalize">{category}</div>
                <div className="text-sm font-semibold">₹{amount?.toLocaleString() || '0'}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Venues Section */}
        <div>
          <h4 className="font-semibold text-gray-900 mb-4 flex items-center">
            <BuildingOfficeIcon className="h-5 w-5 text-blue-600 mr-2" />
            Venues ({venues.length})
          </h4>
          <div className="space-y-4">
            {venues.slice(0, 3).map((venue, index) => (
              <VenueCard key={index} venue={venue} />
            ))}
          </div>
        </div>

        {/* Vendors Section */}
        <div>
          <h4 className="font-semibold text-gray-900 mb-4 flex items-center">
            <UserGroupIcon className="h-5 w-5 text-green-600 mr-2" />
            Service Providers ({vendors.length})
          </h4>
          <div className="space-y-4">
            {Object.entries(groupedVendors).map(([serviceType, serviceVendors]) => (
              <div key={serviceType}>
                <h5 className="text-sm font-medium text-gray-700 mb-2 capitalize flex items-center">
                  <span className="mr-2">{getServiceIcon(serviceType)}</span>
                  {serviceType} ({serviceVendors.length})
                </h5>
                <div className="space-y-2">
                  {serviceVendors.slice(0, 2).map((vendor, index) => (
                    <VendorCard key={index} vendor={vendor} />
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Timeline Preview */}
      {timeline && timeline.length > 0 && (
        <div>
          <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
            <CalendarDaysIcon className="h-5 w-5 text-purple-600 mr-2" />
            Planning Timeline
          </h4>
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="grid gap-3">
              {timeline.slice(0, 4).map((milestone, index) => (
                <div key={index} className="flex justify-between items-center">
                  <span className="text-sm text-gray-700">{milestone.milestone || 'Planning milestone'}</span>
                  <span className="text-xs text-gray-500 flex items-center">
                    <ClockIcon className="h-3 w-3 mr-1" />
                    {milestone.date ? new Date(milestone.date).toLocaleDateString() : 
                     milestone.weeks_before ? `${milestone.weeks_before} weeks before` : 
                     'TBD'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const getServiceIcon = (serviceType) => {
  switch(serviceType.toLowerCase()) {
    case 'photography': return '📸';
    case 'catering': return '🍽️';
    case 'decoration': return '🎨';
    case 'entertainment': return '🎵';
    default: return '⚙️';
  }
};

const VenueCard = ({ venue }) => {
  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <h5 className="font-medium text-gray-900">{venue.name}</h5>
        {venue.context_relevance_score > 0 && (
          <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
            Context Match: {venue.context_relevance_score}
          </span>
        )}
      </div>
      
      <div className="space-y-1 text-sm text-gray-600">
        {venue.capacity && (
          <p className="flex items-center">
            <UserGroupIcon className="h-4 w-4 mr-1" />
            Capacity: {venue.capacity} guests
          </p>
        )}
        {venue.price_per_day && (
          <p className="flex items-center">
            <CurrencyRupeeIcon className="h-4 w-4 mr-1" />
            Price: ₹{venue.price_per_day.toLocaleString()}/day
          </p>
        )}
        {venue.contact && (
          <p className="flex items-center">
            <PhoneIcon className="h-4 w-4 mr-1" />
            {venue.contact}
          </p>
        )}
        {venue.location && (
          <p className="flex items-center">
            <MapPinIcon className="h-4 w-4 mr-1" />
            {venue.location}
          </p>
        )}
      </div>

      {venue.amenities && venue.amenities.length > 0 && (
        <div className="mt-2">
          <div className="flex flex-wrap gap-1">
            {venue.amenities.slice(0, 3).map((amenity, index) => (
              <span key={index} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                {amenity}
              </span>
            ))}
          </div>
        </div>
      )}

      {venue.url && (
        <div className="mt-3">
          <a
            href={venue.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center text-blue-600 hover:text-blue-800 text-sm"
          >
            <GlobeAltIcon className="h-4 w-4 mr-1" />
            View Details
            <ArrowTopRightOnSquareIcon className="h-3 w-3 ml-1" />
          </a>
        </div>
      )}
    </div>
  );
};

const VendorCard = ({ vendor }) => {
  return (
    <div className="border border-gray-200 rounded-lg p-3 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <h6 className="font-medium text-gray-900 text-sm">{vendor.name}</h6>
        {vendor.context_relevance_score > 0 && (
          <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
            Match: {vendor.context_relevance_score}
          </span>
        )}
      </div>

      <div className="space-y-1 text-xs text-gray-600">
        {vendor.price_range && (
          <p className="flex items-center">
            <CurrencyRupeeIcon className="h-3 w-3 mr-1" />
            {vendor.price_range}
          </p>
        )}
        {vendor.contact && (
          <p className="flex items-center">
            <PhoneIcon className="h-3 w-3 mr-1" />
            {vendor.contact}
          </p>
        )}
        {vendor.email && (
          <p className="flex items-center">
            <GlobeAltIcon className="h-3 w-3 mr-1" />
            {vendor.email}
          </p>
        )}
        {vendor.rating && (
          <p className="flex items-center">
            <StarIcon className="h-3 w-3 mr-1" />
            Rating: {vendor.rating}/5
          </p>
        )}
      </div>

      {vendor.specialties && vendor.specialties.length > 0 && (
        <div className="mt-2">
          <div className="flex flex-wrap gap-1">
            {vendor.specialties.slice(0, 2).map((specialty, index) => (
              <span key={index} className="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded">
                {specialty}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="mt-2 flex space-x-2">
        {vendor.contact && (
          <button className="bg-green-600 text-white text-xs px-3 py-1 rounded hover:bg-green-700 transition-colors">
            Call Now
          </button>
        )}
        {vendor.url && (
          <a
            href={vendor.url}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-blue-600 text-white text-xs px-3 py-1 rounded hover:bg-blue-700 transition-colors inline-flex items-center"
          >
            Website
            <ArrowTopRightOnSquareIcon className="h-3 w-3 ml-1" />
          </a>
        )}
      </div>
    </div>
  );
};

export default EnhancedEventResults;