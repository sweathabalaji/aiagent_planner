import React, { useState } from 'react';
import { 
  ArrowLeftIcon, 
  SparklesIcon,
  CurrencyRupeeIcon,
  LightBulbIcon,
  MapPinIcon,
  StarIcon,
  PhoneIcon,
  UserGroupIcon,
  ClockIcon,
  CameraIcon,
  MusicalNoteIcon,
  GiftIcon,
  BuildingOfficeIcon
} from '@heroicons/react/24/outline';

const EventResults = ({ results, onBack, onPlanAnother }) => {
  const [activeSection, setActiveSection] = useState('analysis');

  if (!results) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-sm p-8 text-center">
          <div className="text-gray-500 mb-4">
            <SparklesIcon className="h-12 w-12 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Event Plan Generated</h3>
          <p className="text-gray-600 mb-6">Please try again with different parameters.</p>
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

  // Extract structured data from backend response  
  const variants = results.variants || [];
  const mainVariant = variants[0] || {};
  const venues = mainVariant.venues || [];
  const vendors = mainVariant.vendors || {};
  const agentAnalysis = results.agent_analysis?.full_analysis || '';
  const costBreakdown = mainVariant.cost_breakdown || {};
  const totalCost = mainVariant.estimated_cost || 0;
  const planningInsights = results.planning_insights || [];
  const contextualRecommendations = results.contextual_recommendations || [];

  // Debug logging to see what we're receiving
  console.log('🔍 EventResults Debug:', {
    hasResults: !!results,
    hasVariants: variants.length > 0,
    hasAgentAnalysis: !!agentAnalysis,
    agentAnalysisLength: agentAnalysis.length,
    agentAnalysisPreview: agentAnalysis.substring(0, 200),
    hasVenues: venues.length > 0,
    hasVendors: Object.keys(vendors).length > 0,
    // Add more detailed debugging
    fullResults: results,
    agentAnalysisSection: results.agent_analysis,
    rawAgentAnalysis: results?.agent_analysis?.full_analysis
  });
  
  // EMERGENCY DEBUG: Log the exact path being used
  console.log('🚨 EMERGENCY DEBUG:', {
    'results': !!results,
    'results.agent_analysis': !!results?.agent_analysis,
    'results.agent_analysis.full_analysis': results?.agent_analysis?.full_analysis,
    'typeof results.agent_analysis.full_analysis': typeof results?.agent_analysis?.full_analysis,
    'results keys': results ? Object.keys(results) : 'no results'
  });

  // DEEP DIVE DEBUG: Log the complete results structure
  console.log('🔬 COMPLETE BACKEND RESPONSE:', JSON.stringify(results, null, 2));
  const metadata = results.metadata || {};

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={onBack}
          className="flex items-center text-purple-600 hover:text-purple-700 mb-6 transition-colors"
        >
          <ArrowLeftIcon className="h-5 w-5 mr-2" />
          Back to Form
        </button>
        
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{results.event_name || 'Your Event Plan'}</h1>
            <p className="text-lg text-gray-600 capitalize">{results.event_type} Event Plan</p>
            {metadata.planning_approach && (
              <div className="mt-2">
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  🤖 {metadata.planning_approach}
                </span>
              </div>
            )}
          </div>
          <button
            onClick={onPlanAnother}
            className="mt-4 sm:mt-0 bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg transition-colors font-medium"
          >
            Plan Another Event
          </button>
        </div>

        {/* Navigation Tabs */}
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            {[
              { id: 'analysis', label: 'AI Analysis', icon: SparklesIcon },
              { id: 'cost', label: 'Cost Summary', icon: CurrencyRupeeIcon },
              { id: 'recommendations', label: 'Recommendations', icon: LightBulbIcon }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveSection(tab.id)}
                  className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                    activeSection === tab.id
                      ? 'border-purple-500 text-purple-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-5 w-5 mr-2" />
                  {tab.label}
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Content Sections */}
      <div className="space-y-6">
        
        {/* AI Analysis Section */}
        {activeSection === 'analysis' && (
          <div className="space-y-6">
            {/* Agent Analysis Display */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">🤖 AI Agent Analysis</h2>
                <p className="text-gray-600">Comprehensive event planning analysis</p>
              </div>
              
              {agentAnalysis && agentAnalysis.length > 0 ? (
                <div className="space-y-6">
                  {/* Extract and display structured sections */}
                  {(() => {
                    // Split content by ## sections and find matching ones
                    const splitSections = agentAnalysis.split(/\n## /).slice(1); // Remove first empty element
                    
                    const sections = [
                      { title: '🏛️ Venue Recommendations', searchText: 'Venue Recommendations' },
                      { title: '🍽️ Catering Services', searchText: 'Catering Services' },
                      { title: '📸 Photography Services', searchText: 'Photography Services' },
                      { title: '🎨 Decoration Services', searchText: 'Decoration Services' },
                      { title: '🎵 Entertainment Services', searchText: 'Entertainment Services' },
                      { title: '💰 Budget Allocation', searchText: 'Recommended Budget Allocation' }
                    ];

                    console.log('🔍 Debug: agentAnalysis length:', agentAnalysis.length);
                    console.log('🔍 Debug: splitSections count:', splitSections.length);
                    console.log('🔍 Debug: splitSections titles:', splitSections.map(s => s.split('\n')[0]));

                    const extractedSections = sections.map(section => {
                      const foundSection = splitSections.find(s => 
                        s.toLowerCase().includes(section.searchText.toLowerCase())
                      );
                      console.log(`🔍 Debug: ${section.title} found:`, foundSection ? 'YES' : 'NO');
                      return foundSection ? { ...section, content: '## ' + foundSection } : null;
                    }).filter(Boolean);

                    // Get the full analysis for overview
                    const overviewContent = agentAnalysis.split('## Venue Recommendations')[0];

                    return (
                      <>
                        {/* Overview Section */}
                        {overviewContent && (
                          <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg border-l-4 border-blue-500">
                            <h3 className="text-lg font-semibold text-gray-900 mb-3">📋 Event Overview</h3>
                            <div className="text-gray-800 leading-relaxed whitespace-pre-wrap text-sm">
                              {overviewContent.trim()}
                            </div>
                          </div>
                        )}

                        {/* Structured Sections */}
                        {extractedSections.length > 0 ? (
                          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            {extractedSections.map((section, index) => (
                              <div key={index} className="bg-gradient-to-br from-white to-gray-50 p-6 rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
                                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                                  {section.title}
                                </h3>
                                <div className="text-gray-700 leading-relaxed whitespace-pre-wrap text-sm max-h-64 overflow-y-auto">
                                  {section.content.replace(/^## [^\n]+\n/, '').trim()}
                                </div>
                              </div>
                            ))}
                          </div>
                        ) : (
                          // Fallback: Show full analysis if sections can't be extracted
                          <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg border-l-4 border-blue-500">
                            <h3 className="text-lg font-semibold text-gray-900 mb-3">📋 Complete AI Analysis</h3>
                            <div className="text-gray-800 leading-relaxed whitespace-pre-wrap text-sm max-h-96 overflow-y-auto">
                              {agentAnalysis}
                            </div>
                            <div className="mt-4 text-xs text-gray-600">
                              Note: Structured parsing unavailable - showing full analysis
                            </div>
                          </div>
                        )}

                        {/* Additional Sections (if any) */}
                        {(() => {
                          const additionalContent = agentAnalysis.split(/## Additional Recommendations:?/)[1];
                          if (additionalContent) {
                            return (
                              <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg border-l-4 border-green-500">
                                <h3 className="text-lg font-semibold text-gray-900 mb-3">✨ Additional Recommendations</h3>
                                <div className="text-gray-800 leading-relaxed whitespace-pre-wrap text-sm">
                                  {additionalContent.trim()}
                                </div>
                              </div>
                            );
                          }
                          return null;
                        })()}
                      </>
                    );
                  })()}
                </div>
              ) : (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
                  <div className="text-yellow-800">
                    <span>No analysis provided by the AI agent</span>
                  </div>
                </div>
              )}
            </div>

            {/* AI Recommendations */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">💡 AI Smart Recommendations</h2>
                <p className="text-gray-600">Intelligent insights and strategic recommendations</p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Planning Insights */}
                <div className="bg-gradient-to-br from-green-50 to-emerald-50 p-6 rounded-xl border border-green-200">
                  <div className="flex items-center mb-4">
                    <div className="bg-green-500 rounded-full p-2 mr-3">
                      <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014.846 21H9.154a3.374 3.374 0 00-2.674-1.06l-.548-.547z" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-semibold text-green-900">Planning Insights</h3>
                  </div>
                  
                  {planningInsights?.length > 0 ? (
                    <div className="space-y-3">
                      {planningInsights.map((insight, index) => (
                        <div key={index} className="flex items-start bg-white p-3 rounded-lg shadow-sm">
                          <span className="text-green-500 mr-3 mt-1 text-lg">💡</span>
                          <span className="text-sm text-gray-700 leading-relaxed">{insight}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-4 text-green-600">
                      <p className="text-sm">AI insights will appear here</p>
                    </div>
                  )}
                </div>

                {/* Contextual Recommendations */}
                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-6 rounded-xl border border-blue-200">
                  <div className="flex items-center mb-4">
                    <div className="bg-blue-500 rounded-full p-2 mr-3">
                      <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-semibold text-blue-900">Smart Recommendations</h3>
                  </div>
                  
                  {contextualRecommendations?.length > 0 ? (
                    <div className="space-y-3">
                      {contextualRecommendations.map((recommendation, index) => (
                        <div key={index} className="flex items-start bg-white p-3 rounded-lg shadow-sm">
                          <span className="text-blue-500 mr-3 mt-1 text-lg">🎯</span>
                          <span className="text-sm text-gray-700 leading-relaxed">{recommendation}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-4 text-blue-600">
                      <p className="text-sm">AI recommendations will appear here</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Additional AI Tips Section */}
              {(planningInsights?.length > 0 || contextualRecommendations?.length > 0) && (
                <div className="mt-6 bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-lg border border-purple-200">
                  <div className="flex items-center text-purple-800">
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span className="text-sm font-medium">Pro Tip: These recommendations are generated by analyzing current market trends and your specific requirements!</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Real Venues from Agent */}
        {activeSection === 'venues' && venues.length > 0 && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">🏛️ Recommended Venues</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {venues.map((venue, index) => (
                  <div key={index} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between mb-3">
                      <h4 className="font-semibold text-gray-900 leading-tight">
                        {venue.name || `Venue Option ${index + 1}`}
                      </h4>
                      <div className="flex items-center text-yellow-500 text-sm">
                        <StarIcon className="h-4 w-4 mr-1" />
                        <span>{venue.rating || '4.0'}</span>
                      </div>
                    </div>
                    
                    {venue.location && (
                      <div className="flex items-center text-gray-600 text-sm mb-2">
                        <MapPinIcon className="h-4 w-4 mr-1" />
                        <span>{venue.location}</span>
                      </div>
                    )}
                    
                    {venue.capacity && (
                      <div className="flex items-center text-gray-600 text-sm mb-2">
                        <UserGroupIcon className="h-4 w-4 mr-1" />
                        <span>Capacity: {venue.capacity} guests</span>
                      </div>
                    )}
                    
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <div className="flex justify-between items-center">
                        <span className="font-semibold text-green-600">
                          {venue.price || 'Contact for pricing'}
                        </span>
                        {venue.contact && (
                          <button className="text-blue-600 hover:text-blue-800 text-sm">
                            Contact
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Real Vendors from Agent */}
            {(vendors.catering?.length > 0 || vendors.photography?.length > 0 || vendors.decoration?.length > 0) && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">🏢 Recommended Vendors</h3>
                
                <div className="space-y-6">
                  {/* Catering */}
                  {vendors.catering?.length > 0 && (
                    <div>
                      <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                        <GiftIcon className="h-5 w-5 mr-2 text-orange-500" />
                        Catering Services
                      </h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {vendors.catering.slice(0, 3).map((vendor, index) => (
                          <VendorCard key={index} vendor={vendor} serviceType="catering" />
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Photography */}
                  {vendors.photography?.length > 0 && (
                    <div>
                      <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                        <CameraIcon className="h-5 w-5 mr-2 text-blue-500" />
                        Photography Services
                      </h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {vendors.photography.slice(0, 3).map((vendor, index) => (
                          <VendorCard key={index} vendor={vendor} serviceType="photography" />
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Decoration */}
                  {vendors.decoration?.length > 0 && (
                    <div>
                      <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                        <SparklesIcon className="h-5 w-5 mr-2 text-pink-500" />
                        Decoration Services
                      </h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {vendors.decoration.slice(0, 3).map((vendor, index) => (
                          <VendorCard key={index} vendor={vendor} serviceType="decoration" />
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Cost Summary Section */}
        {activeSection === 'cost' && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">💰 Cost Summary</h2>
              <p className="text-gray-600">Budget breakdown and total costs</p>
            </div>
            
            {totalCost > 0 ? (
              <>
                <div className="mb-6 p-6 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg border">
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Total Estimated Cost</h3>
                  <p className="text-3xl font-bold text-green-600">₹{totalCost.toLocaleString('en-IN')}</p>
                  <p className="text-sm text-gray-600 mt-2">For {results.variants?.[0]?.timeline?.find(t => t.activity.includes('Guests:'))?.activity.match(/\d+/)?.[0] || '50'} guests</p>
                </div>

                {Object.keys(costBreakdown).length > 0 && (
                  <div className="bg-gray-50 rounded-lg p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Cost Breakdown</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {Object.entries(costBreakdown).map(([category, cost]) => (
                        <div key={category} className="bg-white p-4 rounded-lg border shadow-sm">
                          <p className="text-sm text-gray-600 capitalize font-medium">{category}</p>
                          <p className="text-lg font-bold text-gray-900">
                            ₹{typeof cost === 'number' ? cost.toLocaleString('en-IN') : cost}
                          </p>
                          <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                            <div 
                              className="bg-purple-600 h-2 rounded-full" 
                              style={{width: `${(typeof cost === 'number' ? cost : 0) / totalCost * 100}%`}}
                            ></div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Budget Analysis */}
                <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                    <h4 className="font-semibold text-blue-900 mb-1">Budget Status</h4>
                    <p className="text-blue-800">Within Budget</p>
                  </div>
                  <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                    <h4 className="font-semibold text-green-900 mb-1">Cost per Guest</h4>
                    <p className="text-green-800">₹{Math.round(totalCost / 50).toLocaleString('en-IN')}</p>
                  </div>
                  <div className="bg-yellow-50 p-4 rounded-lg border-l-4 border-yellow-500">
                    <h4 className="font-semibold text-yellow-900 mb-1">Payment Method</h4>
                    <p className="text-yellow-800">30% advance + installments</p>
                  </div>
                </div>
              </>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <CurrencyRupeeIcon className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                <p>No cost breakdown available</p>
              </div>
            )}
          </div>
        )}

        {/* Recommendations Section */}
        {activeSection === 'recommendations' && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">💡 AI Recommendations</h2>
              <p className="text-gray-600">Suggestions and recommendations from the AI agent</p>
            </div>
            
            {/* Key Recommendations from Agent Analysis */}
            {(planningInsights.length > 0 || contextualRecommendations.length > 0) ? (
              <div className="space-y-6">
                {/* Planning Insights */}
                {planningInsights.length > 0 && (
                  <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg border-l-4 border-green-500">
                    <h3 className="text-lg font-semibold text-green-900 mb-4">📋 Planning Insights</h3>
                    <div className="space-y-3">
                      {planningInsights.map((insight, index) => (
                        <div key={index} className="flex items-start">
                          <div className="bg-green-500 rounded-full w-2 h-2 mt-2 mr-3 flex-shrink-0"></div>
                          <p className="text-green-800">{insight}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Contextual Recommendations */}
                {contextualRecommendations.length > 0 && (
                  <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-lg border-l-4 border-purple-500">
                    <h3 className="text-lg font-semibold text-purple-900 mb-4">🎯 Smart Recommendations</h3>
                    <div className="space-y-3">
                      {contextualRecommendations.map((rec, index) => (
                        <div key={index} className="flex items-start">
                          <div className="bg-purple-500 rounded-full w-2 h-2 mt-2 mr-3 flex-shrink-0"></div>
                          <p className="text-purple-800">{rec}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Event Highlights from Budget */}
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border-l-4 border-blue-500">
                  <h3 className="text-lg font-semibold text-blue-900 mb-4">📋 Event Planning Highlights</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-white p-4 rounded-lg">
                      <h4 className="font-medium text-gray-900 mb-2">🏛️ Event Style</h4>
                      <p className="text-gray-700">AI-optimized event planning</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg">
                      <h4 className="font-medium text-gray-900 mb-2">💰 Budget Range</h4>
                      <p className="text-gray-700">₹{totalCost.toLocaleString('en-IN')}</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg">
                      <h4 className="font-medium text-gray-900 mb-2">� Location Focus</h4>
                      <p className="text-gray-700">{results.location || 'Chennai'}</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg">
                      <h4 className="font-medium text-gray-900 mb-2">🤖 Planning Mode</h4>
                      <p className="text-gray-700">AI Agent Powered</p>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <LightBulbIcon className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                <p>No specific recommendations available</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

// VendorCard component for displaying individual vendor information
const VendorCard = ({ vendor, serviceType }) => {
  return (
    <div className="border rounded-lg p-4 hover:shadow-md transition-shadow bg-white">
      <div className="flex items-start justify-between mb-3">
        <h5 className="font-semibold text-gray-900 leading-tight">
          {vendor.name || `${serviceType.charAt(0).toUpperCase() + serviceType.slice(1)} Service`}
        </h5>
        <div className="flex items-center text-yellow-500 text-sm">
          <StarIcon className="h-4 w-4 mr-1" />
          <span>{vendor.rating || '4.2'}</span>
        </div>
      </div>
      
      <div className="space-y-2 text-sm text-gray-600">
        <div className="flex items-center">
          <BuildingOfficeIcon className="h-4 w-4 mr-2" />
          <span className="capitalize">{vendor.service || serviceType}</span>
        </div>
        
        <div className="flex items-center">
          <CurrencyRupeeIcon className="h-4 w-4 mr-2" />
          <span>{vendor.price || 'Quote available'}</span>
        </div>

        {vendor.contact && (
          <div className="flex items-center">
            <PhoneIcon className="h-4 w-4 mr-2" />
            <span className="text-blue-600 hover:text-blue-800 cursor-pointer">Contact</span>
          </div>
        )}
      </div>

      {vendor.specialties && vendor.specialties.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-200">
          <div className="flex flex-wrap gap-1">
            {vendor.specialties.slice(0, 3).map((specialty, idx) => (
              <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                {specialty}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default EventResults;
