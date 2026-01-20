import { useState } from 'react';
import BusinessForm from './BusinessForm';
import BusinessResults from './BusinessResults';
import LoadingSpinner from './LoadingSpinner';
import { BriefcaseIcon, SparklesIcon } from '@heroicons/react/24/outline';

export default function BusinessPlanner() {
  const [isLoading, setIsLoading] = useState(false);
  const [businessPlan, setBusinessPlan] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (formData) => {
    setIsLoading(true);
    setError(null);
    setBusinessPlan(null);

    try {
      const response = await fetch('http://localhost:8000/api/business/plan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate business plan');
      }

      const data = await response.json();
      setBusinessPlan(data);
    } catch (err) {
      setError(err.message || 'An error occurred while generating your business plan');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setBusinessPlan(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <BriefcaseIcon className="w-12 h-12 text-blue-600" />
            <h1 className="text-4xl font-bold text-gray-900">Business Startup Planner</h1>
          </div>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            AI-powered comprehensive business planning with funding strategy, market analysis, and growth roadmap
          </p>
          <div className="mt-4 flex items-center justify-center gap-6 text-sm text-gray-600 flex-wrap">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
              <span>Business Model Canvas</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span>Funding Strategy</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
              <span>Market Analysis</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-orange-500 rounded-full animate-pulse"></div>
              <span>Go-to-Market Plan</span>
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="max-w-4xl mx-auto mb-6">
            <div className="bg-red-50 border border-red-200 text-red-800 px-6 py-4 rounded-lg">
              <div className="flex items-start gap-3">
                <svg className="w-6 h-6 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <div>
                  <h3 className="font-semibold mb-1">Error</h3>
                  <p>{error}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Main Content */}
        {!businessPlan && !isLoading && (
          <div className="max-w-4xl mx-auto">
            <BusinessForm onSubmit={handleSubmit} isLoading={isLoading} />
          </div>
        )}

        {isLoading && (
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-lg shadow-xl p-12">
              <div className="flex flex-col items-center justify-center">
                <div className="relative mb-8">
                  <div className="w-24 h-24 border-8 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
                  <BriefcaseIcon className="w-12 h-12 text-blue-600 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3 flex items-center gap-2">
                  <SparklesIcon className="w-6 h-6 text-yellow-500 animate-pulse" />
                  Creating Your Business Plan
                </h3>
                <div className="space-y-3 text-center max-w-md">
                  <p className="text-gray-600 animate-pulse">🎨 Designing Business Model Canvas...</p>
                  <p className="text-gray-600 animate-pulse delay-100">💰 Crafting Funding Strategy...</p>
                  <p className="text-gray-600 animate-pulse delay-200">📊 Analyzing Market Opportunities...</p>
                  <p className="text-gray-600 animate-pulse delay-300">🎯 Building Go-to-Market Plan...</p>
                  <p className="text-gray-600 animate-pulse delay-400">📈 Projecting Financial Growth...</p>
                </div>
                <p className="mt-6 text-sm text-gray-500">This may take 30-60 seconds...</p>
              </div>
            </div>
          </div>
        )}

        {businessPlan && !isLoading && (
          <div className="max-w-7xl mx-auto">
            {/* Success Header */}
            <div className="bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-lg shadow-xl p-6 mb-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="bg-white/20 backdrop-blur rounded-full p-3">
                    <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold">Business Plan Generated Successfully!</h2>
                    <p className="text-green-100">Your comprehensive startup roadmap is ready to review</p>
                  </div>
                </div>
                <button
                  onClick={handleReset}
                  className="bg-white text-green-600 px-6 py-3 rounded-lg font-semibold hover:bg-green-50 transition-colors shadow-lg"
                >
                  Create New Plan
                </button>
              </div>
            </div>

            {/* Results */}
            <BusinessResults results={businessPlan} />
          </div>
        )}

        {/* Features Section (shown when no plan is generated) */}
        {!businessPlan && !isLoading && (
          <div className="max-w-6xl mx-auto mt-12">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-3">What's Included in Your Business Plan</h2>
              <p className="text-gray-600">Comprehensive AI-powered analysis to launch and grow your startup</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
                <div className="bg-yellow-100 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                  <span className="text-2xl">🎨</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Business Model Canvas</h3>
                <p className="text-gray-600 text-sm">
                  Complete 9-building-block framework: value propositions, customer segments, revenue streams, and more
                </p>
              </div>
              <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
                <div className="bg-green-100 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                  <span className="text-2xl">💰</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Funding Strategy</h3>
                <p className="text-gray-600 text-sm">
                  Detailed funding stages, investor targeting, pitch deck outline, and alternative funding options
                </p>
              </div>
              <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
                <div className="bg-blue-100 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                  <span className="text-2xl">📊</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Market Analysis</h3>
                <p className="text-gray-600 text-sm">
                  TAM/SAM/SOM calculations, market trends, customer insights, and entry barriers analysis
                </p>
              </div>
              <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
                <div className="bg-purple-100 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                  <span className="text-2xl">🎯</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Competitive Analysis</h3>
                <p className="text-gray-600 text-sm">
                  SWOT analysis, competitive advantages, market positioning, and differentiation strategies
                </p>
              </div>
              <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
                <div className="bg-emerald-100 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                  <span className="text-2xl">📈</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Financial Projections</h3>
                <p className="text-gray-600 text-sm">
                  3-year revenue forecast, startup costs, monthly operating costs, and key metrics to track
                </p>
              </div>
              <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
                <div className="bg-orange-100 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                  <span className="text-2xl">🚀</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Go-to-Market Strategy</h3>
                <p className="text-gray-600 text-sm">
                  Launch strategy, marketing channels, sales approach, and customer acquisition tactics
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
